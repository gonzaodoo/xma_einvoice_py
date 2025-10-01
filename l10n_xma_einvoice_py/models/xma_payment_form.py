# -*- coding: utf-8 -*-
from odoo import fields, models


class xma_payment_form(models.Model):
    _name = "xma_payment.form"
    
    code = fields.Char()
    name = fields.Char()
    comments = fields.Text()
    country_id = fields.Many2one('res.country', required=True, index=True, help='Country in which this document is valid')