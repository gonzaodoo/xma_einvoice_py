# -*- coding: utf-8 -*-
from odoo import fields, models


class l10n_xma_edi_tax_type(models.Model):
    _name = "l10n_xma.edi_tax_type"
    
    code = fields.Char()
    name = fields.Char()
    comments = fields.Text()
    country_id = fields.Many2one('res.country')