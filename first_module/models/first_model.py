from odoo import models, fields, api
from odoo.exceptions import ValidationError


class FirstModel(models.Model):
    _name = "first.model"
    _description = 'It is my first model'

    text = fields.Text(string='Text')
    check1 = fields.Boolean(string='Test 1')
    check2 = fields.Boolean(string='Test 2')
    check_all = fields.Boolean(string='Select all')
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

    boolean1 = fields.Boolean(string='1')
    boolean2 = fields.Boolean(string='2')
    boolean3 = fields.Boolean(string='3')
    boolean4 = fields.Boolean(string='4')
    boolean5 = fields.Boolean(string='5')
    boolean6 = fields.Boolean(string='6')
    boolean7 = fields.Boolean(string='7')
    boolean8 = fields.Boolean(string='8')
    boolean9 = fields.Boolean(string='9')
    check_all_int = fields.Integer(string='Check All as Integer', compute='_compute_check_all_int',
                                   inverse='_inverse_check_boxes',store=True)

    @api.depends('check_all')
    def _compute_check_all_int(self):
        """compute check_all row from bool to int and write result in new the row"""
        for rec in self:
            rec.check_all_int = 1 if rec.check_all else 0

    def _inverse_check_boxes(self):
        """inverse method to change check1 check2 inputs"""
        for rec in self:
            flag = bool(rec.check_all_int)
            rec.check1 = not flag
            rec.check2 = not flag

    @api.constrains('text')
    def _check_text_len(self):
        """check text length"""
        for record in self:
            if not record.text or len(record.text) < 5:
                raise ValidationError("Short text")

    @api.onchange('text')
    def _check_text_len_before_save(self):
        """check text length before save"""
        for record in self:
            if not record.text or len(record.text) < 5:
                return {
                    'warning': {
                        'title': "Error",
                        'message': "Short text len",
                    }
                }
