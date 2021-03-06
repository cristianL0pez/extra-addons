# -*- coding: utf-8 -*-
from odoo import models, api, fields
from odoo.tools.translate import _
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)


class IRSequence(models.Model):
    _inherit = 'ir.sequence'

    @api.onchange('dte_caf_ids')
    def verificar_pos(self):
        if self.is_dte and self.sii_document_class_id.es_boleta():
            context = dict(self._context or {})
            id = context.get('default_sequence_id') #Al parecer se complica el contexto y se pierde la referencia id
            if not id:
                return
            query = [
                ('rescue', '=', False),
                ('state', 'not in', ['closed']),
                '|',
                ('config_id.secuencia_boleta', '=', id),
                ('config_id.secuencia_boleta_exenta', '=', id),
                ]
            if self.env['pos.session'].sudo().search(query):
                raise UserError("No puede Editar CAF de Una sesión de Punto de Ventas abierto. Cierre y contabiliza el punto de ventas primero")

    def solicitar_caf(self):
        self.verificar_pos()
        return super(IRSequence, self).solicitar_caf()
