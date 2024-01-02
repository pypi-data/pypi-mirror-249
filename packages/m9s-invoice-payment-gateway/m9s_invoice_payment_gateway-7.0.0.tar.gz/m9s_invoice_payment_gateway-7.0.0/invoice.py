# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from decimal import Decimal

from trytond.exceptions import UserError
from trytond.model import ModelView, fields
from trytond.modules.currency.fields import Monetary
from trytond.modules.payment_gateway.transaction import BaseCreditCardViewMixin
from trytond.pool import Pool, PoolMeta
from trytond.pyson import And, Bool, Eval, Id, If, Not, Or
from trytond.rpc import RPC
from trytond.transaction import Transaction
from trytond.wizard import Button, StateTransition, StateView, Wizard


class Invoice(metaclass=PoolMeta):
    __name__ = 'account.invoice'

    @classmethod
    def __setup__(cls):
        super(Invoice, cls).__setup__()
        cls._buttons.update({
            'pay_using_payment_transaction': {
                'invisible': Or(
                    Eval('state') != 'posted',
                    Eval('type') == 'in',
                ),
                'readonly': ~Eval('groups', []).contains(
                    Id('account', 'group_account')),
            },
        })
        cls.__rpc__.update({
            'capture_and_pay_using_transaction': RPC(
                readonly=False, instantiate=0
            ),
        })

    def capture_and_pay_using_transaction(self, profile_id, gateway_id, amount):
        """
        Create a payment transaction, capture paymnet and then pay using
        the transaction

        :param profile_id: Payment profile id
        :param gateway_id: Payment gateway id
        :param amount: Amount to be deducted
        """
        PaymentTransaction = Pool().get('payment_gateway.transaction')
        Date = Pool().get('ir.date')

        transaction = PaymentTransaction(
            party=self.party,
            credit_account=self.party.account_receivable_used,
            address=self.invoice_address,
            gateway=gateway_id,
            payment_profile=profile_id,
            amount=amount,
            currency=self.currency,
            description=self.description,
            date=Date.today(),
        )
        transaction.save()
        PaymentTransaction.capture([transaction])
        if transaction.state in ('completed', 'posted'):
            self.pay_using_transaction(transaction)
        else:
            self.raise_user_error('Payment capture failed')

    def pay_using_transaction(self, payment_transaction):
        """
        Pay an invoice using an existing payment_transaction

        :param payment_transaction: Active record of a payment transaction
        """
        Date = Pool().get('ir.date')
        AccountMoveLine = Pool().get('account.move.line')
        AccountConfiguration = Pool().get('account.configuration')

        config = AccountConfiguration(1)
        for line in payment_transaction.move.lines:
            if line.reconciliation:
                continue

            if line.account == self.account:
                if line not in self.payment_lines:
                    self.write([self], {
                            'payment_lines': [('add', [line.id])]
                            })
                if abs(self.amount_to_pay) <= config.write_off_threshold:
                    # Reconcile lines to pay and payment lines from transaction.
                    # Write-off is required to write-off the remaining balance.
                    # XXX Make missing write-off an UserError
                    if self.amount_to_pay != Decimal('0'):
                        write_off = config.write_off
                    else:
                        write_off = None
                    try:
                        AccountMoveLine.reconcile(
                            self.lines_to_pay + self.payment_lines,
                            writeoff=write_off,
                            date=Date.today(),
                            description=' / '.join([self.rec_name,
                                    payment_transaction.rec_name])
                            )
                    except UserError as e:
                        # If reconcilation fails, do not raise the error
                        pass
                return line

    @classmethod
    @ModelView.button_action(
        'invoice_payment_gateway.wizard_pay_using_transaction')
    def pay_using_payment_transaction(cls, invoices):  # pragma: no cover
        pass


