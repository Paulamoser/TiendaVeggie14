# -*- coding: utf-8 -*-
 
from odoo import http
from odoo.http import content_disposition, request
from datetime import datetime
import io
import xlsxwriter
 
 
class SaleExcelReportController(http.Controller):
    @http.route([
        '/account/account_mix_report/<model("ati.account.wizard"):wizard>',
    ], type='http', auth="user", csrf=False)
    def get_sale_excel_report(self,wizard=None,**args):
         
        response = request.make_response(
                    None,
                    headers=[
                        ('Content-Type', 'application/vnd.ms-excel'),
                        ('Content-Disposition', content_disposition('Reporte de Facturas' + '.xlsx'))
                    ]
                )
 
        # Crea workbook
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
 
        # Estilos de celdas
        title_style = workbook.add_format({'font_name': 'Times', 'font_size': 14, 'bold': True, 'align': 'center','bg_color': 'yellow', 'left': 1, 'bottom':1, 'right':1, 'top':1})
        header_style = workbook.add_format({'font_name': 'Times', 'bold': True, 'left': 1, 'bottom':1, 'right':1, 'top':1, 'align': 'center'})
        text_style = workbook.add_format({'font_name': 'Times', 'left': 1, 'bottom':1, 'right':1, 'top':1, 'align': 'left'})
        text_product = workbook.add_format({'font_name': 'Times', 'left': 1, 'bottom':1, 'right':1, 'top':1, 'align': 'right'})
        number_style = workbook.add_format({'font_name': 'Times', 'left': 1, 'bottom':1, 'right':1, 'top':1, 'align': 'right'})
        date_style = workbook.add_format({'num_format': 'dd/mm/yy','font_name': 'Times', 'left': 1, 'bottom':1, 'right':1, 'top':1, 'align': 'right'})
        currency_style = workbook.add_format({'num_format':'$#,##0.00','font_name': 'Times', 'left': 1, 'bottom':1, 'right':1, 'top':1, 'align': 'right'})
 
        # Crea worksheet
        sheet = workbook.add_worksheet("Reporte")
        # Orientacion landscape
        sheet.set_landscape()
        # Tamaño de papel A4
        sheet.set_paper(9)
        # Margenes
        sheet.set_margins(0.5,0.5,0.5,0.5)

        # Configuracion de ancho de columnas
        sheet.set_column('A:A', 10)
        sheet.set_column('B:B', 10)
        sheet.set_column('C:C', 5)
        sheet.set_column('D:D', 19)
        sheet.set_column('E:E', 20)
        sheet.set_column('F:F', 15)
        sheet.set_column('G:G', 10)
        sheet.set_column('H:H', 12)
        sheet.set_column('I:I', 50)
        sheet.set_column('J:J', 15)
        sheet.set_column('K:K', 21)
        sheet.set_column('L:L', 16)
        sheet.set_column('M:M', 19)
        sheet.set_column('N:V', 15)
        sheet.set_column('W:W', 25)
        sheet.set_column('X:AG', 15)

        # Titulos de reporte
        sheet.merge_range('A1:G1', 'Documento de venta', title_style)
        sheet.merge_range('H1:L1', 'Definicion de producto', title_style)
        sheet.merge_range('M1:AG1', 'Definicion del cliente', title_style)
         
        # Títulos de columnas
        sheet.write(1, 0, 'Fecha', header_style)
        sheet.write(1, 1, 'Mes', header_style)
        sheet.write(1, 2, 'Año', header_style)
        sheet.write(1, 3, 'Tipo de documento', header_style)
        sheet.write(1, 4, 'N° Factura', header_style)
        sheet.write(1, 5, 'Precio unitario', header_style)
        sheet.write(1, 6, 'Cantidad', header_style)
        sheet.write(1, 7, 'Tipo', header_style)
        sheet.write(1, 8, 'Producto', header_style)
        sheet.write(1, 9, 'ID Producto', header_style)
        sheet.write(1, 10, 'Presentacion producto', header_style)
        sheet.write(1, 11, 'Proveedor', header_style)
        sheet.write(1, 12, 'Razon Social', header_style)
        sheet.write(1, 13, 'RS ID Odoo', header_style)
        sheet.write(1, 14, 'Codigo Interno', header_style)
        sheet.write(1, 15, 'Fecha de alta', header_style)
        sheet.write(1, 16, 'Nombre fantasia', header_style)
        sheet.write(1, 17, 'Direccion', header_style)
        sheet.write(1, 18, 'Codigo Postal', header_style)
        sheet.write(1, 19, 'Ciudad / Barrio', header_style)
        sheet.write(1, 20, 'Provincia', header_style)
        sheet.write(1, 21, 'Cuit', header_style)
        sheet.write(1, 22, 'Responsabilidad AFIP', header_style)
        sheet.write(1, 23, 'Forma pago', header_style)
        sheet.write(1, 24, 'Canal', header_style)
        sheet.write(1, 25, 'Dia de entrega', header_style)
        sheet.write(1, 26, 'Expreso', header_style)
        sheet.write(1, 27, 'Tarifa', header_style)
        sheet.write(1, 28, 'Movil', header_style)
        sheet.write(1, 29, 'Telefono', header_style)
        sheet.write(1, 30, 'Correo', header_style)
        sheet.write(1, 31, 'Instagram', header_style)
        sheet.write(1, 32, 'Nombre de contacto', header_style)

        row = 2
        number = 1

        #Busca todas las facturas
        invoices = request.env['account.move'].search([('move_type','=','out_invoice'), ('invoice_date','>=', wizard.start_date), ('invoice_date','<=', wizard.end_date)])

        for invoice in invoices:
 
            #Busca todas las lineas de cada factura
            invoce_lines = request.env['account.move.line'].search([('move_id','=',invoice.id),('product_id','!=', False)])

            for line in invoce_lines:
                # Documento de venta
                sheet.write(row, 0, invoice.invoice_date, date_style)
                sheet.write(row, 1, datetime.strptime(str(invoice.invoice_date), "%Y-%m-%d").strftime('%B'), text_style)
                sheet.write(row, 2, datetime.strptime(str(invoice.invoice_date), "%Y-%m-%d").strftime('%Y'), text_style)
                sheet.write(row, 3, invoice.l10n_latam_document_type_id.name, text_style)
                sheet.write(row, 4, invoice.name, text_style)
                sheet.write(row, 5, line.price_unit, currency_style)
                sheet.write(row, 6, line.quantity, number_style)

                # Definicion de producto
                sheet.write(row, 7, line.product_id.type, number_style)
                sheet.write(row, 8, line.product_id.name, number_style)
                #Se buscan los datos necesarios para formarl el External ID de product.template
                model_data = request.env['ir.model.data'].search(([('model', '=', 'product.template'),('res_id','=',line.product_id.product_tmpl_id.id)]), limit=1)
                sheet.write(row, 9, "%s.%s" % (model_data.module, model_data.name), text_style)
                sheet.write(row, 10, line.product_id.uom_id.name, number_style)
                sheet.write(row, 11, invoice.name, text_style)# Reemplazar con proveedor / marca

                # Definicion del cliente
                sheet.write(row, 12, invoice.partner_id.name, text_style)
                model_data = request.env['ir.model.data'].search(([('model', '=', 'res.partner'),('res_id','=',invoice.partner_id.id)]), limit=1)
                sheet.write(row, 13, "%s.%s" % (model_data.module, model_data.name), text_style)
                sheet.write(row, 14, invoice.partner_id.comment, text_style)
                sheet.write(row, 15, invoice.partner_id.create_date, date_style)
                sheet.write(row, 16, invoice.partner_id.internal_reference, text_style) #Nombre Fantasia
                sheet.write(row, 17, invoice.partner_id.street, text_style)
                sheet.write(row, 18, invoice.partner_id.zip, text_style)
                sheet.write(row, 19, invoice.partner_id.city, text_style)
                sheet.write(row, 20, invoice.partner_id.state_id.name, text_style)
                sheet.write(row, 21, invoice.partner_id.vat, text_style)
                sheet.write(row, 22, invoice.partner_id.l10n_ar_afip_responsibility_type_id.name, text_style)
                sheet.write(row, 23, invoice.partner_id.property_payment_term_id.name, text_style) #Forma de pago
                sheet.write(row, 24, invoice.partner_id.team_id.name, text_style)
                sheet.write(row, 25, invoice.partner_id.delivery_day, text_style) #Dia Entrega
                sheet.write(row, 26, invoice.partner_id.carrier_id.name, text_style) #Expreso
                sheet.write(row, 27, invoice.partner_id.property_product_pricelist.name, text_style)
                sheet.write(row, 28, invoice.partner_id.mobile, text_style)
                sheet.write(row, 29, invoice.partner_id.phone, text_style)
                sheet.write(row, 30, invoice.partner_id.email, text_style)
                sheet.write(row, 31, invoice.partner_id.net_captor, text_style) #Red Social
                sheet.write(row, 32, invoice.partner_id.ref, text_style) #Red Social
 
                row += 1
                number += 1
 
        # Devuelve el archivo de Excel como respuesta, para que el navegador pueda descargarlo 
        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()
 
        return response
