# © 2017 Niaga Solution - Edi Santoso <repodevs@gmail.com>
# Copyright (C) 2019 Serpent Consulting Services
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import api, fields, models


class ResPartner(models.Model):

    _inherit = 'res.partner'

    @api.model
    def operating_unit_default_get(self, uid2=False):
        if not uid2:
            uid2 = self._uid
        user = self.env['res.users'].browse(uid2)
        return user.default_operating_unit_id

    @api.model
    def _default_operating_unit(self):
        return self.operating_unit_default_get()

    @api.model
    def _default_operating_units(self):
        return self._default_operating_unit()

    operating_unit_ids = fields.Many2many(
        'operating.unit', 'operating_unit_partner_rel',
        'partner_id', 'operating_unit_id',
        'Operating Units', default=lambda self: self._default_operating_units()
    )

    @api.depends('operating_unit_ids')
    def _recompute_allowed_partners(self):
        self.env.user.sudo()._compute_allowed_partners()

    # @api.multi
    # def write(self, vals):
    #     for partner_id in self:
    #         if vals.get('operating_unit_ids', False)[0][2]:
    #             new_list = partner_id.env.user.partner_allowed_by_ou_ids.ids
    #             if partner_id.id not in new_list:
    #                 new_list.append(partner_id.id)
    #                 partner_id.env.user.partner_allowed_by_ou_ids = [(6, 0,  new_list)]
    #     return super().write(vals)

    # Code for Storing Users on Partners
    # Ran into issue creating Recored Rule this way

    # user_allowed_by_ou_ids = fields.Many2many('res.users', 'user_id_partner_id', 'partner_id', 'user_id', "Allowed users", compute='_compute_allowed_users', store=True)

    # @api.depends('operating_unit_ids')
    # def _compute_allowed_users(self):
    #     cr = self._cr
    #     for partner_id in self:
    #         if partner_id.operating_unit_ids:
    #             users = []
    #             query = """SELECT user_id FROM operating_unit_users_rel WHERE operating_unit_id IN %s""" % partner_id.operating_unit_ids.ids
    #             cr.execute(query)
    #             query_results = cr.dictfetchall()
    #             partner_id.user_allowed_by_ou_ids = query_results.ids
