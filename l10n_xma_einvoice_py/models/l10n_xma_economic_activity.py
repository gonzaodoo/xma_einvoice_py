# -*- coding: utf-8 -*-
from odoo import fields, models


class L10nXmaEdiLegalStatus(models.Model):
    _name = "l10n_xma.economic_activity"
    
    code = fields.Char()
    name = fields.Char()
    comments = fields.Text()
    country_id = fields.Many2one('res.country')
    res_company = fields.Many2one('res.company',
        readonly=True,
        index=True,
        auto_join=True,
        ondelete="cascade",
        check_company=True,)
