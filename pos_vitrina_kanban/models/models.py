# -*- coding: utf-8 -*-

#from odoo import models, fields, api

# class pos_vitrina_kanban(models.Model):
#     _name = 'pos_vitrina_kanban.pos_vitrina_kanban'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100


# -*- coding: utf-8 -*-
from odoo import models, fields, api

class posdata(models.Model):
    _inherit = 'pos.order'
