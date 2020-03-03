# © 2017 Niaga Solution - Edi Santoso <repodevs@gmail.com>
# Copyright (C) 2019 Serpent Consulting Services
# Copyright (C) 2019 Open Source Integrators
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class ResUsers(models.Model):
    _inherit = 'res.users'

    @api.model
    def create(self, vals):
        res = super().create(vals)
        if vals.get('default_operating_unit_id'):
            res.partner_id.operating_unit_ids = \
                [(4, res.default_operating_unit_id.id)]
        return res

    @api.multi
    def write(self, vals):
        if vals.get('default_operating_unit_id'):
            # Add the new OU
            self.partner_id.operating_unit_ids = \
                [(4, vals.get('default_operating_unit_id'))]
        return super().write(vals)

    @api.constrains('partner_id.operating_unit_ids',
                    'default_operating_unit_id')
    def check_partner_operating_unit(self):
        if self.default_operating_unit_id:
            if self.default_operating_unit_id not in self.operating_unit_ids:
                self.operating_unit_ids = [(4, self.default_operating_unit_id.id)]
            if self.partner_id.operating_unit_ids and \
                    self.default_operating_unit_id.id not in \
                    self.partner_id.operating_unit_ids.ids:
                raise UserError(_(
                    "The operating units of the partner must include the default "
                    "one of the user."))


    partner_allowed_by_ou_ids = fields.\
        Many2many('res.partner',
                  'partner_id_user_id',
                  'user_id',
                  'partner_id',
                  "Allowed Partners",
                  compute='_compute_allowed_partners')

    @api.depends('operating_unit_ids')
    def _compute_allowed_partners(self):
        import pdb; pdb.set_trace()
        cr = self._cr
        for user_id in self:
            if user_id.operating_unit_ids:
                partners = []
                query = """SELECT DISTINCT partner_id FROM operating_unit_partner_rel WHERE operating_unit_id IN %s"""
                params = [tuple(user_id.operating_unit_ids.ids)]
                cr.execute(query, params)
                query_results = cr.fetchall()
                ids = [item for t in query_results for item in t]
                if query_results:
                    user_id.partner_allowed_by_ou_ids = [(6, 0, ids)]
