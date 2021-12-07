# -*- coding: utf-8 -*-

import logging
import psycopg2

from odoo import api, fields, models, registry, SUPERUSER_ID, _

_logger = logging.getLogger(__name__)


class res_Carrier(models.Model):
    _name = 'res.carrier'
    _description = "Expresos"
    _order = 'sequence, id'

    name = fields.Char('Expreso', required=True, translate=True)
    active = fields.Boolean(default=True)
    sequence = fields.Integer(help="Determine the display order", default=10)

