# -*- coding: utf-'8' "-*-"
import logging
from odoo import api, models, fields
from odoo.tools import float_round, DEFAULT_SERVER_DATE_FORMAT
from odoo.tools.float_utils import float_compare, float_repr
from odoo.tools.translate import _

_logger = logging.getLogger(__name__)
try:
    from transbank.webpay.webpay_plus.transaction import *
    from transbank.webpay.webpay_plus import WebpayPlus
    from transbank.webpay.webpay_plus import webpay_plus_default_commerce_code, default_api_key
except Exception as e:
    _logger.warning("No Load transbank: %s" %str(e))




class PaymentAcquirerWebpay(models.Model):
    _inherit = 'payment.acquirer'

    @api.model
    def _get_providers(self,):
        providers = super(PaymentAcquirerWebpay, self)._get_providers()
        return providers

    provider = fields.Selection(
            selection_add=[('webpay', 'Webpay')]
        )
    webpay_commer_code = fields.Char(
            string="Commerce Code"
        )
    webpay_api_key_secret = fields.Char(
            string="Api Secret Key",
        )
    webpay_mode = fields.Selection(
            [
                ('normal', "Normal"),
                ('mall', "Normal Mall"),
                ('oneclick', "OneClick"),
                ('completa', "Completa"),
            ],
            string="Webpay Mode",
            default="normal"
        )
    environment = fields.Selection(
            selection_add=[('integ', 'Integración')],
        )

    @api.onchange('webpay_mode')
    def verificar_webpay_mode(self):
        if self.webpay_mode == 'mall':
            ICPSudo = self.env['ir.config_parameter'].sudo()
            if not ICPSudo.get_param(
                        'webpay.commerce_code')\
            or not ICPSudo.get_param(
                        'webpay.private_key')\
            or not ICPSudo.get_param(
                        'webpay.public_cert')\
            or not ICPSudo.get_param(
                        'webpay.cert'):
                raise UserError("No hay configuración definida para Mall")

    @api.multi
    def _get_feature_support(self):
        res = super(PaymentAcquirerWebpay, self)._get_feature_support()
        res['fees'].append('webpay')
        return res

    @api.multi
    def webpay_compute_fees(self, amount, currency_id, country_id):
        """ Compute paypal fees.

            :param float amount: the amount to pay
            :param integer country_id: an ID of a res.country, or None. This is
                                       the customer's country, to be compared to
                                       the acquirer company country.
            :return float fees: computed fees
        """
        if not self.fees_active:
            return 0.0
        country = self.env['res.country'].browse(country_id)
        if country and self.company_id.country_id.id == country.id:
            percentage = self.fees_dom_var
            fixed = self.fees_dom_fixed
        else:
            percentage = self.fees_int_var
            fixed = self.fees_int_fixed
        fees = (percentage / 100.0 * amount + fixed) / (1 - percentage / 100.0)
        return fees

    def _get_webpay_urls(self):
        url = URLS[self.environment]
        return url

    @api.multi
    def webpay_form_generate_values(self, values):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        values.update({
            'business': self.company_id.name,
            'item_name': values['reference'].split('-')[0],
            'item_number': values['reference'],
            'amount': values['amount'],
            'currency_code': values['currency'] and values['currency'].name or '',
            'address1': values.get('partner_address'),
            'city': values.get('partner_city'),
            'country': values.get('partner_country') and values.get('partner_country').code or '',
            'state': values.get('partner_state') and (values.get('partner_state').code or values.get('partner_state').name) or '',
            'email': values.get('partner_email'),
            'zip_code': values.get('partner_zip'),
            'first_name': values.get('partner_first_name'),
            'last_name': values.get('partner_last_name'),
            'return_url': base_url + '/payment/webpay/final'
        })
        return values

    @api.multi
    def webpay_get_form_action_url(self,):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        return base_url + '/payment/webpay/redirect'

    def get_WebPay_cert(self):
        webpay_cert = self.webpay_cert
        if self.webpay_mode == 'mall':
            ICPSudo = self.env['ir.config_parameter']
            webpay_cert = ICPSudo.get_param(
                        'webpay.cert')
        return b64decode(webpay_cert)

    def get_client(self,):
        if self.environment == 'test':
            WebpayPlus.configure_for_integration(webpay_plus_default_commerce_code, default_api_key)
        else:
            WebpayPlus.configure_for_production(self.webpay_commer_code, self.webpay_api_key_secret)
        return Transaction

    def details(self, client,  post):
        detail = client.factory.create('wsTransactionDetail')
        fees = post.get('fees', 0.0)
        if fees == '':
            fees = 0
        amount = (float(post['amount']) + float(fees))
        currency = self.env['res.currency'].search([
            ('name', '=', post.get('currency', 'CLP')),
        ])
        if self.force_currency and currency != self.force_currency_id:
            amount = currency._convert(
                                amount,
                                self.force_currency_id,
                                self.company_id,
                                datetime.now())
            currency = self.force_currency_id
        detail.amount = currency.round(amount)

        detail.commerceCode = self.webpay_commer_code
        detail.buyOrder = post['item_number']
        return [detail]

    """
    initTransaction

    Permite inicializar una transaccion en Webpay.
    Como respuesta a la invocacion se genera un token que representa en forma unica una transaccion.
    """
    def initTransaction(self, post):
        ICPSudo = self.env['ir.config_parameter'].sudo()
        base_url = ICPSudo.get_param('web.base.url')
        client = self.get_client()
        fees = post.get('fees', 0.0)
        if fees == '':
            fees = 0
        amount = (float(post['amount']) + float(fees))
        currency = self.env['res.currency'].search([
            ('name', '=', post.get('currency', 'CLP')),
        ])
        if self.force_currency and currency != self.force_currency_id:
            amount = currency._convert(
                                amount,
                                self.force_currency_id,
                                self.company_id,
                                datetime.now())
            currency = self.force_currency_id
        _logger.warning(amount)
        amount = currency.round(amount)
        _logger.warning(amount)
        response = client.create(
            post['item_name'],
            post['item_number'],
            amount,
            base_url + '/payment/webpay/return/'+str(self.id)
        )
        return response


