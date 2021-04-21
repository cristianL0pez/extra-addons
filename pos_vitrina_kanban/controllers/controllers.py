# -*- coding: utf-8 -*-
from odoo import http

 class PosVitrinaKanban(http.Controller):
     @http.route('/pos_vitrina_kanban/pos_vitrina_kanban/', auth='public')
     def index(self, **kw):
         return "Hello, world"

     @http.route('/pos_vitrina_kanban/pos_vitrina_kanban/objects/', auth='public')
     def list(self, **kw):
        return http.request.render('pos_vitrina_kanban.listing', {
            'root': '/pos_vitrina_kanban/pos_vitrina_kanban',
            'objects': http.request.env['pos_vitrina_kanban.pos_vitrina_kanban'].search([]),
        })

     @http.route('/pos_vitrina_kanban/pos_vitrina_kanban/objects/<model("pos_vitrina_kanban.pos_vitrina_kanban"):obj>/', auth='public')
     def object(self, obj, **kw):
         return http.request.render('pos_vitrina_kanban.object', {
             'object': obj
         })