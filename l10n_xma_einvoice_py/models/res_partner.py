# -*- coding: utf-8 -*-
from odoo import fields, models



class ResPartner(models.Model):
    _inherit = "res.partner"

    l10n_xma_taxpayer_type_id = fields.Many2one(
        'l10n_xma.taxpayer.type',
        string='Taxpayer Type'
    )    
    
   
    commercial_name = fields.Char()
    
    l10n_xma_external_number = fields.Char()
    
    l10n_xma_internal_number = fields.Char()
    
    l10n_xma_city_id = fields.Many2one(
        'res.city',string="Ciudad"
    )#fields.Many2one('res.city')
    
    l10n_xma_control_digit = fields.Char()
    
    l10n_xma_municipality_id = fields.Many2one(
        'l10n_xma.municipality', string='Municipio'
    )
    
    l10n_xma_is_taxpayer = fields.Boolean()
    
    l10n_xma_customer_operation_type = fields.Selection([ ('1', 'B2B'),
                                                ('2', 'B2C'),
                                                ('3', 'B2G'),
                                                ('4', 'B2F'),])
