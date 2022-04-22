# -*- coding: utf-8 -*-
# from odoo import http


# class ExeSuplierDueDate(http.Controller):
#     @http.route('/exe_suplier_due_date/exe_suplier_due_date/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/exe_suplier_due_date/exe_suplier_due_date/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('exe_suplier_due_date.listing', {
#             'root': '/exe_suplier_due_date/exe_suplier_due_date',
#             'objects': http.request.env['exe_suplier_due_date.exe_suplier_due_date'].search([]),
#         })

#     @http.route('/exe_suplier_due_date/exe_suplier_due_date/objects/<model("exe_suplier_due_date.exe_suplier_due_date"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('exe_suplier_due_date.object', {
#             'object': obj
#         })
