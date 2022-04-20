from odoo import models, fields, api,tools, _
from odoo.exceptions import ValidationError

class Statistics_sell (models.Model):
    _name = "statistics.sell"
    _description = "Estadísticas de venta por producto"

    product_id = fields.Many2one()
    nro_week = fields.Integer(string='Nro de Semana')
    date_order = fields.Date(string='Fecha')
    name_day = fields.Char(string='Dia de la semana')
    week_name = fields.Char(string='Semana')
    quantity = fields.Integer()

    @api.model
    def _get_sales_product(self, date_orders):
            ret_list = []
            req = (
                "SELECT  prod.id as product_id, sum(line.product_uom_qty)as quantity , CAST(sale.date_order as date) as date_order  ,"
                " to_char(CAST(sale.date_order as date), 'dy') as name_day," +
                " to_char(CAST(sale.date_order as date), 'MON') ||  CAST((extract('day' from date_trunc('week', CAST(sale.date_order as date)) -   date_trunc('week', date_trunc('month', CAST(sale.date_order as date)))) / 7 + 1) as char) ||'_'|| to_char(current_date, 'yy') as week_name ," +
                " extract(week from CAST(sale.date_order as date)) as nro_week " +
                " FROM  product_template as prod inner join product_brand on prod.product_brand_id=  product_brand.id inner " +
                " join res_partner on res_partner.id= product_brand.partner_id " +
                " LEFT JOIN (sale_order_line as line  inner join sale_order as sale on  line.order_id = sale.id) on prod.id=line.product_id " )
            req_where = " WHERE prod.active=True "
            #if date_orders:
            #    req_where = req_where + "and sale.date_order = " + date_orders
            req_grouporder = " GROUP  by prod.id, prod.name, prod.default_code, res_partner.name  ,  CAST(sale.date_order as date),sale.date_order  ORDER by res_partner.name, sale.date_order"

            self.env.cr.execute(req + req_where + req_grouporder)
            for rec in self.env.cr.dictfetchall():
                self.env['statistics.sell'].create({
                    'product_id': rec['product_id'],
                    'nro_week': rec['nro_week'],
                    'date_order': rec['date_order'],
                    'name_day': rec['name_day'],
                    'week_name': rec['week_name'],
                    'quantity': rec['quantity']
                })