class PayInvoiceUsingTransactionStart(BaseCreditCardViewMixin, ModelView):
    'Pay using Transaction Wizard'
    __name__ = 'account.invoice.pay_using_transaction.start'

    invoice = fields.Many2One(
        'account.invoice', 'Invoice', required=True, readonly=True
    )
    transaction_type = fields.Function(
        fields.Char("Transaction Type"), "on_change_with_transaction_type"
    )
    party = fields.Many2One('party.party', 'Party',
        readonly=True,
        context={
            'company': Eval('company', -1),
            },
    )
    gateway = fields.Many2One(
        'payment_gateway.gateway', 'Gateway', required=True,
        domain=[('users', '=', Eval('user'))],
    )
    method = fields.Function(
        fields.Char('Payment Gateway Method'), 'get_method'
    )
    use_existing_card = fields.Boolean(
        'Use existing Card?', states={
            'invisible': Eval('method') != 'credit_card'
        },
    )
    payment_profile = fields.Many2One(
        'party.payment_profile', 'Payment Profile',
        domain=[
            ('party', '=', Eval('party')),
            ('gateway', '=', Eval('gateway')),
        ],
        states={
            'required': And(
                Eval('method') == 'credit_card', Bool(Eval('use_existing_card'))
            ),
            'invisible': ~Bool(Eval('use_existing_card'))
        },
    )
    user = fields.Many2One(
        "res.user", "Tryton User", readonly=True
    )
    amount = Monetary(
        'Amount', currency='currency', digits='currency', required=True)
    currency = fields.Function(
        fields.Many2One('currency.currency', 'Currency'),
        'on_change_with_currency'
    )
    reference = fields.Char(
        'Reference', states={
            'invisible': Not(Eval('method') == 'manual'),
        }
    )

    company = fields.Many2One(
        'company.company', 'Company', readonly=True, required=True,
        domain=[
            ('id', If(Eval('context', {}).contains('company'), '=', '!='),
                Eval('context', {}).get('company', -1)),
        ],
    )
    credit_account = fields.Many2One(
        'account.account', 'Credit Account', required=True,
        domain=[
            ('company', '=', Eval('company', -1)),
            ('type.receivable', '=', True)
            ],
    )
    transaction = fields.Many2One(
        'payment_gateway.transaction', "Transaction", domain=[
            ('party', '=', Eval('party')),
            ('gateway', '=', Eval('gateway')),
        ],
        context={
            'company': Eval('company', -1),
            },
        states={
            'required': Eval('transaction_type') == 'refund',
            'invisible': Eval('transaction_type') != 'refund'
        },
    )

    @classmethod
    def __setup__(cls):
        super(PayInvoiceUsingTransactionStart, cls).__setup__()

        INV = Or(
            Eval('method') == 'manual',
            And(
                Eval('method') == 'credit_card',
                Bool(Eval('use_existing_card'))
            )
        )
        STATE1 = {
            'required': And(
                ~Bool(Eval('use_existing_card')),
                Eval('method') == 'credit_card',
                Eval('transaction_type') == 'charge',
            ),
            'invisible': INV
        }

        cls.owner.states.update(STATE1)
        cls.number.states.update(STATE1)
        cls.expiry_month.states.update(STATE1)
        cls.expiry_year.states.update(STATE1)
        cls.csc.states.update(STATE1)
        cls.swipe_data.states = {'invisible': INV}

    def get_method(self, name=None):  # pragma: no cover
        """
        Return the method based on the gateway
        """
        return self.gateway.method

    @fields.depends('gateway')
    def on_change_gateway(self):  # pragma: no cover
        if self.gateway:
            self.method = self.gateway.method or None

    @fields.depends('invoice')
    def on_change_with_transaction_type(self, name=None):
        "If the receivable today is positive, it's a charge else refund"
        if self.invoice:
            if self.invoice.amount_to_pay_today >= 0:
                return 'charge'
            else:
                return 'refund'

    @fields.depends('invoice', '_parent_invoice.currency')
    def on_change_with_currency(self, name=None):
        if self.invoice:
            return self.invoice.currency

    @classmethod
    def view_attributes(cls):
        return super().view_attributes() + [
            ('//group[@id="charge"]', 'states', {
                    'invisible': Eval('transaction_type') != 'charge',
                    }),
            ('//group[@id="refund"]', 'states', {
                    'invisible': Eval('transaction_type') != 'refund',
                    })]


class PayInvoiceUsingTransactionFailed(ModelView):
    'Pay using Transaction Wizard'
    __name__ = 'account.invoice.pay_using_transaction.failed'

    message = fields.Text("Message", readonly=True)


