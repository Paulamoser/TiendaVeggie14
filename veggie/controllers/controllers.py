# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request
from odoo.addons.website_form.controllers.main import WebsiteForm
import logging
import base64
import json
import pytz

from datetime import datetime
from psycopg2 import IntegrityError
from werkzeug.exceptions import BadRequest

_logger = logging.getLogger(__name__)

class WebsiteForm(WebsiteForm):

    def _handle_website_form(self, model_name, **kwargs):
        email = request.params.get('partner_email')
        if email:
            partner = request.env['res.partner'].sudo().search([('email', '=', email)], limit=1)
            if not partner:
                partner = request.env['res.partner'].sudo().create({
                    'email': email,
                    'name': request.params.get('partner_name', False)
                })
            request.params['partner_id'] = partner.id
            request.params['business_name'] = request.params.get('business_name')
            request.params['address'] = request.params.get('address')
            request.params['resolution_type'] = request.params.get('resolution_type')
            request.params['business'] = request.params.get('business')
            request.params['claim'] = request.params.get('claim')

        return super(WebsiteForm, self)._handle_website_form(model_name, **kwargs)