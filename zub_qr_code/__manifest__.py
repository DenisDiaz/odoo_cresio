{
    'name': "zub_qr_code",
    'summary': "Api para generar y validar el codigo QR",
    'description': 'Api para generar y validar el codigo QR',
    'author': 'Zublime',
    "website": "https://zublime.mx",
    'contributors': [
        'William Vidal  <william.vidal@zublime.dev>',
    ],
    'category': 'Others',
    'version': '0.1',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'data/ir_cron_data.xml',
    ],
    "license": "LGPL-3",
    'installable': True,
    'auto_install': True,
    'application': False,
}
