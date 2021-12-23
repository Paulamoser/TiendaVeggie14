from odoo import fields, models, api
# from odoo.exceptions import ValidationError
import logging
_logger = logging.getLogger(__name__)


class AccountPaymentGroup(models.Model):
    _inherit = "account.payment.group"


    def post(self):
        #self = self.with_context({})
        for rec in self:
            if rec.payment_ids:
                for payment in rec.payment_ids:
                    payment.name=''
        vals = super(AccountPaymentGroup, self).post()

