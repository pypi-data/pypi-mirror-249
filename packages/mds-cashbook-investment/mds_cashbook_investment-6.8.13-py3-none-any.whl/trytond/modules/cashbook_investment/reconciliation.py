# -*- coding: utf-8 -*-
# This file is part of the cashbook-module from m-ds for Tryton.
# The COPYRIGHT file at the top level of this repository contains the
# full copyright notices and license terms.


from trytond.pool import PoolMeta, Pool
from trytond.model import fields
from trytond.pyson import Eval
from trytond.report import Report
from decimal import Decimal


class Reconciliation(metaclass=PoolMeta):
    __name__ = 'cashbook.recon'

    start_quantity = fields.Numeric(
        string='Start Quantity', readonly=True,
        digits=(16, Eval('quantity_digits', 4)),
        states={
            'required': Eval('feature', '') == 'asset',
            'invisible': Eval('feature', '') != 'asset',
        }, depends=['quantity_digits', 'feature'])
    end_quantity = fields.Numeric(
        string='End Quantity', readonly=True,
        digits=(16, Eval('quantity_digits', 4)),
        states={
            'required': Eval('feature', '') == 'asset',
            'invisible': Eval('feature', '') != 'asset',
        }, depends=['quantity_digits', 'feature'])
    quantity_digits = fields.Function(fields.Integer(
        string='Quantity Digits'), 'on_change_with_quantity_digits')
    quantity_uom = fields.Function(fields.Many2One(
        string='Symbol', readonly=True, model_name='product.uom'),
        'on_change_with_quantity_uom')

    def get_rec_name(self, name):
        """ add quantities - if its a asset-cashbook
        """
        recname = super(Reconciliation, self).get_rec_name(name)
        if self.cashbook.feature == 'asset':
            recname += ' '.join([
                ' |',
                Report.format_number(
                    self.start_quantity or 0.0, None,
                    digits=self.quantity_digits),
                getattr(self.quantity_uom, 'symbol', '-'),
                '-',
                Report.format_number(
                    self.end_quantity or 0.0, None,
                    digits=self.quantity_digits),
                getattr(self.quantity_uom, 'symbol', '-')
                ])
        return recname

    @fields.depends('cashbook', '_parent_cashbook.quantity_uom')
    def on_change_with_quantity_uom(self, name=None):
        """ get quantity-unit of asset
        """
        if self.cashbook:
            if self.cashbook.quantity_uom:
                return self.cashbook.quantity_uom.id

    @fields.depends('cashbook', '_parent_cashbook.quantity_digits')
    def on_change_with_quantity_digits(self, name=None):
        """ quantity_digits of cashbook
        """
        if self.cashbook:
            return self.cashbook.quantity_digits
        else:
            return 4

    @classmethod
    def default_start_quantity(cls):
        return Decimal('0.0')

    @classmethod
    def default_end_quantity(cls):
        return Decimal('0.0')

    @classmethod
    def get_values_wfedit(cls, reconciliation):
        """ get values for 'to_write' in wf-edit
        """
        values = super(Reconciliation, cls).get_values_wfedit(reconciliation)
        values.update({
            'start_quantity': Decimal('0.0'),
            'end_quantity': Decimal('0.0')})
        return values

    @classmethod
    def get_values_wfcheck(cls, reconciliation):
        """ get values for 'to_write' in wf-check
        """
        Line = Pool().get('cashbook.line')

        values = super(Reconciliation, cls).get_values_wfcheck(reconciliation)
        if reconciliation.cashbook.feature != 'asset':
            return values

        if reconciliation.predecessor:
            values['start_quantity'] = reconciliation.predecessor.end_quantity
        else:
            values['start_quantity'] = Decimal('0.0')
        values['end_quantity'] = values['start_quantity']

        # add quantities of new lines
        if 'lines' in values.keys():
            if len(values['lines']) != 1:
                raise ValueError('invalid number of values')

            lines_records = Line.browse(values['lines'][0][1])
            values['end_quantity'] += sum([
                    x.quantity_credit - x.quantity_debit
                    for x in lines_records
                ])

        # add quantities of already linked lines
        values['end_quantity'] += sum([
                x.quantity_credit - x.quantity_debit
                for x in reconciliation.lines])

        return values

# end Reconciliation
