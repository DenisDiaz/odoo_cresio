# -*- coding: utf-8 -*-
from odoo.http import request, Response
from odoo import _, http, service
from odoo.addons.zub_utils.tools.http import make_json_response

class CommonController(http.Controller):

    @http.route('/api/v1/branch-offices/get-all', methods=['GET'], protected=False, type='json', auth='public')
    def branch_offices_get_all(self, **kw):
        model = request.env['res.partner'].sudo()
        try:
            data, status = model.get_office_branches(request.httprequest.json)
        except Exception as e:
            data, status = {"message": str(e)}, 403
        return make_json_response(data, status=status)

    @http.route('/api/v1/branch-offices/get-by-id', methods=['GET'], protected=False, type='json', auth='public')
    def branch_offices_get_by_id(self, **kw):
        model = request.env['res.partner'].sudo()
        try:
            data, status = model.get_office_branch_by_id(request.httprequest.json)
        except Exception as e:
            data, status = {"message": str(e)}, 403
        return make_json_response(data, status=status)

    @http.route('/api/v1/branch-offices/toggle-favorite', methods=['POST'], protected=False, type='json', auth='public')
    def branch_offices_toggle_favorite(self, **kwargs):
        model = request.env['res.partner'].sudo()
        try:
            data, status = model.toggle_favorite(request.httprequest.json)
        except Exception as e:
            data, status = {"message": str(e)}, 403
        return make_json_response(data, status=status)


    @http.route('/api/v1/branch-offices/search', methods=['POST'], protected=False, type='json', auth='public')
    def search_partners_query(self, **kwargs):
        model = request.env['res.partner'].sudo()
        try:
            data, status = model.search_nearby_partners(request.httprequest.json)
        except Exception as e:
            data, status = {"message": str(e)}, 403
        return make_json_response(data, status=status)