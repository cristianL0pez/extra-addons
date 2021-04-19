# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import UserError


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'


    webpay_commerce_code = fields.Char(
            string="Commerce Code"
        )
    webpay_private_key = fields.Binary(
            string="User Private Key",
        )
    webpay_public_cert = fields.Binary(
            string="User Public Cert",
        )
    webpay_cert = fields.Binary(
            string='Webpay Cert',
        )


    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        ICPSudo = self.env['ir.config_parameter'].sudo()
        webpay_commerce_code = ICPSudo.get_param(
                    'webpay.commerce_code')
        webpay_private_key = ICPSudo.get_param(
                    'webpay.private_key')
        webpay_public_cert = ICPSudo.get_param(
                    'webpay.public_cert')
        webpay_cert = ICPSudo.get_param(
                    'webpay.cert')
        res.update(
                webpay_commerce_code=webpay_commerce_code,
                webpay_private_key=webpay_private_key,
                webpay_public_cert=webpay_public_cert,
                webpay_cert=webpay_cert
            )
        return res

    @api.multi
    def set_values(self):
        super(ResConfigSettings, self).set_values()
        ICPSudo = self.env['ir.config_parameter'].sudo()
        ICPSudo.set_param('webpay.commerce_code',
                          self.webpay_commerce_code)
        ICPSudo.set_param('webpay.private_key',
                          self.webpay_private_key)
        ICPSudo.set_param('webpay.public_cert',
                          self.webpay_public_cert)
        ICPSudo.set_param('webpay.cert',
                          self.webpay_cert)
