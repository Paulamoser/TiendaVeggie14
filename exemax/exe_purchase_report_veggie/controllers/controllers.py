# -*- coding: utf-8 -*-
# from odoo import http


# class Sources/exePurchaseReportVeggie(http.Controller):
#     @http.route('/sources/exe_purchase_report_veggie/sources/exe_purchase_report_veggie/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sources/exe_purchase_report_veggie/sources/exe_purchase_report_veggie/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('sources/exe_purchase_report_veggie.listing', {
#             'root': '/sources/exe_purchase_report_veggie/sources/exe_purchase_report_veggie',
#             'objects': http.request.env['sources/exe_purchase_report_veggie.sources/exe_purchase_report_veggie'].search([]),
#         })

#     @http.route('/sources/exe_purchase_report_veggie/sources/exe_purchase_report_veggie/objects/<model("sources/exe_purchase_report_veggie.sources/exe_purchase_report_veggie"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sources/exe_purchase_report_veggie.object', {
#             'object': obj
#         })
