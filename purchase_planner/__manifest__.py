# -*- coding: utf-8 -*-
{
    'name': "purchase_planner",

    'summary': """
        Planificador de compras Veggie en base a estadisticas de venta""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale','brand'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        #'views/views.xml',
        #'views/templates.xml'
        #"'views/statistics_sale.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
