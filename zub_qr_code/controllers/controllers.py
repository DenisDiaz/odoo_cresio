from odoo.http import request, Response
from odoo import _, http, service
from odoo.addons.zub_utils.tools.http import make_json_response

class ZubQrCode(http.Controller):
    @http.route('/api/v1/code/generate', type='json', auth='user', methods=['POST'])
    def generate_user_code(self, **kwargs):
        user = request.env.user
        if not user or user._is_public():
            return {"message": "No hay usuario autenticado o sesión inválida"}, 401

        model = request.env['zub.qr.code']
        try:
            data, status = model.create_user_code(user)
        except Exception as e:
            data, status = {"message": str(e)}, 403
        return make_json_response(data, status=status)

    @http.route('/api/v1/code/validate', type='json', auth='public', methods=['POST'], csrf=False)
    def validate_qr_code(self, **kwargs):
        model = request.env['zub.qr.code']
        try:
            data, status = model.validate_code(request.httprequest.json)
        except Exception as e:
            data, status = {"message": str(e)}, 403
        return make_json_response(data, status=status)
