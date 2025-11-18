from odoo import models, fields

class LoyaltyPromotionImage(models.Model):
    _name = "loyalty.promotion.image"
    _description = "Imagenes de la promocion"

    promotion_id = fields.Many2one(
        "loyalty.program",
        string="promocion",
        required=True,
        ondelete="cascade"
    )

    sequence = fields.Integer('Sequence', default=1, help="Determine the display order")
    image = fields.Image(string="Imagen", required=True)
    image_type = fields.Selection(
        [
            ("image_16_9", "16:9"),
            ("image_4_3", "4:3"),
            ("image_1_1", "1:1"),
        ],
        string="Tipo de imagen",
        required=True
    )
    active = fields.Boolean(string="Activo", default=True)
