from odoo import models, fields, api
from odoo.exceptions import UserError


class MyOrder(models.Model):
    _name = 'my.order'
    _description = 'Order'

    name = fields.Char(string='Order name', required=True)
    order_line = fields.One2many('my.order.line', 'order_id', string='Order Lines')

    total_quantity = fields.Float(string='Total Quantity', compute='_compute_summary', store=True)
    total_amount = fields.Float(string='Total Amount', compute='_compute_summary', store=True)
    average_discount = fields.Float(string='Average Discount %', compute='_compute_summary', store=True)

    is_draft = fields.Boolean(String='Draft')
    is_confirm = fields.Boolean(String='Confirm')

    def action_confirm(self):
        for order in self:
            order.is_draft = False
            order.is_confirm = True

    def action_set_draft(self):
        for order in self:
            order.is_draft = True
            order.is_confirm = False

    @api.depends('order_line.quantity', 'order_line.unit_price', 'order_line.discount')
    def _compute_summary(self):
        for order in self:
            total_qty = 0.0
            total_amt = 0.0
            total_discount = 0.0
            lines_count = len(order.order_line)
            for line in order.order_line:
                total_qty += line.quantity
                line_total = line.quantity * line.unit_price * (1 - line.discount / 100)
                total_amt += line_total
                total_discount += line.discount
            order.total_quantity = total_qty
            order.total_amount = total_amt
            order.average_discount = (total_discount / lines_count) if lines_count else 0.0


class MyOrderLine(models.Model):
    _name = 'my.order.line'
    _description = 'Order Line'

    order_id = fields.Many2one('my.order', string='Order Reference', required=True, ondelete='cascade')
    product_name = fields.Char(string='Product Name', required=True)
    quantity = fields.Float(string='Quantity', default=1.0)
    unit_price = fields.Float(string='Unit Price', default=0.0)
    discount = fields.Float(string='Discount %', default=0.0)

    is_confirm = fields.Boolean(string='Is Confirmed', related='order_id.is_confirm', store=True)
    is_draft = fields.Boolean(string='Is Draft', related='order_id.is_draft', store=True)

    @api.model
    def create(self, vals):
        order = self.env['my.order'].browse(vals.get('order_id'))
        if order.is_confirm:
            raise UserError("Error")
        return super().create(vals)


    def unlink(self):
        for line in self:
            if line.order_id.is_confirm:
                raise UserError("Error")
        return super().unlink()
