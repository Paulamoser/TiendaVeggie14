# -*- coding: utf-8 -*-
# from odoo import http


# class ExeWebsiteCustom(http.Controller):
#     @http.route('/exe_website_custom/exe_website_custom/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/exe_website_custom/exe_website_custom/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('exe_website_custom.listing', {
#             'root': '/exe_website_custom/exe_website_custom',
#             'objects': http.request.env['exe_website_custom.exe_website_custom'].search([]),
#         })

#     @http.route('/exe_website_custom/exe_website_custom/objects/<model("exe_website_custom.exe_website_custom"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('exe_website_custom.object', {
#             'object': obj
#         })
