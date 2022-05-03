# -*- coding: utf-8 -*-
# from odoo import http


# class Sources/exeNoFollowInvoices(http.Controller):
#     @http.route('/sources/exe_no_follow_invoices/sources/exe_no_follow_invoices/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sources/exe_no_follow_invoices/sources/exe_no_follow_invoices/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('sources/exe_no_follow_invoices.listing', {
#             'root': '/sources/exe_no_follow_invoices/sources/exe_no_follow_invoices',
#             'objects': http.request.env['sources/exe_no_follow_invoices.sources/exe_no_follow_invoices'].search([]),
#         })

#     @http.route('/sources/exe_no_follow_invoices/sources/exe_no_follow_invoices/objects/<model("sources/exe_no_follow_invoices.sources/exe_no_follow_invoices"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sources/exe_no_follow_invoices.object', {
#             'object': obj
#         })
