# -*- coding: utf-8 -*-

from odoo import models, fields, api

class AccountPaymentGroupVencimiento(models.Model):
    _inherit = 'account.payment.group'

    cm_supplier_due_date = fields.Date(string='Fecha vencimiento pago')

