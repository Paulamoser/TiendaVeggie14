# -*- coding: utf-8 -*-
 
from odoo import models, fields, api, exceptions, _
 
class AccountWizard(models.TransientModel):
    _name = 'ati.account.wizard'
 
 
    start_date = fields.Date("Start Date")
    end_date = fields.Date("End Date")
 
 
    def get_excel_report(self):
        # redirect to /sale/excel_report controller to generate the excel file
        return {
            'type': 'ir.actions.act_url',
            'url': '/account/account_mix_report/%s' % (self.id),
            'target': 'new',
        }