class PayInvoiceUsingTransaction(Wizard):
    'Pay using Transaction Wizard'
    __name__ = 'account.invoice.pay_using_transaction'

    start = StateView(
        'account.invoice.pay_using_transaction.start',
        'invoice_payment_gateway.pay_using_transaction_start_view_form', [
            Button('Cancel', 'end', 'tryton-cancel'),
            Button('Ok', 'pay', 'tryton-ok', default=True),
        ]
    )
    pay = StateTransition()
    failed = StateView(
        'account.invoice.pay_using_transaction.failed',
        'invoice_payment_gateway.pay_using_transaction_failed_view_form',
        [
            Button('Ok', 'end', 'tryton-ok'),
        ]
    )

    def default_start(self, field=None):
        pool = Pool()
        Invoice = pool.get('account.invoice')
        Party = pool.get('party.party')

        invoice = Invoice(Transaction().context.get('active_id'))

        if (invoice.amount_to_pay_today or invoice.amount_to_pay) >= 0:
            transaction_type = 'charge'
        else:
            transaction_type = 'refund'

        # Rebrowse the party with company context to get correct account data
        with Transaction().set_context(company=invoice.company.id):
            party = Party(invoice.party)
            receivable = party.account_receivable_used

        res = {
            'invoice': invoice.id,
            'company': invoice.company.id,
            'party': invoice.party.id,
            'credit_account': receivable,
            'owner': invoice.party.name,
            'currency': invoice.currency,
            'amount': abs(invoice.amount_to_pay_today or invoice.amount_to_pay),
            'user': Transaction().user,
            'transaction_type': transaction_type,
            }
        return res

    def create_payment_transaction(self, profile=None):
        """
        Helper function to create new payment transaction
        """
        PaymentTransaction = Pool().get('payment_gateway.transaction')
        Date = Pool().get('ir.date')

        return PaymentTransaction(
            origin='%s,%s' % (
                self.start.invoice.__name__, self.start.invoice.id),
            party=self.start.party,
            credit_account=self.start.credit_account,
            address=self.start.invoice.invoice_address,
            gateway=self.start.gateway,
            payment_profile=profile,
            amount=abs(self.start.amount),
            currency=self.start.invoice.currency,
            description=self.start.reference or None,
            date=Date.today(),
        )

    def create_payment_profile(self):
        """
        Helper function to create payment profile
        """
        Invoice = Pool().get('account.invoice')
        ProfileWizard = Pool().get(
            'party.party.payment_profile.add', type="wizard"
        )
        profile_wizard = ProfileWizard(
            ProfileWizard.create()[0]
        )
        profile_wizard.card_info.owner = self.start.owner
        profile_wizard.card_info.number = self.start.number
        profile_wizard.card_info.expiry_month = self.start.expiry_month
        profile_wizard.card_info.expiry_year = self.start.expiry_year
        profile_wizard.card_info.csc = self.start.csc or ''
        profile_wizard.card_info.gateway = self.start.gateway
        profile_wizard.card_info.address = Invoice(
            Transaction().context.get('active_id')
        ).invoice_address
        profile_wizard.card_info.party = self.start.party

        with Transaction().set_context(return_profile=True):
            profile = profile_wizard.transition_add()
        return profile

    def transition_pay(self):
        """
        Creates a new payment transaction and pay invoice with it
        """
        PaymentTransaction = Pool().get('payment_gateway.transaction')

        if self.start.transaction_type == 'charge':
            profile = self.start.payment_profile
            if self.start.method == 'credit_card' and (
                not self.start.use_existing_card
            ):
                profile = self.create_payment_profile()

            transaction = self.create_payment_transaction(profile=profile)
            transaction.save()

            # Capture Transaction
            PaymentTransaction.capture([transaction])
            if transaction.state in ('completed', 'posted'):
                # Pay invoice using above captured transaction
                self.start.invoice.pay_using_transaction(transaction)
            else:
                self.failed.message = \
                    "Payment capture failed, refer transaction logs"
                return 'failed'

        elif self.start.transaction_type == 'refund':
            refund_transaction = self.start.transaction.create_refund(
                self.start.amount
            )
            PaymentTransaction.refund([refund_transaction])
            if refund_transaction.state in ('completed', 'posted'):
                self.start.invoice.pay_using_transaction(refund_transaction)
            else:
                self.failed.message = \
                    "Payment refund failed, refer transaction logs"
                return 'failed'

        return 'end'

    def default_failed(self, data):  # pragma: nocover
        return {
            'message': self.failed.message,
        }


class PaymentTransaction(metaclass=PoolMeta):
    'Gateway Transaction'
    __name__ = 'payment_gateway.transaction'

    @classmethod
    def _get_origin(cls):
        'Add invoice to the selections'
        res = super(PaymentTransaction, cls)._get_origin()
        if 'account.invoice' not in res:
            res.append('account.invoice')
        return res


class AccountConfiguration(metaclass=PoolMeta):
    __name__ = 'account.configuration'

    write_off = fields.Many2One('account.move.reconcile.write_off',
        'Threshold Write Off')
    write_off_threshold = fields.Numeric('Writeoff Threshold', required=True)

    @staticmethod
    def default_write_off_threshold():
        return Decimal('0')
