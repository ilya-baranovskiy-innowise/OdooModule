from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_primary = fields.Boolean(string='Primary Contact')

    @api.constrains('child_ids', 'child_ids.is_primary')
    def _check_single_primary(self):
        for partner in self:
            primary_contacts = partner.child_ids.filtered(lambda c: c.is_primary)
            if len(primary_contacts) > 1:
                raise ValidationError("Primary contact already exists")

    def unlink(self):
        for partner in self:
            if partner.is_primary and partner.parent_id:
                parent = partner.parent_id
                primary_contacts = parent.child_ids.filtered(lambda c: c.is_primary)
                if len(primary_contacts) == 1 and primary_contacts == partner:
                    raise UserError('You cannot delete the only primary contact of the partner')
        return super(ResPartner, self).unlink()
