from odoo import models, fields


class FirstModelLine(models.Model):
    _name = 'first.model.line'
    _description = 'Lines for First Model'

    name = fields.Char(string='Line Name')
    first_model_id = fields.Many2one('first.model', string='First Model', ondelete='cascade')
