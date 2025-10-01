# -*- coding: utf-8 -*-
from odoo import fields, models



class ResPartner(models.Model):
    _inherit = "res.company"
    
    l10n_xma_economic_activity_campany_id = fields.One2many('l10n_xma.economic_activity','res_company')