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
            raise UserError('Ocurrio un error codificando la imagen \n%s.' % url)

        return data


    def import_file(self):


        try:
            book = xlrd.open_workbook(file_contents=base64.decodestring(self.file_name))

        except FileNotFoundError:
            raise UserError('No se encontró el archivo \n%s.' % self.filename)
        except xlrd.biffh.XLRDError:
            raise UserError('Solo archivos Excel soportados.')
        sh = book.sheet_by_index(0)
        for rx in range(1, sh.nrows):
                row = sh.row(rx)
                product = row[0].value
                image_path = row[1].value
                if "http://" in image_path or "https://" in image_path:
                    image_base64 = self.fetch_image_from_url(image_path)
                else:
                    try:
                        with open(image_path, 'rb') as image:
                            #image_base64 = image.read().encode("base64")
                            image_base64 = base64.b64encode(image.read())
                    except IOError:
                        raise Warning(
                            "Could not find the image '%s' - please make sure it is accessible to this script" %
                            product + '(' + image_path +')')
                if image_base64:
                    product_obj = self.env['product.template'].search([('default_code', '=', product)])
                    vals = {
                               'image_1920': image_base64,
                            }
                    if product_obj.id:
                            product_obj.write(vals)
                    else:
                            raise Warning("No se encontró el producto con referencia interna %s" % product + '(' + image_path +')')
