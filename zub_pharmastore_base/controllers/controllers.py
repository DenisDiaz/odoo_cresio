# -*- coding: utf-8 -*-

from odoo.http import request, Response
from odoo import _, http, service
from odoo.addons.zub_utils.tools.http import make_json_response

class CommonController(http.Controller):
    @http.route('/api/v1/generate_recovery_code', type='json', auth='none', methods=['POST'])
    def forgot_password(self, **kwargs):
        model = request.env['res.users'].sudo()
        try:
            data, status = model.generate_recovery_code(request.httprequest.json)
        except Exception as e:
            data, status = {"message": str(e)}, 403
        return make_json_response(data, status=status)

    @http.route('/api/v1/validate_recovery_code', type='json', auth='none', methods=['POST'])
    def validate_code(self, **kwargs):
        model = request.env['res.users'].sudo()
        try:
            data, status = model.validate_recovery_code(request.httprequest.json)
        except Exception as e:
            data, status = {"message": str(e)}, 403
        return make_json_response(data, status=status)

    @http.route('/api/v1/reset_password', type='json', auth='none', methods=['POST'])
    def reset_password(self, **kwargs):
        model = request.env['res.users'].sudo()
        try:
            data, status = model.reset_password(request.httprequest.json)
        except Exception as e:
            data, status = {"message": str(e)}, 403
        return make_json_response(data, status=status)


# aqui