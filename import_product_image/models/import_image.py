import csv
import requests
import base64
import xlrd
import sys
from odoo import models, fields, api
from odoo.exceptions import Warning, UserError
import logging
_logger = logging.getLogger(__name__)

class ProductImageImportWizard(models.TransientModel):
    _name = 'import.product_image'

    file_name = fields.Binary('Excel a importar', required=True)
    filename = fields.Char('Name of file')

    def fetch_image_from_url(self, url):
        """
        Gets an image from a URL and converts it to an Odoo friendly format
        so that we can store it in a Binary field.
        :param url: The URL to fetch.

        :return: Returns a base64 encoded string.
        """
        data = ""

        try:
            data = base64.b64encode(requests.get(url).content).replace(b"\n", b"")
        except Exception as e:
            raise UserError('Ocurrio un error codificanado la imagen \n%s.' % url)

        return data


    def import_file(self):


        try:
            book = xlrd.open_workbook(file_contents=base64.decodestring(self.file_name))

        except FileNotFoundError:
            raise UserError('No se encontrĂ³ el archivo \n%s.' % self.filename)
        except xlrd.biffh.XLRDError:
            raise UserError('Solo archivos Excel soportados.')
        sh = book.sheet_by_index(0)
        for rx in range(1, sh.nrows):
                row = sh.row(rx)
                product = row[0].value
                image_path = row[1].value
                image_base64 = self.fetch_image_from_url(image_path)
                product_obj = self.env['product.template'].search([('default_code', '=', product)])
                vals = {
                           'image_1920': image_base64,
                        }
                if product_obj.id:
                            product_obj.write(vals)
                else:
                            raise Warning("No se encontrĂ³ el producto con referencia interna %s" % product)
