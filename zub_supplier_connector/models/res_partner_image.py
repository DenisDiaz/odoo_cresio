from odoo import fields, models, _

class ResPartnerImage(models.Model):
    _name = 'res.partner.image'
    _description = 'Imágenes de la Sucursal'

    name = fields.Char(string='Imagen de Sucursal')
    image = fields.Image("Image", max_width=1920, max_height=1920)
    partner_id = fields.Many2one('res.partner', string='Partner', ondelete='cascade')