from odoo import fields, models, api
# from odoo.exceptions import ValidationError
import logging
_logger = logging.getLogger(__name__)

class SequenceMixin(models.AbstractModel):
    _inherit = 'sequence.mixin'

    def _get_last_sequence_temp(self, relaxed=False):
        self.ensure_one()
        if self._sequence_field not in self._fields or not self._fields[self._sequence_field].store:
            raise ValidationError(_('%s is not a stored field', self._sequence_field))
        where_string, param = self._get_last_sequence_domain(relaxed)
        if self.id or self.id.origin:
            where_string += " AND id != %(id)s "
            param['id'] = self.id or self.id.origin

        query = """
                       SELECT id FROM {table}
                       {where_string}
                       AND sequence_prefix = (SELECT sequence_prefix FROM {table} {where_string} ORDER BY id DESC LIMIT 1)
                       ORDER BY sequence_number DESC
                       LIMIT 1
               """.format(
            table=self._table,
            where_string=where_string,
            field=self._sequence_field,
        )

        self.flush([self._sequence_field, 'sequence_number', 'sequence_prefix'])
        self.env.cr.execute(query, param)
        return (self.env.cr.fetchone() or [None])[0]

    def _get_next_sequence(self):
        """get the next sequence. dont't change it
        """
        self.ensure_one()
        last_sequence = self._get_last_sequence_temp()
        new = not last_sequence
        if new:
            last_sequence = self._get_last_sequence_temp(relaxed=True) or self._get_starting_sequence()

        format, format_values = self._get_sequence_format_param(last_sequence)
        if new:
            format_values['seq'] = 0
            format_values['year'] = self[self._sequence_date_field].year % (10 ** format_values['year_length'])
            format_values['month'] = self[self._sequence_date_field].month
        format_values['seq'] = format_values['seq'] + 1

        self[self._sequence_field] = format.format(**format_values)
        self._compute_split_sequence()