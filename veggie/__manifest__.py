# -*- coding: utf-8 -*-
{
    'name': "Veggie Odoo",

    'summary': """
        Modificaciones a Tienda Veggie - Odoo""",

    'description': """
        Modificaciones a Tienda Veggie - Odoo
    """,

    'author': "Exemax, Codize",
    'website': "https://www.codize.ar",

    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['base', 'stock', 'sale', 'purchase', 'account', 'website_form'],

    'data': [
        'views/views.xml',
        'views/templates.xml',
        'views/table.xml',
        'views/table_parent_col.xml',
        'views/congelados.xml',
        'views/secos.xml',
        'views/refrigerados.xml',
        'views/mixtos.xml',
        'views/invoices.xml',
        'views/product.xml',
        'data/data.xml',
        'views/account_payment_group_custom.xml'
    ],
    'demo': [],
}