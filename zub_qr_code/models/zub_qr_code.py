import random
import string
from datetime import timedelta, datetime
from odoo import models, fields, api

class ZubQrCode(models.Model):
    _name = "zub.qr.code"
    _description = "Código QR"

    code = fields.Char(string="Código", required=True, index=True)
    create_date = fields.Datetime(string="Fecha de creación", readonly=True, default=lambda self: fields.Datetime.now())
    expiration_date = fields.Datetime(string="Fecha de expiración", required=True)
    user_id = fields.Many2one("res.users", string="Usuario", required=True, ondelete="cascade")

    @api.model
    def generate_random_code(self, length):
        return ''.join(random.choices(string.digits, k=length))

    def create_user_code(self, user):
        #user = self.env['res.users'].browse(user_id)
        if not user.exists():
            return {"message": "Usuario no encontrado"}, 404

        qr_code_length = int(self.env['ir.config_parameter'].sudo().get_param('pharmastore.qr_code_length', default=8.0))
        qr_code_duration = int(self.env['ir.config_parameter'].sudo().get_param('pharmastore.qr_code_duration', default=15.0))

        code = self.generate_random_code(qr_code_length)
        now = fields.Datetime.now()
        expiration = now + timedelta(minutes=qr_code_duration)

        record = self.create({
            'code': code,
            'expiration_date': expiration,
            'user_id': user.id,
        })

        return {
            "message": "Código generado correctamente",
            "code": record.code,
        }, 200

    @api.model
    def validate_code(self, data):
        code = data["code"]

        if not code:
            return {"success": False, "message": "El código es obligatorio."}, 400

        record = self.search([("code", "=", code)], limit=1)
        if not record:
            return {"success": False, "message": "El código no existe."}, 404

        current_time = fields.Datetime.now()
        if record.expiration_date < current_time:
            return {"success": False, "message": "El código ha expirado."}, 400

        return {
            "message": "El código es válido.",
            "data": {
                "id": record.id,
                "code": record.code,
                "user_id": record.user_id.id,
                "user_name": record.user_id.name,
                "create_date": record.create_date,
                "expiration_date": record.expiration_date,
            }
        }, 200

    @api.model
    def cron_clean_expired_codes(self):
        now = fields.Datetime.now()
        expired_codes = self.search([('expiration_date', '<', now)])
        count = len(expired_codes)
        expired_codes.unlink()
        _logger = self.env['ir.logging']
        self.env.cr.commit()
        return f"{count} códigos expirados eliminados"
