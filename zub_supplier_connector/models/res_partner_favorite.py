from odoo import api, fields, models, _

class ResPartnerFavorite(models.Model):
    _name = "res.partner.favorite"
    _description = "Relación de favoritos entre usuarios y partners"
    _rec_name = "partner_id"
    _order = "create_date desc"

    user_id = fields.Many2one("res.users", string="Usuario", required=True, ondelete="cascade")
    partner_id = fields.Many2one("res.partner", string="Partner", required=True, ondelete="cascade")

    _sql_constraints = [
        ('unique_user_partner', 'unique(user_id, partner_id)', 'El partner ya está marcado como favorito por este usuario.')
    ]
