from odoo import api, fields, models, _

class LoyaltyProgram(models.Model):
    _inherit = "loyalty.program"

    highlight_text = fields.Char(
        string="Texto destacado",
        help="Texto destacado de la promoción"
    )

    terms_and_conditions = fields.Html(
        string="Términos y condiciones",
        help="Contenido HTML con los términos y condiciones de la promoción"
    )

    description_html = fields.Html(
        string="Descripción detallada",
        help="Contenido HTML para mostrar una descripción de la promoción"
    )

    image_ids = fields.One2many(
        "loyalty.promotion.image",
        "promotion_id",
        string="Imagenes",
        help="Listado de imagenes relacionadas de la promoción"
    )

    @api.model
    def get_promotions(self, data):
        program_type = data["program_types"]
        image_type = data["image_type"]

        if not program_type or not image_type:
            return {"message": "Los parámetros 'program_type' e 'image_type' son obligatorios."}, 400

        current_date = fields.Date.context_today(self)

        domain = [
            ("active", "=", True),
            ("program_type", "=", program_type),
            ("date_from", "<=", current_date),
            ("date_to", ">=", current_date),
        ]

        promotions = self.search(domain)

        results = []
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        for promotion in promotions:
            images = promotion.image_ids.filtered(
                lambda img: img.active and img.image_type == image_type
            )

            if not images:
                continue

            results.append({
                "id": promotion.id,
                "name": promotion.name,
                "program_type": promotion.program_type,
                "highlight_text": promotion.highlight_text,
                "terms_and_conditions": promotion.terms_and_conditions,
                "description_html": promotion.description_html,
                "date_from": promotion.date_from,
                "date_to": promotion.date_to,
                "images": [
                    {
                        "id": img.id,
                        "image": img.image,
                        "image_url": f"{base_url}/web/image/loyalty.promotion.image/{img.id}/image",
                        "sequence": img.sequence,
                        "image_type": img.image_type,
                    }
                    for img in images
                ]
            })

        if not results:
            return {}, 404
        return {"data": results}, 200

    def get_promotion_by_id(self, data):
        promotion_id = data["id"]

        promotion = self.env['loyalty.program'].sudo().browse(promotion_id)
        if not promotion.exists():
            return {"message": "La promoción no existe"}, 404

        images_data = []
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        for img in promotion.image_ids:
            images_data.append({
                "id": img.id,
                "image": img.image,
                "image_url": f"{base_url}/web/image/loyalty.promotion.image/{img.id}/image",
                "sequence": img.sequence,
                "image_type": img.image_type,
            })

        result = {
            "id": promotion.id,
            "name": promotion.name,
            "program_type": promotion.program_type,
            "highlight_text": promotion.highlight_text,
            "terms_and_conditions": promotion.terms_and_conditions,
            "description_html": promotion.description_html,
            "date_from": promotion.date_from,
            "date_to": promotion.date_to,
            "images": images_data,
        }

        return result, 200
