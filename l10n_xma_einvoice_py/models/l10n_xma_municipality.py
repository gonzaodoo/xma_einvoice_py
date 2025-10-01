# -*- coding: utf-8 -*-
from odoo import fields, models


class l10n_xmam_unicipality(models.Model):
    _name = "l10n_xma.municipality"
    
    code = fields.Char()
    name = fields.Char()
    comments = fields.Text()
    country_id = fields.Many2one('res.country')