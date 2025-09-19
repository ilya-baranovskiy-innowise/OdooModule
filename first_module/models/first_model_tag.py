from odoo import models, fields


class FirstModelTag(models.Model):
    _name = 'first.model.tag'
    _description = 'Tags for First Model'

    name = fields.Char(string='Tag Name')
