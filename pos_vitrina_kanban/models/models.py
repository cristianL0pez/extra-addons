# -*- coding: utf-8 -*-

from odoo import models, fields, api

 class pos_vitrina_kanban(models.Model):
    _name = 'pos_vitrina_kanban.pos_vitrina_kanban_test'

     name = fields.Char()
     value = fields.Integer()
     value2 = fields.Float(compute="_value_pc", store=True)
     description = fields.Text()

     @api.depends('value')
     def _value_pc(self):
        self.value2 = float(self.value) / 100

# -*- coding: utf-8 -*-

#class pos_vitrina_kanban(models.Model):
   #_inherit = 'base'
   # Override the statement_ids field to make readonly at false
   # statement_ids = fields.One2many('account.bank.statement.line', 'pos_statement_id', string='Payments', readonly=False)    
