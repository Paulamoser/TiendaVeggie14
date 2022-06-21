# -*- coding: utf-8 -*-
{
    'name': "Reporte de compra customizado",

    'summary': """
        Reporte de compra customizado para tienda veggie""",

    'description': """
        Reporte de compra customizado para tienda veggie hereda purchase.report_purchaseorder_document y lo modificamos
    """,

    'author': "Exemax - Matías Bressanello",
    'website': "http://www.exemax.com.ar",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','product'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        #'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
