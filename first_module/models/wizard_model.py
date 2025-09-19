from odoo import models, fields


class WizardPartnerModel(models.Model):
    _name = 'create.partner.wizard'
    _description = 'Wizard to create parthner'

    name = fields.Text(string='Name', required=True)
    is_company = fields.Boolean(string='Is a company', required=True)

    def action_create_partner(self):
        """function to create partner record"""
        self.ensure_one()
        partner = self.env['res.partner'].create({
            'name': self.name,
            'is_company': self.is_company,
        })
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'res.partner',
            'view_mode': 'form',
            'res_id': partner.id,
            'target': 'current',
        }
