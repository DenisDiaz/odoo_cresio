from odoo.http import request, Response
from odoo import _, http, service
from odoo.addons.zub_utils.tools.http import make_json_response

class CommonController(http.Controller):
    @http.route('/api/v1/promotions/get-all', methods=['GET'], protected=False, type='json', auth='public')
    def promotions_get_all(self, **kw):
        model = request.env['loyalty.program'].sudo()
        try:
            data, status = model.get_promotions(request.httprequest.json)
        except Exception as e:
            data, status = {"message": str(e)}, 403
        return make_json_response(data, status=status)

    @http.route('/api/v1/promotions/get-by-id', methods=['GET'], protected=False, type='json', auth='public')
    def branch_offices_get_by_id(self, **kw):
        model = request.env['loyalty.program'].sudo()
        try:
            data, status = model.get_promotion_by_id(request.httprequest.json)
        except Exception as e:
            data, status = {"message": str(e)}, 403
        return make_json_response(data, status=status)