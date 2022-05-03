# -*- coding: utf-8 -*-
{
    'name': "No follow invoices",

    'summary': """
        exe_no_follow_invoices se instala para desactivar los seguidores en facturacion""",

    'description': """
        Para que no se llene la casilla de quienes crean la factura. 

    """,

    'author': "Exemax - Matias",
    'website': "http://www.exemax.com.ar",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale','purchase'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
