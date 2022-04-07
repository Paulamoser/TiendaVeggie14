# -*- coding: utf-8 -*-
# from odoo import http


# class PurchasePlanner(http.Controller):
#     @http.route('/purchase_planner/purchase_planner/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/purchase_planner/purchase_planner/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('purchase_planner.listing', {
#             'root': '/purchase_planner/purchase_planner',
#             'objects': http.request.env['purchase_planner.purchase_planner'].search([]),
#         })

#     @http.route('/purchase_planner/purchase_planner/objects/<model("purchase_planner.purchase_planner"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('purchase_planner.object', {
#             'object': obj
#         })
