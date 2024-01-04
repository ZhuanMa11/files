# -*- coding: utf-8 -*-
# Part of DTCloud. See LICENSE file for full copyright and licensing details.

from dtcloud import fields, models


class ServerAction(models.Model):
    _inherit = "ir.actions.server"

    usage = fields.Selection(selection_add=[
        ('base_automation', 'Automated Action')
    ], ondelete={'base_automation': 'cascade'})
