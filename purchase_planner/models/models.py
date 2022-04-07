# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import models, fields, api,tools, _
from odoo.exceptions import ValidationError
#import logging

class PurchasePlanner(models.Model):
    _name="purchase.planner"
    _description = "Planificador de compras"

    partner_id = fields.Many2one(
        'res.partner',
        string='Proveedor',
        required=True
    )
    nro_week = fields.Integer(string='Nro de Semana')
    fecha = fields.Date(string='Fecha',_defaults= {  'record_date': fields.date.context_today,})
    name_day = fields.Char(string='Dia de la semana')
    week = fields.Char(string='Semana')
    purchase_product_line = fields.One2many('purchase.planner.line', 'purchase_planner_id', string='Purchase Planner Lines',  copy=True, auto_join=True)

    @api.onchange('partner_id')
    def onchange_partner_id(self):
            cr = self._cr
            tools.drop_view_if_exists(cr,'purchase.planner.line')
            # we use tax_ids for base amount instead of tax_base_amount for two reasons:
            # * zero taxes do not create any aml line so we can't get base for them with tax_base_amount
            # * we use same method as in odoo tax report to avoid any possible discrepancy with the computed tax_base_amount
            sql = """ SELECT  prod.name, prod.default_code, res_partner.name
              FROM  product_template as prod INNER JOIN product_brand ON prod.product_brand_id=  product_brand.id 
              INNER JOIN  res_partner ON res_partner.id= product_brand.partner_id
              WHERE prod.active=True AND res_partner_id= """ + self.partner_id + """order by res_partner.name;

            """
            cr.execute(sql)

class PurchasePlannerLine(models.Model):
    _name = "purchase.planner.line"
    _description = "Productos del planificador de compras"

    purchase_planner_id = fields.Many2one('purchase.planner', string='Purchase planner Reference', required=True, ondelete='cascade', index=True, copy=False)
    product_id = fields.Many2one(
        'product.template',
        string='Producto',
        required=True
    )

    product_name = fields.Char(string='Producto')
    today_stock_am = fields.integer()
    today_in = fields.integer()
    today_out = fields.integer()
    today_stock_pm = fields.integer()
    today_purchase = fields.integer()

    second_in = fields.integer()
    second_out = fields.integer()
    second_stock_pm = fields.integer()
    second_purchase = fields.integer()

    trhird_in = fields.integer()
    third_out = fields.integer()
    third_stock_pm = fields.integer()
    thirth_purchase = fields.integer()

    fourth_in = fields.integer()
    fourth_out = fields.integer()
    fourth_stock_pm = fields.integer()
    fourth_purchase = fields.integer()

    fifth_in = fields.integer()
    fifth_out = fields.integer()
    fifth_stock_pm = fields.integer()
    fifth_purchase = fields.integer()

    sixth_in = fields.integer()
    sixth_out = fields.integer()
    sixth_stock_pm = fields.integer()
    sixth_purchase = fields.integer()

    seventh_in = fields.integer()
    seventh_out = fields.integer()
    seventh_stock_pm = fields.integer()
    seventh_purchase = fields.integer()

