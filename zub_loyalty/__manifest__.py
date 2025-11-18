# -*- coding: utf-8 -*-
{
    'name': "zub_loyalty",
    'summary': "Progrma de lealtad",
    'description': 'Progrma de lealtad',
    'author': 'Zublime',
    "website": "https://zublime.mx",
    'contributors': [
        'William Vidal  <william.vidal@zublime.dev>',
    ],
    'category': 'Others',
    'version': '0.1',
    'depends': ['base', 'sale_loyalty',],
    'data': [
        'security/ir.model.access.csv',
        "views/loyalty_promotion_image_view.xml",
    ],
    "license": "LGPL-3",
    'installable': True,
    'auto_install': True,
    'application': False,
}

