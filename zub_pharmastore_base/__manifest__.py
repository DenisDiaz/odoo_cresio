# -*- coding: utf-8 -*-
{
    'name': "zub_pharmastore_base",
    'summary': "Api para recuperar contraseña",
    'description': 'Zublime Forgot_Password',
    'author': 'Zublime',
    "website": "https://zublime.mx",
    'contributors': [
        'William Vidal  <william.vidal@zublime.dev>',
    ],
    'category': 'Others',
    'version': '0.1',
    'depends': ['base', 'mail'],
    'data': [
        # 'security/ir.model.access.csv',
        "views/email_template.xml",
        'views/res_config_settings_views.xml',
    ],
    "license": "LGPL-3",
    'installable': True,
    'auto_install': True,
    'application': False,
}