class PaymentTxWebpay(models.Model):
    _inherit = 'payment.transaction'

    webpay_txn_type = fields.Selection([
            ('VD', 'Venta Debito'),
            ('VP', 'Venta Prepago'),
            ('VN', 'Venta Normal'),
            ('VC', 'Venta en cuotas'),
            ('SI', '3 cuotas sin interés'),
            ('S2', 'cuotas sin interés'),
            ('NC', 'N Cuotas sin interés'),
        ],
       string="Webpay Tipo Transacción")
    webpay_token = fields.Char(
            string="Webpay Token"
        )

    """
    getTransaction

    Permite obtener el resultado de la transaccion una vez que
    Webpay ha resuelto su autorizacion financiera.
    """
    @api.multi
    def getTransaction(self, acquirer_id, token):
        client = acquirer_id.get_client()
        response = client.commit(token)
        return response

    @api.multi
    def _webpay_form_get_invalid_parameters(self, data):
        invalid_parameters = []
        if data.session_id != self.reference:
            invalid_parameters.append(('reference', data.session_id,
                                       self.reference))
        amount = (self.amount + self.acquirer_id.webpay_compute_fees(self.amount, self.currency_id.id, self.partner_country_id.id))
        currency = self.currency_id
        if self.acquirer_id.force_currency and currency != self.acquirer_id.force_currency_id:
            amount = lambda price: currency._convert(
                                amount,
                                self.acquirer_id.force_currency_id,
                                self.acquirer_id.company_id,
                                datetime.now())
            currency = self.acquirer_id.force_currency_id
        amount = currency.round(amount)
        if data.amount != amount:
            invalid_parameters.append(('amount', data.amount, amount))

        return invalid_parameters

    @api.model
    def _webpay_form_get_tx_from_data(self, data):
        txn_id, reference = data.buy_order, data.session_id
        if not reference or not txn_id:
            error_msg = _('Webpay: received data with missing reference (%s) or txn_id (%s)') % (reference, txn_id)
            _logger.info(error_msg)
            raise ValidationError(error_msg)

        # find tx -> @TDENOTE use txn_id ?
        tx_ids = self.env['payment.transaction'].search([('reference', '=', reference)])
        if not tx_ids or len(tx_ids) > 1:
            error_msg = 'Webpay: received data for reference %s' % (reference)
            if not tx_ids:
                error_msg += '; no order found'
            else:
                error_msg += '; multiple order found'
            _logger.warning(error_msg)
            raise ValidationError(error_msg)
        return tx_ids[0]

    @api.multi
    def _webpay_form_validate(self, data):
        codes = {
                '0': 'Transacción aprobada.',
                '-1': 'Rechazo de transacción.',
                '-2': 'Transacción debe reintentarse.',
                '-3': 'Rechazo - Interno Transbank.',
                '-4': 'Rechazo - Rechazada por parte del emisor.',
                '-5': 'Rechazo - Transacción con riesgo de posible fraude.',
            }
        status = str(data.response_code)
        res = {
            'acquirer_reference': data.authorization_code,
            'webpay_txn_type': data.payment_type_code,
            'date_validate': data.transaction_date,
            'webpay_token': data.token,
        }
        if status in ['0']:
            _logger.info('Validated webpay payment for tx %s: set as done' % (self.reference))
            self._set_transaction_done()
        elif status in ['-6', '-7']:
            _logger.warning('Received notification for webpay payment %s: set as pending' % (self.reference))
            self._set_transaction_pending()
        elif status in ['-1', '-4']:
            self._set_transaction_cancel()
        else:
            error = 'Received unrecognized status for webpay payment %s: %s, set as error' % (self.reference, codes[status])
            _logger.warning(error)
        return self.write(res)

    def _confirm_so(self):
        if self.state not in ['cancel']:
            return super(PaymentTxWebpay, self)._confirm_so()
        self._set_transaction_cancel()
        return True

    """
    acknowledgeTransaction
    Indica  a Webpay que se ha recibido conforme el resultado de la transaccion
    """
    def acknowledgeTransaction(self, acquirer_id, token):
        client = acquirer_id.get_client()
        datos = client.status(token)
        return datos
