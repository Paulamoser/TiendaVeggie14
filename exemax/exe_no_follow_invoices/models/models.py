# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountMove(models.Model):
	_inherit="account.move"

	def create(self,vals):
		res=super(AccountMove,self.with_context(tracking_disable=True)).create(vals)
		return res