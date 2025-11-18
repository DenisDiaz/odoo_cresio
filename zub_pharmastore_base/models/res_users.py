# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
import random
import datetime

def get_now():
    return datetime.datetime.now()

def generate_code():
    return str(random.randint(1000, 9999))

class ResUsers(models.Model):
    _inherit = "res.users"

    reset_code = fields.Char(string="Codigo de Recuperacion", readonly=True)
    reset_expiration = fields.Datetime(string="Expiracion del Codigo", readonly=True)

    def _get_mail_tz(self):
        return 1

    def generate_recovery_code(self, data):
        email = data.get("email")
        if not email:
            return {"message": "El email es obligatorio"}, 400
        user = self.sudo().search([("login", "=", email)], limit=1)
        if not user:
            return {"message": "El usuario no existe"}, 404
        code = str(generate_code())[:4]
        expiration = fields.Datetime.to_string(
            get_now() + datetime.timedelta(minutes=30)
        )
        user.sudo().write({
            "reset_code": code,
            "reset_expiration": expiration
        })
        ok, msg = self._send_recovery_email(user)
        if not ok:
            return {"message": f"Error al enviar correo: {msg}"}, 500

        return {"message": "Código generado correctamente"}, 200

    def validate_recovery_code(self, data):
        email = data["email"]
        code = data["code"]
        if not email or not code:
            return {"message": "Email y código son obligatorios"}, 400
        user = self.search([("login", "=", email)], limit=1)
        if not user or not user.reset_code:
            return {"message": "No hay un código para este usuario"}, 404
        expiration = fields.Datetime.from_string(user.reset_expiration)
        if get_now() > expiration:
            return {"message": "El código ha expirado"}, 417
        if user.reset_code != code:
            return {"message": "Código inválido"}, 417
        return {"message": "Código válido"}, 200

    def reset_password(self, data):
        email = data["email"]
        code = data["code"]
        password = data["password"]
        if not email or not code or not password:
            return {"message": "Email, código y nueva contraseña son requeridos"}, 400
        user = self.search([("login", "=", email)], limit=1)
        if not user:
            return {"message": "El usuario no existe"}, 404
        expiration = fields.Datetime.from_string(user.reset_expiration)
        if get_now() > expiration:
            return {"message": "El código ha expirado"}, 417
        if user.reset_code != code:
            return {"message": "Código inválido"}, 417
        if len(password) < 6 or len(password) > 15:
            return {"message": "La contraseña debe tener entre 6 y 15 caracteres"}, 417
        user.write({
            "reset_code": False,
            "reset_expiration": False,
            "password": password
        })
        return {"message": "Tu contraseña se actualizó correctamente! Inicia sesión con tu nueva contraseña"}, 200

    def _send_recovery_email(self, user):
        try:
            if not user or not user.email:
                return False, "El usuario no tiene correo registrado"
            template = self.env.ref(
                'zub_pharmastore_base.password_reset_code_template',
                raise_if_not_found=False
            )
            if not template:
                return False, "No se encontró la plantilla de correo"
            email_values = {'email_from': user.company_id.email}
            template.sudo().send_mail(
                user.id,
                force_send=True,
                email_values=email_values
            )
            return True, "Correo enviado"
        except Exception as e:
            return False, str(e)
