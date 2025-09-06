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

    # digit fields
    # check_all_int = fields.Integer(string='Check All as Integer', compute='_compute_check_all_int',
    # inverse='_inverse_check_boxes', store=True)
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

    @api.onchange('check_all')
    def _onchange_check_all(self):
        if self.check_all:
            self.check1 = True
            self.check2 = True
        else:
            self.check1 = False
            self.check2 = False

    @api.onchange('check1', 'check2')
    def _onchange_check1_check2(self):
        if self.check1 and self.check2:
            self.check_all = True
        else:
            if self.check_all:
                self.check_all = False

    @api.depends('target_datetime')
    def _compute_menu_visible(self):
        """compute menu visible"""
        for rec in self:
            if rec.menu_visible:
                rec.menu_visible = False

    """@api.depends('check_all')
    def _compute_check_all_int(self):
        ""compute check_all row from bool to int and write result in new the row""
        for rec in self:
            rec.check_all_int = 1 if rec.check_all else 0

    def _inverse_check_boxes(self):
        ""inverse method to change check1 check2 inputs""
        for rec in self:
            flag = bool(rec.check_all_int)
            rec.check1 = not flag
            rec.check2 = not flag

    @api.constrains('text')
    def _check_text_len(self):
        ""check text length""
        for record in self:
            if not record.text or len(record.text) < 5:
                raise ValidationError("Short text")

    @api.onchange('text')
    def _check_text_len_before_save(self):
        ""check text length before save""
        for record in self:
            if not record.text or len(record.text) < 5:
                return {
                    'warning': {
                        'title': "Error",
                        'message': "Short text len",
                    }
                }"""
