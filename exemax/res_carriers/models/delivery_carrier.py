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
    razon_social = fields.Char('Razón Social')
    direccion = fields.Char('Dirección')
    ciudad = fields.Char('Ciudad')
    telefono = fields.Char('Teléfono')
    movil = fields.Char('Móvil')
    email =fields.Char('Correo electrónico')
    active = fields.Boolean(default=True)
    sequence = fields.Integer(help="Determine the display order", default=10)

    country_ids = fields.Many2many('res.country', 'delivery_carrier_country_rel', 'carrier_id', 'country_id', 'Countries')
    state_ids = fields.Many2many('res.country.state', 'delivery_carrier_state_rel', 'carrier_id', 'state_id', 'States')