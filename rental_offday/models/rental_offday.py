# Part of rental-vertical See LICENSE file for full copyright and licensing details.

import time
from datetime import timedelta
from odoo import api, fields, models, exceptions, _


class RentalOffday(models.Model):
    _name = 'rental.offday'

    add_order_line_id = fields.Many2one(
        'sale.order.line',
        string='Order Line',
        ondelete='set null',
    )

    fixed_order_line_id = fields.Many2one(
        'sale.order.line',
        string='Order Line',
        ondelete='set null',
    )

    name = fields.Char(
        'Description'
    )

    date = fields.Date(
        'Date',
        required=True,
    )

    @api.multi
    @api.constrains('fixed_order_line_id', 'date', 'add_order_line_id')
    def _check_date(self):
        for line in self:
            domain = [
                ('date', '=', line.date),
                ('id', '!=', line.id),
                ('fixed_order_line_id', '=', line.fixed_order_line_id.id),
            ]
            if line.fixed_order_line_id:
                domain.append('|')
                domain.append(('fixed_order_line_id', '=', line.fixed_order_line_id.id))
                domain.append(('add_order_line_id', '=', line.fixed_order_line_id.id))
            if line.add_order_line_id:
                domain.append('|')
                domain.append(('fixed_order_line_id', '=', line.add_order_line_id.id))
                domain.append(('add_order_line_id', '=', line.add_order_line_id.id))
            lines = self.search_count(domain)
            if lines:
                raise exceptions.ValidationError(
                    _('You have already created the off-day "%s".') % line.date)