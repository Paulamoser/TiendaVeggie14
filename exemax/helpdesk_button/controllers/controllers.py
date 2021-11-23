# -*- coding: utf-8 -*-
# from odoo import http


# class HelpdeskButton(http.Controller):
#     @http.route('/helpdesk_button/helpdesk_button/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/helpdesk_button/helpdesk_button/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('helpdesk_button.listing', {
#             'root': '/helpdesk_button/helpdesk_button',
#             'objects': http.request.env['helpdesk_button.helpdesk_button'].search([]),
#         })

#     @http.route('/helpdesk_button/helpdesk_button/objects/<model("helpdesk_button.helpdesk_button"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('helpdesk_button.object', {
#             'object': obj
#         })
