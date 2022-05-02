from odoo import models, fields, api,tools, _
from odoo.exceptions import ValidationError

class Statistics_sale (models.Model):
    _name = "statistics.sale"
    _description = "Estadísticas de venta por producto"

    product_id = fields.Many2one('product.template')
    nro_week = fields.Integer(string='Nro de Semana')
    date_order = fields.Date(string='Fecha')
    name_day = fields.Char(string='Dia de la semana')
    week_name = fields.Char(string='Semana')
    quantity = fields.Integer()
    year_order = fields.Integer(string='Año del pedido')

    @api.model
    def _get_sales_product(self):
            ret_list = []
            req = (
                "SELECT  prod.id as product_id, sum(line.product_uom_qty)as quantity , CAST(sale.date_order as date) as date_order  ,"
                " to_char(CAST(sale.date_order as date), 'dy') as name_day," +
                " to_char(CAST(sale.date_order as date), 'MON') ||  CAST((extract('day' from date_trunc('week', CAST(sale.date_order as date)) -   date_trunc('week', date_trunc('month', CAST(sale.date_order as date)))) / 7 + 1) as char) ||'_'|| to_char(current_date, 'yy') as week_name ," +
                " extract(week from CAST(sale.date_order as date)) as nro_week , extract('year' from sale.date_order) as anio" +
                " FROM  product_template as prod inner join product_brand on prod.product_brand_id=  product_brand.id inner " +
                " join res_partner on res_partner.id= product_brand.partner_id " +
                " LEFT JOIN (sale_order_line as line  inner join sale_order as sale on  line.order_id = sale.id) on prod.id=line.product_id " )
            req_where = " WHERE prod.active=True "
            #if date_orders:
            #    req_where = req_where + "and sale.date_order = " + date_orders
            req_grouporder = " GROUP  by prod.id, prod.name, prod.default_code, res_partner.name  ,  CAST(sale.date_order as date),sale.date_order  ORDER by res_partner.name, sale.date_order"

            self.env.cr.execute(req + req_where + req_grouporder)
            for rec in self.env.cr.dictfetchall():
                self.env['statistics.sale'].create({
                    'product_id': rec['product_id'],
                    'nro_week': rec['nro_week'],
                    'date_order': rec['date_order'],
                    'name_day': rec['name_day'],
                    'week_name': rec['week_name'],
                    'quantity': rec['quantity'],
                    'year_order': rec['anio']
                })

class ReportStatisticsSale(models.Model):
    _name = 'report.statistics.sale'
    _auto = False
    _description = 'Statistics Sales Report'

    default_code = fields.Char()
    qt_T5 = fields.Integer(string="week - 5")
    qt_T4 = fields.Integer(string="week - 4")
    qt_T3 = fields.Integer(string="week - 3")
    qt_T2 = fields.Integer(string="week - 2")
    qt_T1 = fields.Integer(string="week - 1")

    def init(self):
        #proveedores= self.env['product_brand'].browse([])
        self._cr.execute(
            """  SELECT (extract(week FROM current_date));""")
        actual_week = self._cr.fetchall()
        self._cr.execute(
            """  SELECT partner_id from product_brand ;""")
        proveedores = self._cr.fetchall()
        for provee in proveedores:
            productos = self.env['product_template'].search([('product_brand','=', provee)])

            for prod in productos:
                for i in range(5):
                    self._cr.execute(
                        """  SELECT sum(quantity)as quantity 
                        FROM  statistics_sale as ventas 
                        WHERE nro_week= """ + actual_week -i +
                        """ and  product_id=""" + prod.id
                        )
                    if (i==5):
                        qt_T5=self._cr.fetchall()
                    if (i == 4):
                        qt_T4 = self._cr.fetchall()
                    if (i==3):
                        qt_T3 = self._cr.fetchall()
                    if (i==2):
                        qt_T2=self._cr.fetchall()
                    if (i==1):
                        qt_T1=self._cr.fetchall()

                self.env['report_statistics_sale'].create({
                        'product_id': prod.default_code,
                        'qt_T5': qt_T5,
                        'qt_T4': qt_T4,
                        'qt_T3': qt_T3,
                        'qt_T2': qt_T2,
                        'qt_T1': qt_T1,
                    })
