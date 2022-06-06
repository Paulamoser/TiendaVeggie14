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

    @http.route(['/get_products/ingresos'], type='json', auth="public", website=True)
    def get_products_ingresos(self):
        products = http.request.env['product.template'].sudo().search([('website_published','=',True),('product_new','=',True)], limit=6, order='website_sequence asc')
        pricelist = http.request.env['product.pricelist'].sudo().search([('id','=',1)], limit=1)
        p = []

        for product in products:
            combination = product._get_first_possible_combination()
            combination_info = product._get_combination_info(combination=combination, only_template=True, add_qty=1, pricelist=pricelist)
            news = {
                "name": product.name,
                "id": product.id,
                "list_price": product.list_price,
                "combination": combination_info
            }
            p.append(news)
        return p