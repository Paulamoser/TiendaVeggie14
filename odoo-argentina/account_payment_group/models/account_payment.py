# © 2016 ADHOC SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

import logging
_logger = logging.getLogger(__name__)


class AccountPayment(models.Model):
    _inherit = "account.payment"

    move_id = fields.Many2one(
        comodel_name='account.move',
        string='Journal Entry', required=True, readonly=False, ondelete='cascade',
        check_company=True)

    payment_group_id = fields.Many2one(
        'account.payment.group',
        'Recibo',
        ondelete='cascade',
        readonly=True,
    )
    # we add this field so company can be send in context when adding payments
    # before payment group is saved
    payment_group_company_id = fields.Many2one(
        related='payment_group_id.company_id',
        string='Payment Group Company',
    )
    # we make a copy without transfer option, we try with related but it
    # does not works
    payment_type_copy = fields.Selection(
        selection=[('outbound', 'Send Money'), ('inbound', 'Receive Money')],
        compute='_compute_payment_type_copy',
        inverse='_inverse_payment_type_copy',
        string='Payment Type (without transfer)'
    )
    signed_amount = fields.Monetary(
        string='Monto',
        compute='_compute_signed_amount',
    )
    signed_amount_company_currency = fields.Monetary(
        string='Monto del Pago en la Moneda de la Empresa',
        compute='_compute_signed_amount',
        currency_field='company_currency_id',
    )
    amount_company_currency = fields.Monetary(
        string='Monto en la Moneda de la Empresa',
        compute='_compute_amount_company_currency',
        inverse='_inverse_amount_company_currency',
        currency_field='company_currency_id',
    )
    other_currency = fields.Boolean(
        compute='_compute_other_currency',
    )
    force_amount_company_currency = fields.Monetary(
        string='Monto Forzado en la Moneda de la Empresa',
        currency_field='company_currency_id',
        copy=False,
    )
    exchange_rate = fields.Float(
        string='Tipo de Cambio',
        #compute='_compute_exchange_rate',
        # readonly=False,
        # inverse='_inverse_exchange_rate',
        digits=(16, 4),
    )
    company_currency_id = fields.Many2one(
        related='company_id.currency_id',
        string='Company currency',
    )

    def _seek_for_lines(self):
        ''' Helper used to dispatch the journal items between:
        - The lines using the temporary liquidity account.
        - The lines using the counterpart account.
        - The lines being the write-off lines.
        :return: (liquidity_lines, counterpart_lines, writeoff_lines)
        '''
        self.ensure_one()

        liquidity_lines = self.env['account.move.line']
        counterpart_lines = self.env['account.move.line']
        writeoff_lines = self.env['account.move.line']

        for line in self.move_id.line_ids:
            if line.account_id in (
                    self.journal_id.default_account_id,
                    self.journal_id.payment_debit_account_id,
                    self.journal_id.payment_credit_account_id,
            ):
                if len(liquidity_lines) != 1:
                    liquidity_lines += line
            elif line.account_id.internal_type in ('receivable', 'payable') or line.partner_id == line.company_id.partner_id:
                if len(counterpart_lines) != 1:
                    counterpart_lines += line
            else:
                writeoff_lines += line

        return liquidity_lines, counterpart_lines, writeoff_lines

    @api.model_create_multi
    def create(self, vals_list):
        _logger.info('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        # OVERRIDE
        write_off_line_vals_list = []

        for vals in vals_list:

            # Hack to add a custom write-off line.
            write_off_line_vals_list.append(vals.pop('write_off_line_vals', None))

            # Force the move_type to avoid inconsistency with residual 'default_move_type' inside the context.
            vals['move_type'] = 'entry'

            # Force the computation of 'journal_id' since this field is set on account.move but must have the
            # bank/cash type.
            if 'journal_id' not in vals:
                vals['journal_id'] = self._get_default_journal().id

            # Since 'currency_id' is a computed editable field, it will be computed later.
            # Prevent the account.move to call the _get_default_currency method that could raise
            # the 'Please define an accounting miscellaneous journal in your company' error.
            if 'currency_id' not in vals:
                journal = self.env['account.journal'].browse(vals['journal_id'])
                vals['currency_id'] = journal.currency_id.id or journal.company_id.currency_id.id

        payments = super().create(vals_list)

        for i, pay in enumerate(payments):
            write_off_line_vals = write_off_line_vals_list[i]

            # Write payment_id on the journal entry plus the fields being stored in both models but having the same
            # name, e.g. partner_bank_id. The ORM is currently not able to perform such synchronization and make things
            # more difficult by creating related fields on the fly to handle the _inherits.
            # Then, when partner_bank_id is in vals, the key is consumed by account.payment but is never written on
            # account.move.
            to_write = {'payment_id': pay.id}
            for k, v in vals_list[i].items():
                if k in self._fields and self._fields[k].store and k in pay.move_id._fields and pay.move_id._fields[k].store:
                    to_write[k] = v

            if 'line_ids' not in vals_list[i]:
                _logger.info('>>>> LINES')
                _logger.info(line_vals)
                to_write['line_ids'] = [(0, 0, line_vals) for line_vals in pay._prepare_move_line_default_vals(write_off_line_vals=write_off_line_vals)]

            pay.move_id.write(to_write)

        return payments

    @api.depends('amount', 'payment_type', 'partner_type', 'amount_company_currency')
    def _compute_signed_amount(self):
        for rec in self:
            sign = 1.0
            if (
                    (rec.partner_type == 'supplier' and
                        rec.payment_type == 'inbound') or
                    (rec.partner_type == 'customer' and
                        rec.payment_type == 'outbound')):
                sign = -1.0
            rec.signed_amount = rec.amount and rec.amount * sign
            rec.signed_amount_company_currency = (
                rec.amount_company_currency and
                rec.amount_company_currency * sign)

    # TODO check why we get error with depend on company_id and fix it
    # (recursive dependency?). The error is on paymentrs tree/form view
    # @api.depends('currency_id', 'company_id')
    @api.depends('currency_id')
    def _compute_other_currency(self):
        for rec in self:
            rec.other_currency = False
            if rec.company_currency_id and rec.currency_id and \
               rec.company_currency_id != rec.currency_id:
                rec.other_currency = True

    @api.depends('amount', 'other_currency', 'amount_company_currency')
    def _compute_exchange_rate(self):
        for rec in self.filtered('other_currency'):
            rec.exchange_rate = rec.amount and (
                rec.amount_company_currency / rec.amount) or 0.0

    # this onchange is necesary because odoo, sometimes, re-compute
    # and overwrites amount_company_currency. That happends due to an issue
    # with rounding of amount field (amount field is not change but due to
    # rouding odoo believes amount has changed)
    @api.onchange('amount_company_currency')
    def _inverse_amount_company_currency(self):
        for rec in self:
            if rec.other_currency and rec.amount_company_currency != \
                    rec.currency_id._convert(
                        rec.amount, rec.company_id.currency_id,
                        rec.company_id, rec.payment_date):
                force_amount_company_currency = rec.amount_company_currency
            else:
                force_amount_company_currency = False
            rec.force_amount_company_currency = force_amount_company_currency

    @api.depends('amount', 'other_currency', 'force_amount_company_currency')
    def _compute_amount_company_currency(self):
        """
        * Si las monedas son iguales devuelve 1
        * si no, si hay force_amount_company_currency, devuelve ese valor
        * sino, devuelve el amount convertido a la moneda de la cia
        """
        for rec in self:
            if not rec.other_currency:
                amount_company_currency = rec.amount
            elif rec.force_amount_company_currency:
                amount_company_currency = rec.force_amount_company_currency
            else:
                amount_company_currency = rec.currency_id._convert(
                    rec.amount, rec.company_id.currency_id,
                    rec.company_id, rec.payment_date)
            rec.amount_company_currency = amount_company_currency

    @api.onchange('payment_type_copy')
    def _inverse_payment_type_copy(self):
        for rec in self:
            # if false, then it is a transfer
            rec.payment_type = (
                rec.payment_type_copy and rec.payment_type_copy or 'transfer')

    @api.depends('payment_type')
    def _compute_payment_type_copy(self):
        for rec in self:
            if rec.payment_type == 'transfer':
                continue
            rec.payment_type_copy = rec.payment_type

    def get_journals_domain(self):
        domain = super(AccountPayment, self).get_journals_domain()
        if self.payment_group_company_id:
            domain.append(
                ('company_id', '=', self.payment_group_company_id.id))
        return domain

    @api.onchange('payment_type')
    def _onchange_payment_type(self):
        """
        we disable change of partner_type if we came from a payment_group
        but we still reset the journal
        """
        if not self._context.get('payment_group'):
            return super(AccountPayment, self)._onchange_payment_type()
        self.journal_id = False

    @api.constrains('payment_group_id', 'payment_type')
    def check_payment_group(self):
        # odoo tests don't create payments with payment gorups
        if self.env.registry.in_test_mode():
            return True
        for rec in self:
            receivable_payable = all([
                x['move_line'].account_id.internal_type in [
                    'receivable', 'payable']
                for x in self._context.get('counterpart_aml_dicts', [])])
            if rec.partner_type and rec.partner_id and receivable_payable and \
               not rec.payment_group_id:
                raise ValidationError(_(
                    'Payments with partners must be created from '
                    'payments groups'))
            # transfers or payments from bank reconciliation without partners
            elif not rec.partner_type and rec.payment_group_id:
                raise ValidationError(_(
                    "Payments without partners (usually transfers) cant't "
                    "have a related payment group"))

    @api.model
    def get_amls(self):
        """ Review parameters of process_reconciliation() method and transform
        them to amls recordset. this one is return to recompute the payment
        values
         context keys(
            'counterpart_aml_dicts', 'new_aml_dicts', 'payment_aml_rec')
         :return: account move line recorset
        """
        counterpart_aml_data = self._context.get('counterpart_aml_dicts', [])
        new_aml_data = self._context.get('new_aml_dicts', [])
        amls = self.env['account.move.line']
        if counterpart_aml_data:
            for item in counterpart_aml_data:
                amls |= item.get(
                    'move_line', self.env['account.move.line'])
        if new_aml_data:
            for aml_values in new_aml_data:
                amls |= amls.new(aml_values)
        return amls

    @api.model
    def infer_partner_info(self, vals):
        """ Odoo way to to interpret the partner_id, partner_type is not
        usefull for us because in some time they leave this ones empty and
        we need them in order to create the payment group.

        In this method will try to improve infer when it has a debt related
        taking into account the account type of the line to concile, and
        computing the partner if this ones is not setted when concile
        operation.

        return dictionary with keys (partner_id, partner_type)
        """
        res = {}
        # Get related amls
        amls = self.get_amls()
        if not amls:
            return res
        _logger.info('> AMLS')
        _logger.info(amls)

        # odoo manda partner type segun si el pago es positivo o no, nosotros
        # mejoramos infiriendo a partir de que tipo de deuda se esta pagando
        partner_type = False
        internal_type = amls.mapped('account_id.internal_type')
        if len(internal_type) == 1:
            if internal_type == ['payable']:
                partner_type = 'supplier'
            elif internal_type == ['receivable']:
                partner_type = 'customer'
            if partner_type:
                res.update({'partner_type': partner_type})

        # por mas que el usuario no haya selecccionado partner, si esta pagando
        # deuda usamos el partner de esa deuda
        partner_id = vals.get('partner_id', False)
        if not partner_id and len(amls.mapped('partner_id')) == 1:
            partner_id = amls.mapped('partner_id').id
            res.update({'partner_id': partner_id})

        return res

    @api.model
    def create(self, vals):
        """ When payments are created from bank reconciliation create the
        Payment group before creating payment to avoid raising error, only
        apply when the all the counterpart account are receivable/payable """
        # Si viene counterpart_aml entonces estamos viniendo de una
        # conciliacion desde el wizard
        new_aml_dicts = self._context.get('new_aml_dicts', [])
        counterpart_aml_data = self._context.get('counterpart_aml_dicts', [])
        if counterpart_aml_data or new_aml_dicts:
            vals.update(self.infer_partner_info(vals))

        create_from_statement = self._context.get(
            'create_from_statement', False) and vals.get('partner_type') \
            and vals.get('partner_id') and all([
                x['move_line'].account_id.internal_type in [
                    'receivable', 'payable']
                for x in counterpart_aml_data])
        create_from_expense = self._context.get('create_from_expense', False)
        create_from_website = self._context.get('create_from_website', False)
        # NOTE: This is required at least from POS when we do not have
        # partner_id and we do not want a payment group in tha case.
        create_payment_group = \
            create_from_statement or create_from_website or create_from_expense
        if create_payment_group:
            company_id = self.env['account.journal'].browse(
                vals.get('journal_id')).company_id.id
            payment_group = self.env['account.payment.group'].create({
                'company_id': company_id,
                'partner_type': vals.get('partner_type'),
                'partner_id': vals.get('partner_id'),
                'payment_date': vals.get('date', fields.Date.context_today(self)),
                'communication': vals.get('communication'),
            })
            vals['payment_group_id'] = payment_group.id
        payment = super(AccountPayment, self).create(vals)
        if create_payment_group:
            payment.payment_group_id.post()
        return payment

    @api.depends('invoice_line_ids', 'payment_type', 'partner_type', 'partner_id')
    def _compute_destination_account_id(self):
        """
        If we are paying a payment gorup with paylines, we use account
        of lines that are going to be paid
        """
        for rec in self:
            to_pay_account = rec.payment_group_id.to_pay_move_line_ids.mapped(
                'account_id')
            if len(to_pay_account) > 1:
                raise ValidationError(_(
                    'To Pay Lines must be of the same account!'))
            elif len(to_pay_account) == 1:
                rec.destination_account_id = to_pay_account[0]
            else:
                super(AccountPayment, rec)._compute_destination_account_id()

    def show_details(self):
        """
        Metodo para mostrar form editable de payment, principalmente para ser
        usado cuando hacemos ajustes y el payment group esta confirmado pero
        queremos editar una linea
        """
        return {
            'name': _('Payment Lines'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'account.payment',
            'target': 'new',
            'res_id': self.id,
            'context': self._context,
        }

    def _get_shared_move_line_vals(
            self, debit, credit, amount_currency, move_id, invoice_id=False):
        """
        Si se esta forzando importe en moneda de cia, usamos este importe
        para debito/credito
        """
        res = super(AccountPayment, self)._get_shared_move_line_vals(
            debit, credit, amount_currency, move_id, invoice_id=invoice_id)
        if self.force_amount_company_currency:
            if res.get('debit', False):
                res['debit'] = self.force_amount_company_currency
            if res.get('credit', False):
                res['credit'] = self.force_amount_company_currency
        return res

    def _get_move_vals(self, journal=None):
        """If we have a communication on payment group append it before
        payment communication
        """
        vals = super(AccountPayment, self)._get_move_vals(journal=journal)
        if self.payment_group_id.communication:
            vals['ref'] = "%s%s" % (
                self.payment_group_id.communication,
                self.communication and ": %s" % self.communication or "")
        return vals


    def _prepare_payment_moves(self):
        res = super(AccountPayment, self)._prepare_payment_moves()
        #for i,rec in enumerate(self):
        #    if rec.signed_amount_company_currency != line.credit:
        for i,rec in enumerate(self):
            if rec.currency_id.id != rec.company_id.currency_id.id and rec.payment_type == 'inbound':
                amount_debit = res[i]['line_ids'][0][2]['debit']
                amount_credit = res[i]['line_ids'][0][2]['credit']
                if amount_credit > 0 and rec.signed_amount_company_currency != amount_credit:
                    #raise ValidationError('estamos aca %s %s'%(amount_credit,res[0]['line_ids'][0][2]))
                    res[i]['line_ids'][0][2]['credit'] = rec.signed_amount_company_currency
                amount_debit = res[i]['line_ids'][1][2]['debit']
                amount_credit = res[i]['line_ids'][1][2]['credit']
                if amount_debit > 0 and rec.signed_amount_company_currency != amount_debit:
                    #raise ValidationError('estamos aca %s %s'%(amount_credit,res[0]['line_ids'][0][2]))
                    res[i]['line_ids'][1][2]['debit'] = rec.signed_amount_company_currency
        return res
