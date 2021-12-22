from odoo import models, api, fields, _
from odoo.exceptions import ValidationError
_logger = logging.getLogger(__name__)

class AccountMove(models.Model):
    _inherit = "account.move"


    def action_post(self):
        _logger.info('antes post')
        res = super(AccountMove, self).action_post()
        _logger.info('despues post')
        self.pay_now()
        _logger.info('despues pay ')
        return res
