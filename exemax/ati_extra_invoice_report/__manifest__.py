# Copyright (c) 2020-Present Autodidacta TI. (<https://autodidactati.com>)

{
    'name': 'Extra Invoice Report',
    "version": "14.0",
    'author': 'Ivan Arriola - Autodidacta TI, Exemax',
    'category': 'Extra Tools',
    'license': 'OPL-1',
    'website': 'https://autodidactati.com',
    'summary': 'Reporte extra en facturas de ventas',
    'description': '''Descarga un reporte en formato xls con datos particulares de las facturas''',
    'depends': ['account'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/report_wizard_view.xml'
    ],
    'installable': True,
    'auto_install': False
}
