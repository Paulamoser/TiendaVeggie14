from odoo import models, fields, api,tools, _
from odoo.exceptions import ValidationError

class Statistics_sales (models.Model):
    _name = "statistics.sales"
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
                self.env['statistics.sales'].create({
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

    product_id = fields.Integer()
    partner_name = fields.Char()
    default_code = fields.Char()
    qt_T5 = fields.Integer(string="week - 5")
    qt_T4 = fields.Integer(string="week - 4")
    qt_T3 = fields.Integer(string="week - 3")
    qt_T2 = fields.Integer(string="week - 2")
    qt_T1 = fields.Integer(string="week - 1")

    def init(self):
        #proveedores= self.env['product_brand'].browse([])
        tools.drop_view_if_exists(self._cr, self._table)
        self._cr.execute(
            """  SELECT (extract(week FROM current_date)) ;""")
        actual_week = self._cr.fetchone()
        query=  """  SELECT pt.id as product_id, default_code, p.name as partner_name, 0 as qt_T5, 0 as qt_T4, 0 as qt_T3,
           0 as qt_T2 , 0 as qt_T1 from product_brand as pb INNER JOIN res_partner as p on  p.id=pb.partner_id  
        INNER JOIN product_template  as pt ON pt.product_brand_id=pb.id 
        order by partner_id
        """
        self._cr.execute("""CREATE or REPLACE VIEW %s as (%s
                )""" % (self._table, query))

        self._cr.execute("""  SELECT product_id from   report_statistics_sale""")
        productos = self._cr.fetchall()
        for prod in productos:
                qt_T5=0
                qt_T4=0
                qt_T3=0
                qt_T2=0
                qt_T1=0
                for i in range(5):
                    self._cr.execute(
                        """  SELECT sum(quantity)as quantity 
                        FROM  statistics_sales as ventas 
                        WHERE nro_week= """ + str(int(actual_week[0]) -i) +
                        """ and  product_id=""" + str(prod[0])
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
                self._cr.execute(
                    """  SELECT sum(quantity)as quantity 
                    FROM  statistics_sales as ventas 
                    WHERE nro_week= """ + str(int(actual_week[0]) - i) +
                    """ and  product_id=""" + str(prod[0])
                )
                self._cr.execute(
                    """  UPDATE  report_statistics_sale
                    SET qt_T5=""" + str(qt_T5) + """, qt_T4=""" +  str(qt_T4) +
                        """, qt_T3=""" + str(qt_T3) + """, qt_T2= """ + str(qt_T2) +
                    """, qt_T1=""" + str(qt_T1) +
                    """ WHERE  product_id=""" + str(prod[0]) + """ and nro_week= """ + str(int(actual_week[0]) -i)
                )
