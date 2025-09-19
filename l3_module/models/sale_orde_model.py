from odoo import models, api, fields


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    express_delivery = fields.Boolean(string='Express Delivery')

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if not self.order_id:
            return

        other_lines = self.order_id.order_line.filtered(lambda l: l != self and l.product_id)
        selected_product_ids = other_lines.mapped('product_id').ids

        domain = {'product_id': [('id', 'not in', selected_product_ids)]}

        if self.product_id and self.product_id.id in selected_product_ids:
            self.product_id = False
            return {
                'warning': {
                    'title': 'Warning',
                    'message': 'This product already exists',
                },
                'domain': domain,
            }
        return {'domain': domain}


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _create_picking_for_lines(self, lines, express=False):
        self.ensure_one()
        picking_type = self.picking_type_id or self.partner_shipping_id.property_stock_delivery_carrier or self.env.ref(
            'stock.picking_type_out')

        picking_vals = {
            'partner_id': self.partner_shipping_id.id,
            'picking_type_id': picking_type.id,
            'origin': self.name,
            'location_id': picking_type.default_location_src_id.id,
            'location_dest_id': picking_type.default_location_dest_id.id,
            'sale_id': self.id,
        }
        picking = self.env['stock.picking'].create(picking_vals)

        moves = lines._create_stock_moves(picking_type)
        moves._action_confirm()
        moves._action_assign()

        picking.message_post(body="make from express delivery: %s" % express)
        return picking

    @api.model
    def _create_pickings(self):
        normal_lines = self.order_line.filtered(lambda l: not l.express_delivery)
        express_lines = self.order_line.filtered(lambda l: l.express_delivery)

        pickings = self.env['stock.picking']

        if normal_lines:
            picking_normal = self._create_picking_for_lines(normal_lines)
            pickings |= picking_normal

        if express_lines:
            picking_express = self._create_picking_for_lines(express_lines, express=True)
            pickings |= picking_express

        return pickings


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def _prepare_stock_moves(self):
        moves_vals = super()._prepare_stock_moves()
        for move_val in moves_vals:
            sale_line = self.sale_line_id
            if sale_line:
                move_val['sale_line_id'] = sale_line.id
        return moves_vals


class StockMove(models.Model):
    _inherit = 'stock.move'

    express_delivery = fields.Boolean(
        string='Express Delivery',
        related='sale_line_id.express_delivery',
        store=True,
    )
