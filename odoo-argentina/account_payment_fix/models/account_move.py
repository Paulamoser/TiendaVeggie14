
from odoo import models, api, fields, _
from odoo.exceptions import ValidationError

class AccountMove(models.Model):
    _inherit = "account.move"

@api.depends('payment_move_line_ids')
def _compute_payment_groups(self):
    for rec in self:
        rec.payment_group_ids = rec.payment_move_line_ids.mapped(
            'payment_id.payment_group_id')