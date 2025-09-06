from odoo import models, fields, api
from odoo.exceptions import ValidationError


class FirstModel(models.Model):
    _name = "first.model"
    _description = 'It is my first model'

    # text field
    text = fields.Text(string='Text')
    name = fields.Char(string='Name')
    html_content = fields.Html(string='HTML content')

    # bool fields
    check1 = fields.Boolean(string='Test 1')
    check2 = fields.Boolean(string='Test 2')
    check_all = fields.Boolean(string='Select all')
    boolean1 = fields.Boolean(string='1')
    boolean2 = fields.Boolean(string='2')
    boolean3 = fields.Boolean(string='3')
    boolean4 = fields.Boolean(string='4')
    boolean5 = fields.Boolean(string='5')
    boolean6 = fields.Boolean(string='6')
    boolean7 = fields.Boolean(string='7')
    boolean8 = fields.Boolean(string='8')
    boolean9 = fields.Boolean(string='9')

    show_boolean1 = fields.Boolean(string='show bool 1', compute=False, store=False, default=True)
    show_boolean2 = fields.Boolean(string='show bool 2', compute=False, store=False, default=True)
    show_boolean3 = fields.Boolean(string='show bool 3', compute=False, store=False, default=True)
    show_boolean4 = fields.Boolean(string='show bool 4', compute=False, store=False, default=True)
    show_boolean5 = fields.Boolean(string='show bool 5', compute=False, store=False, default=True)
    show_boolean6 = fields.Boolean(string='show bool 6', compute=False, store=False, default=True)
    show_boolean7 = fields.Boolean(string='show bool 7', compute=False, store=False, default=True)
    show_boolean8 = fields.Boolean(string='show bool 8', compute=False, store=False, default=True)
    show_boolean9 = fields.Boolean(string='show bool 9', compute=False, store=False, default=True)

    # selections fields
    select1 = fields.Selection([
        ('1', '1'),
        ('2', '2'),
        ('3', '3')
    ])
    select2 = fields.Selection([
        ('4', '4'),
        ('5', '5'),
        ('6', '6')
    ])

    amount = fields.Float(string='Amount')
    price = fields.Monetary(string='Price', currency_field='currency_id')

    # date fields
    target_date = fields.Date(string='Target date')
    target_datetime = fields.Datetime(string='Target datetime')

    # related fields
    currency_id = fields.Many2one('res.currency', string='Currency')
    line_ids = fields.One2many('first.model.line', 'first_model_id', string='Lines')
    tag_ids = fields.Many2many('first.model.tag', string='Tags')

    # binary fields
    binary = fields.Binary(string='Binary')

    # references field
    reference_field = fields.Reference(
        selection=[('res.partner', 'Partner'), ('res.users', 'User')],
        string='Reference'
    )
    json_data = fields.Json(string='Json data')
    menu_visible = fields.Boolean(default=True, compute='_compute_menu_visible', store=True)
    checked_order = fields.Char(string='Checked Order', default='')

    @api.onchange('select1', 'select2')
    def _change_bool_visible(self):
        visible_fields = set()

        select1_dict = {
            '1': ['1', '2', '3'],
            '2': ['4', '5', '6'],
            '3': ['7', '8', '9']
        }

        select2_dict = {
            '4': ['1', '4', '7'],
            '5': ['2', '5', '8'],
            '6': ['3', '6', '9']
        }
        if self.select1 in select1_dict:
            visible_fields.update(select1_dict[self.select1])
        if self.select2 in select2_dict:
            visible_fields.update(select2_dict[self.select2])

        for i in range(1, 10):
            setattr(self, f'show_boolean{i}', True)

        for i in visible_fields:
            setattr(self, f'show_boolean{i}', False)

    @api.onchange('check_all')
    def _onchange_check_all(self):
        """check check_all box"""
        for rec in self:
            if rec.check_all:
                rec.check1 = True
                rec.check2 = True
            else:
                rec.check1 = False
                rec.check2 = False

    @api.onchange('check1', 'check2')
    def _onchange_check1_check2(self):
        """check check_all box and add text to text field"""
        order = self.checked_order.split(',') if self.checked_order else []

        def update_order(checkbox_id, checked):
            if checked and checkbox_id not in order:
                order.append(checkbox_id)
            elif not checked and checkbox_id in order:
                order.remove(checkbox_id)

        update_order('check1', self.check1)
        update_order('check2', self.check2)

        self.checked_order = ','.join(order)

        parts = []
        for cb in order:
            if cb == 'check1':
                parts.append(f'[{self._fields["check1"].string}]')
            elif cb == 'check2':
                parts.append(f'{{{self._fields["check2"].string}}}')

        self.text = ' '.join(parts)

    @api.depends('target_datetime')
    def _compute_menu_visible(self):
        """compute menu visible"""
        for rec in self:
            if rec.menu_visible:
                rec.menu_visible = False
