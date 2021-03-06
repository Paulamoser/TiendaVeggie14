# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)

class StockPicking(models.Model):
    _inherit = "stock.picking"

    frozen_roadmap = fields.Boolean(string="P.C.", default=False, index=True)
    refrigerated_roadmap = fields.Boolean(string="P.R.", default=False, index=True)
    dry_roadmap = fields.Boolean(string="P.S.", default=False, index=True)

    order = fields.Integer('Orden')
    rute = fields.Char('Ruta')

    total_weight = fields.Float('Peso Total',compute='_compute_total_weight')
    total_volume = fields.Float('Volumen Total',compute='_compute_total_volume')

    def _compute_total_weight(self):
        for rec in self:
            tw=0
            for line in rec.move_ids_without_package:
                tw+=line.product_uom_qty*line.product_id.weight
            rec.total_weight=tw

    def _compute_total_volume(self):
        for rec in self:
            tv=0
            for line in rec.move_ids_without_package:
                tv+=line.product_uom_qty*line.product_id.volume
            rec.total_volume=tv

class SaleAdvancePaymentInv(models.Model):
    _inherit = "sale.order"

    invoicing = fields.Boolean(default=False, string="Factura", index=True)

    def action_clear(self):
        for rec in self:
            rec.write({'order_line': [(5, 0, 0)]})

    def get_deuda_total(self, partner):
        orders = self.search([
                ('partner_id', '=', partner.id),
                ('state', 'in', ['draft','sent'])
            ])
        deuda = 0
        for o in orders:
            deuda += o.amount_total
        return deuda

    def in_caba(self, partner):
        _logger.info("\n\n\n deuda: {} \n\n\n".format(partner.state_id))
        if partner.state_id.id in [
            self.env.ref("base.state_ar_c").id, 
            self.env.ref("base.state_ar_b").id]:
            return True
        else:
            return False
    
    def _prepare_invoice(self):
        """
        Prepare the dict of values to create the new invoice for a sales order. This method may be
        overridden to implement custom invoice generation (making sure to call super() to establish
        a clean extension chain).
        """
        self.ensure_one()
        if self.invoicing == False:
            journal = self.env['account.journal'].sudo().search([('invoicing', '=', True)])
        else:
            journal = self.env['account.move'].with_context(default_move_type='out_invoice')._get_default_journal()
        if not journal:
            raise UserError(_('Please define an accounting sales journal for the company %s (%s).') % (self.company_id.name, self.company_id.id))

        invoice_vals = {
            'ref': self.client_order_ref or '',
            'move_type': 'out_invoice',
            'narration': self.note,
            'currency_id': self.pricelist_id.currency_id.id,
            'campaign_id': self.campaign_id.id,
            'medium_id': self.medium_id.id,
            'source_id': self.source_id.id,
            'user_id': self.user_id.id,
            'invoice_user_id': self.user_id.id,
            'team_id': self.team_id.id,
            'partner_id': self.partner_invoice_id.id,
            'partner_shipping_id': self.partner_shipping_id.id,
            'fiscal_position_id': (self.fiscal_position_id or self.fiscal_position_id.get_fiscal_position(self.partner_invoice_id.id)).id,
            'partner_bank_id': self.company_id.partner_id.bank_ids[:1].id,
            'journal_id': journal.id,  # company comes from the journal
            'invoice_origin': self.name,
            'invoice_payment_term_id': self.payment_term_id.id,
            'payment_reference': self.reference,
            'transaction_ids': [(6, 0, self.transaction_ids.ids)],
            'invoice_line_ids': [],
            'company_id': self.company_id.id,
        }
        return invoice_vals


    def _create_invoices(self, grouped=False, final=False, date=None):
        """
        Create the invoice associated to the SO.
        :param grouped: if True, invoices are grouped by SO id. If False, invoices are grouped by
                        (partner_invoice_id, currency)
        :param final: if True, refunds will be generated if necessary
        :returns: list of created invoices
        """
        grouped = True
        if not self.env['account.move'].check_access_rights('create', False):
            try:
                self.check_access_rights('write')
                self.check_access_rule('write')
            except AccessError:
                return self.env['account.move']

        # 1) Create invoices.
        invoice_vals_list = []
        invoice_item_sequence = 0 # Incremental sequencing to keep the lines order on the invoice.
        for order in self:
            order = order.with_company(order.company_id)
            current_section_vals = None
            down_payments = order.env['sale.order.line']

            invoice_vals = order._prepare_invoice()
            invoiceable_lines = order._get_invoiceable_lines(final)

            if not any(not line.display_type for line in invoiceable_lines):
                continue

            invoice_line_vals = []
            down_payment_section_added = False
            for line in invoiceable_lines:
                if not down_payment_section_added and line.is_downpayment:
                    # Create a dedicated section for the down payments
                    # (put at the end of the invoiceable_lines)
                    invoice_line_vals.append(
                        (0, 0, order._prepare_down_payment_section_line(
                            sequence=invoice_item_sequence,
                        )),
                    )
                    down_payment_section_added = True
                    invoice_item_sequence += 1
                invoice_line_vals.append(
                    (0, 0, line._prepare_invoice_line(
                        sequence=invoice_item_sequence,
                    )),
                )
                invoice_item_sequence += 1

            invoice_vals['invoice_line_ids'] += invoice_line_vals
            invoice_vals_list.append(invoice_vals)

        if not invoice_vals_list:
            raise self._nothing_to_invoice_error()

        # 2) Manage 'grouped' parameter: group by (partner_id, currency_id).
        if not grouped:
            new_invoice_vals_list = []
            invoice_grouping_keys = self._get_invoice_grouping_keys()
            invoice_vals_list = sorted(invoice_vals_list, key=lambda x: [x.get(grouping_key) for grouping_key in invoice_grouping_keys])
            for grouping_keys, invoices in groupby(invoice_vals_list, key=lambda x: [x.get(grouping_key) for grouping_key in invoice_grouping_keys]):
                origins = set()
                payment_refs = set()
                refs = set()
                ref_invoice_vals = None
                for invoice_vals in invoices:
                    if not ref_invoice_vals:
                        ref_invoice_vals = invoice_vals
                    else:
                        ref_invoice_vals['invoice_line_ids'] += invoice_vals['invoice_line_ids']
                    origins.add(invoice_vals['invoice_origin'])
                    payment_refs.add(invoice_vals['payment_reference'])
                    refs.add(invoice_vals['ref'])
                ref_invoice_vals.update({
                    'ref': ', '.join(refs)[:2000],
                    'invoice_origin': ', '.join(origins),
                    'payment_reference': len(payment_refs) == 1 and payment_refs.pop() or False,
                })
                new_invoice_vals_list.append(ref_invoice_vals)
            invoice_vals_list = new_invoice_vals_list

        # 3) Create invoices.

        # As part of the invoice creation, we make sure the sequence of multiple SO do not interfere
        # in a single invoice. Example:
        # SO 1:
        # - Section A (sequence: 10)
        # - Product A (sequence: 11)
        # SO 2:
        # - Section B (sequence: 10)
        # - Product B (sequence: 11)
        #
        # If SO 1 & 2 are grouped in the same invoice, the result will be:
        # - Section A (sequence: 10)
        # - Section B (sequence: 10)
        # - Product A (sequence: 11)
        # - Product B (sequence: 11)
        #
        # Resequencing should be safe, however we resequence only if there are less invoices than
        # orders, meaning a grouping might have been done. This could also mean that only a part
        # of the selected SO are invoiceable, but resequencing in this case shouldn't be an issue.
        if len(invoice_vals_list) < len(self):
            SaleOrderLine = self.env['sale.order.line']
            for invoice in invoice_vals_list:
                sequence = 1
                for line in invoice['invoice_line_ids']:
                    line[2]['sequence'] = SaleOrderLine._get_invoice_line_sequence(new=sequence, old=line[2]['sequence'])
                    sequence += 1

        # Manage the creation of invoices in sudo because a salesperson must be able to generate an invoice from a
        # sale order without "billing" access rights. However, he should not be able to create an invoice from scratch.
        moves = self.env['account.move'].sudo().with_context(default_move_type='out_invoice').create(invoice_vals_list)

        # 4) Some moves might actually be refunds: convert them if the total amount is negative
        # We do this after the moves have been created since we need taxes, etc. to know if the total
        # is actually negative or not
        if final:
            moves.sudo().filtered(lambda m: m.amount_total < 0).action_switch_invoice_into_refund_credit_note()
        for move in moves:
            move.message_post_with_view('mail.message_origin_link',
                values={'self': move, 'origin': move.line_ids.mapped('sale_line_ids.order_id')},
                subtype_id=self.env.ref('mail.mt_note').id
            )
        return moves

