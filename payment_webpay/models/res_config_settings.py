# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import UserError


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    webpay_mall = fields.Boolean(
        string="Activar modo MALL",
    )
    webpay_commerce_code = fields.Char(
            string="Commerce Code"
        )
    webpay_api_key_secret = fields.Char(
            string='Webpay Api Secret Key',
        )


    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        ICPSudo = self.env['ir.config_parameter'].sudo()
        webpay_commerce_code = ICPSudo.get_param(
                    'webpay.commerce_code')
        webpay_api_key_secret = ICPSudo.get_param(
                    'webpay.api_key_secret')
        webpay_mall = ICPSudo.get_param(
                    'webpay.mall')
        res.update(
                webpay_commerce_code=webpay_commerce_code,
                webpay_api_key_secret=webpay_api_key_secret,
                webpay_mall=webpay_mall
            )
        return res

    @api.multi
    def set_values(self):
        super(ResConfigSettings, self).set_values()
        ICPSudo = self.env['ir.config_parameter'].sudo()
        ICPSudo.set_param('webpay.commerce_code',
                          self.webpay_commerce_code)
        ICPSudo.set_param('webpay.api_key_secret',
                          self.webpay_api_key_secret)
        ICPSudo.set_param('webpay.mall',
                          self.webpay_mall)
