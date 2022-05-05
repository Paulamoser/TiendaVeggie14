# -*- coding: utf-8 -*-

from odoo import models, fields, api

class AccountMoveNew(models.Model):
	_inherit = "account.move"

	def create(self, vals):
		res = super(AccountMoveNew, self.with_context(tracking_disable=True)).create(vals)
		return res