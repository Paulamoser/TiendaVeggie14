# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import models, fields, api, _
from odoo.exceptions import Warning, ValidationError
import time
import logging
_logger = logging.getLogger(__name__)

class account_vat_ledger(models.Model):

    _name = "account.vat.ledger"
    _description = "Account VAT Ledger"
    _inherit = ['mail.thread']
    _order = 'date_from desc'

    company_id = fields.Many2one(
        'res.company',
        string='Empresa',
        required=True,
        readonly=True,
        states={'draft': [('readonly', False)]},
        default=lambda self: self.env[
            'res.company']._company_default_get('account.vat.ledger')
    )
    type = fields.Selection(
        [('sale', 'Sale'), ('purchase', 'Purchase')],
        "Type",
        required=True
    )
    date_from = fields.Date(
        string='Fecha Desde',
        required=True,
        readonly=True,
        states={'draft': [('readonly', False)]},
    )
    date_to = fields.Date(
        string='Fecha Hasta',
        required=True,
        readonly=True,
        states={'draft': [('readonly', False)]},
    )

    #@api.onchange('date_range_id')
    #def onchange_date_range_id(self):
    #    if self.date_range_id:
    #        self.date_from = self.date_range_id.date_start
    #        self.date_to = self.date_range_id.date_end
    #    else:
    #        self.date_from = self.date_to = None
    # period_id = fields.Many2one(
    #     'account.period', 'Period', required=True,
    #     readonly=True, states={'draft': [('readonly', False)]},)
    journal_ids = fields.Many2many(
        'account.journal', 'account_vat_ledger_journal_rel',
        'vat_ledger_id', 'journal_id',
        string='Diarios',
        required=True,
        readonly=True,
        states={'draft': [('readonly', False)]},
    )
    #first_page = fields.Integer(
    #    "First Page",
    #    required=True,
    #    readonly=True,
    #    states={'draft': [('readonly', False)]},
    #)
    #last_page = fields.Integer(
    #    "Last Page",
    #    readonly=True,
    #    states={'draft': [('readonly', False)]},
    #)
    presented_ledger = fields.Binary(
        "Presented Ledger",
        readonly=True,
        states={'draft': [('readonly', False)]},
    )
    presented_ledger_name = fields.Char(
    )
    state = fields.Selection(
        [('draft', 'Borrador'), ('presented', 'Presentado'), ('cancel', 'Cancelado')],
        'State',
        required=True,
        default='draft'
    )
    note = fields.Html(
        "Notas"
    )
# Computed fields
    name = fields.Char(
        'Nombre',
        compute='_get_name'
    )
    reference = fields.Char(
        'Referencia',
    )
    invoice_ids = fields.Many2many(
        'account.move',
        string="Facturas",
        compute="_get_data"
    )
    #document_type_ids = fields.Many2many(
    #    'account.document.type',
    #    string="Document Classes",
    #    compute="_get_data"
    #)
    #vat_tax_ids = fields.Many2many(
    #    'account.tax',
    #    string="VAT Taxes",
    #    compute="_get_data"
    #)
    #other_tax_ids = fields.Many2many(
    #    'account.tax',
    #    string="Other Taxes",
    #    compute="_get_data"
    #)
    # vat_tax_code_ids = fields.Many2many(
    #     'account.tax.code',
    #     string="VAT Tax Codes",
    #     compute="_get_data"
    # )
    # other_tax_code_ids = fields.Many2many(
    #     'account.tax.code',
    #     string="Other Tax Codes",
    #     compute="_get_data"
    # )
    #afip_responsability_type_ids = fields.Many2many(
    #    'l10nafip.responsability.type',
    #    string="AFIP Responsabilities",
    #    compute="_get_data"
    #)

    # Sacamos el depends por un error con el cache en esqume multi cia al
    # cambiar periodo de una cia hija con usuario distinto a admin
    # @api.depends('journal_ids', 'period_id')
    def _get_data(self):
        #self.afip_responsability_type_ids = self.env[
        #    'l10n_ar.afip.responsibility.type'].search([])

        if self.type == 'sale':
            invoices_domain = [
                # cancel invoices with internal number are invoices
                ('state', '!=', 'draft'),
                ('document_number', '!=', False),
                #('internal_number', '!=', False),
                ('journal_id', 'in', self.journal_ids.ids),
                ('date', '>=', self.date_from),
                ('date', '<=', self.date_to),
            ]
            invoices = self.env['account.move'].search(
                # TODO, tal vez directamente podemos invertir el orden, como?
                invoices_domain,
                order='invoice_date asc, document_number asc, id asc')
        else:
            invoices_domain = [
                # cancel invoices with internal number are invoices
                ('state', '!=', 'draft'),
                ('name', '!=', False),
                # ('internal_number', '!=', False),
                ('journal_id', 'in', self.journal_ids.ids),
                ('date', '>=', self.date_from),
                ('date', '<=', self.date_to),
            ]
            invoices = self.env['account.move'].search(
                # TODO, tal vez directamente podemos invertir el orden, como?
                invoices_domain,
                order='invoice_date asc, name asc, id asc')


        #self.document_type_ids = invoices.mapped('l10n_latam_document_type_id')
        self.invoice_ids = invoices

        #self.vat_tax_ids = invoices.mapped(
        #    'vat_tax_ids.tax_id')
        #self.other_tax_ids = invoices.mapped(
        #    'not_vat_tax_ids.tax_id')
        # self.vat_tax_code_ids = invoices.mapped(
        #     'vat_tax_ids.tax_code_id')
        # self.other_tax_code_ids = invoices.mapped(
        #     'not_vat_tax_ids.tax_code_id')

    def _get_name(self):
        for rec in self:
            if rec.type == 'sale':
                ledger_type = _('Ventas')
            elif rec.type == 'purchase':
                ledger_type = _('Compras')

            lang = self.env['res.lang']
            #date_format = lang.browse(lang._lang_get(
            #    self._context.get('lang', 'en_US'))).date_format

            name = _("%s Libro de IVA %s - %s") % (
                ledger_type,
                rec.date_from and fields.Date.from_string(
                    rec.date_from).strftime("%d-%m-%Y") or '',
                rec.date_to and fields.Date.from_string(
                    rec.date_to).strftime("%d-%m-%Y") or '',
            )
            if rec.reference:
                name = "%s - %s" % (name, rec.reference)
            rec.name = name

    @api.onchange('company_id')
    def change_company(self):
        now = time.strftime('%Y-%m-%d')
        company_id = self.company_id.id
        domain = [('company_id', '=', company_id),
                  ('date_start', '<', now), ('date_stop', '>', now)]
        # fiscalyears = self.env['account.fiscalyear'].search(domain, limit=1)
        # self.fiscalyear_id = fiscalyears
        if self.type == 'sale':
            domain = [('type', '=', 'sale')]
        elif self.type == 'purchase':
            domain = [('type', '=', 'purchase')]
        domain += [
            ('l10n_latam_use_documents', '=', True),
            ('company_id', '=', self.company_id.id),
        ]
        journals = self.env['account.journal'].search(domain)
        self.journal_ids = journals

    def action_present(self):
        if not self.invoice_ids:
            raise ValidationError('??Est?? intentando presentar un Libro IVA sin Facturas!')
        self.state = 'presented'

    def action_cancel(self):
        self.state = 'cancel'

    def action_to_draft(self):
        self.state = 'draft'
