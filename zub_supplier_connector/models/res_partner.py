# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_supplier_with_external_connection = fields.Boolean("Conexión Externa", default=False)
    partner_image_ids = fields.One2many(
        'res.partner.image',
        'partner_id',
        string='Imágenes'
    )

    @api.model
    def get_nearby_partners(self, lat, lon):
        radius_km = float(self.env['ir.config_parameter'].sudo().get_param('pharmastore.radius_km', default=5.0))

        query = """
            SELECT
                *
            FROM (
                SELECT
                *,
                6371 * 2 * ASIN(
                    SQRT(
                        POWER(SIN(RADIANS(partner_latitude - %s) / 2), 2) +
                        COS(RADIANS(%s)) * COS(RADIANS(partner_latitude)) *
                        POWER(SIN(RADIANS(partner_longitude - %s) / 2), 2)
                    )
                ) AS distance
                FROM res_partner
                WHERE partner_latitude IS NOT NULL AND partner_longitude IS NOT NULL
            ) AS sub
            WHERE distance <= %s
            ORDER BY distance ASC
        """

        self._cr.execute(query, (lat, lat, lon, radius_km))
        rows = self._cr.dictfetchall()
        return rows

    def get_office_branches(self, data):
        latitude = data["latitude"]
        longitude = data["longitude"]
        records = self.env['res.partner'].sudo().get_nearby_partners(latitude, longitude)
        result = []
        for rec in records:
            result.append({
                "name": rec["name"], #rec.name,
                "street": rec["street"], #rec.street,
                "street2": rec["street2"], #rec.street2,
                "city": rec["city"], #rec.city,
                "state": rec["name"], #rec.state_id.name,
                "zip": rec["zip"], #rec.zip,
                "country_id": rec["country_id"], #rec.country_id.name,
                "phone": rec["phone"], #rec.phone,
                "mobile": rec["mobile"], #rec.mobile,
                "email": rec["email"], #rec.email,
                "website": rec["website"], #rec.website,
                "partner_longitude": rec["partner_longitude"], #rec.partner_longitude,
                "partner_latitude": rec["partner_latitude"], #rec.partner_latitude,
                "distance_km": round(rec["distance"], 2)
            })
        if not result:
            return {}, 404
        return {"data": result}, 200

    def get_office_branch_by_id(self, data):
        partner_id = data["id"]

        partner = self.env['res.partner'].sudo().browse(partner_id)
        if not partner.exists():
            return {"message": "La sucursal no existe"}, 404

        images_data = []
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        for img in partner.partner_image_ids:
            image_url = f"{base_url}/web/image/res.partner.image/{img.id}/image"
            images_data.append({
                "id": img.id,
                "name": img.name,
                "image": img.image,
                "image_url": image_url
            })

        result = {
            "name": partner.name,
            "street": partner.street,
            "street2": partner.street2,
            "city": partner.city,
            "state": partner.state_id.name,
            "zip": partner.zip,
            "country_id": partner.country_id.name,
            "phone": partner.phone,
            "mobile": partner.mobile,
            "email": partner.email,
            "website": partner.website,
            "partner_longitude": partner.partner_longitude,
            "partner_latitude": partner.partner_latitude,
            "images": images_data,
        }

        return result, 200

    def toggle_favorite(self, data):
        partner_id = data["partner_id"]
        user_id = data["user_id"]

        if not user_id or not partner_id:
            return {"message": "Se requieren user_id y partner_id"}, 400

        user = self.env['res.users'].sudo().browse(int(user_id))
        if not user.exists():
            return {"message": "El usuario no existe"}, 404

        partner = self.env['res.partner'].sudo().browse(int(partner_id))
        if not partner.exists():
            return {"message": "La sucursal no existe"}, 404

        favorite_partner = self.env["res.partner.favorite"].sudo()
        favorite = favorite_partner.search([
            ("partner_id", "=", partner.id),
            ("user_id", "=", user.id)
        ], limit=1)

        if favorite:
            favorite.unlink()
            return {"message": "Eliminado de favoritos."}, 200
        else:
            favorite_partner.create({
                "user_id": user.id,
                "partner_id": partner.id
            })
            return {"message": "Agregado de favoritos."}, 200

    @api.model
    def search_nearby_partners(self, data):
        latitude = data["latitude"]
        longitude = data["longitude"]
        name = data["name"]
        page = data["page"]
        limit = data["limit"]

        offset = (page - 1) * limit

        query = """
            SELECT
                *,
                6371 * 2 * ASIN(
                    SQRT(
                        POWER(SIN(RADIANS(partner_latitude - %s) / 2), 2) +
                        COS(RADIANS(%s)) * COS(RADIANS(partner_latitude)) *
                        POWER(SIN(RADIANS(partner_longitude - %s) / 2), 2)
                    )
                ) AS distance
            FROM res_partner
            WHERE
                partner_latitude IS NOT NULL
                AND partner_longitude IS NOT NULL
                AND name LIKE %s  
            ORDER BY distance ASC
            LIMIT %s OFFSET %s
        """

        params = (latitude, latitude, longitude, f'%{name}%', limit, offset)
        self.env.cr.execute(query, params)
        records = self.env.cr.dictfetchall()

        count_query = """
            SELECT COUNT(*) FROM res_partner
            WHERE
                partner_latitude IS NOT NULL
                AND partner_longitude IS NOT NULL
                AND name LIKE %s
        """
        self.env.cr.execute(count_query, (f'%{name}%',))
        total = self.env.cr.fetchone()[0]

        total_pages = (total // limit) + (1 if total % limit else 0)

        result = []
        for rec in records:
            result.append({
                "name": rec["name"], #rec.name,
                "street": rec["street"], #rec.street,
                "street2": rec["street2"], #rec.street2,
                "city": rec["city"], #rec.city,
                "state": rec["name"], #rec.state_id.name,
                "zip": rec["zip"], #rec.zip,
                "country_id": rec["country_id"], #rec.country_id.name,
                "phone": rec["phone"], #rec.phone,
                "mobile": rec["mobile"], #rec.mobile,
                "email": rec["email"], #rec.email,
                "website": rec["website"], #rec.website,
                "partner_longitude": rec["partner_longitude"], #rec.partner_longitude,
                "partner_latitude": rec["partner_latitude"], #rec.partner_latitude,
                "distance_km": round(rec["distance"], 2)
            })

        return {
            "total": total,
            "page": page,
            "limit": limit,
            "total_pages": total_pages,
            "data": result
        }, 200