class ProductCategory(models.Model):
    _inherit ="product.category"

    order_report = fields.Integer('Orden en el reporte', store=True)

class ProductProduct(models.Model):
    _inherit ="product.product"
    
    order_report = fields.Integer('Orden en el reporte', store=True)

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    product_liqui = fields.Boolean('??Es Liquidaci??n?')
    product_new = fields.Boolean('??Es Nuevo Ingreso?')
    product_featured = fields.Boolean('??Es Destacado?')

class AccountJournal(models.Model):
    _inherit ='account.journal'

    invoicing = fields.Boolean(default=False, string="Testing", index=True)

class AccountMove(models.Model):
    _inherit ='account.move'

    state_id = fields.Char(string='Provincia', store=True, related='partner_id.state_id.name')
    city = fields.Char(string='Ciudad', store=True, related='partner_id.city')

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    def action_clear(self):
        for rec in self:
            rec.write({'order_line': [(5, 0, 0)]})


#class HelpdeskTicket(models.Model):
#    _inherit = 'helpdesk.ticket'

#    resolution_type = fields.Selection([ ('nc', 'Nota de Cr??dito'),('rm', 'Recambio de Mercader??a'),('prov', 'Comunicado al Proveedor') ],'Tipo de Resoluci??n')
#    order_delivery_date = fields.Date(required=True, default=fields.Date.context_today)
#    business_name = fields.Char(string="Nombre del Comercio")
#    business = fields.Selection([ ('diet', 'Diet??tica'),('expr', 'Diet??tica con env??o en Expreso')],'Tipo de Comercio')
#    address = fields.Text(string='Direcci??n (Calle, Altura y Localidad)')
#    invoice_number = fields.Char(string="N??mero de Factura")
#    claim = fields.Selection([ ('fc', 'Factura'),('falt', 'Faltante'),('prob', 'Problema con producto'), ('otr', 'Otros (Colocar detalle en la descripci??n)')],'Reclamo')