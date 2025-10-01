from odoo import fields,models

class ResCountry(models.Model):
    _inherit="res.country"

    l10n_xma_country_code = fields.Char(
        string="Codigo de Pais"
    )