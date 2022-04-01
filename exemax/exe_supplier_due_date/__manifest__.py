# -*- coding: utf-8 -*-
{
    'name': "Fecha de vencimiento en pago a proveedores",

    'summary': """
        Se agrega el campo Fecha de vencimiento en recibos de pago a proveedores y en la vista tree
        account.payment.group """,

    'description': """
        Se agrega el campo Fecha de vencimiento en pago a proveedores y en la vista tree
    """,

    'author': "Exemax",
    'website': "http://www.exemax.com.ar",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','purchase'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
    ],

}
