from odoo import models, fields, api

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    pharmastore_radius = fields.Float(
        string="Radio de búsqueda de sucursales",
        config_parameter='pharmastore.radius_km',
        default=5.0,
        help="Distancia para buscar sucursales cercanas."
    )

    pharmastore_qr_code_length = fields.Integer(
        string="Cantidad de digitos del código QR",
        config_parameter='pharmastore.qr_code_length',
        default=8,
        help="Cantidad de digitos del código QR."
    )

    pharmastore_qr_code_duration = fields.Integer(
        string="Vigencia del código QR",
        config_parameter='pharmastore.qr_code_duration',
        default=15,
        help="Vigencia del código QR"
    )