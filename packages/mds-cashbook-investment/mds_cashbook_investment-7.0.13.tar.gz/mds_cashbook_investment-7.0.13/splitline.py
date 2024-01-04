# -*- coding: utf-8 -*-
# This file is part of the cashbook-module from m-ds.de for Tryton.
# The COPYRIGHT file at the top level of this repository contains the
# full copyright notices and license terms.


from trytond.pool import PoolMeta, Pool
from trytond.model import fields
from trytond.pyson import Eval, Or, And
from trytond.report import Report
from trytond.modules.cashbook.line import STATES
from .mixin import SecondUomMixin
from .line import STATESQ1, DEPENDSQ1

STATESQ1A = {}
STATESQ1A.update(STATESQ1)
STATESQ1A['readonly'] = ~And(
    ~STATES['readonly'],
    Eval('bookingtype', '').in_(['spin', 'spout']),
    Or(
        Eval('feature', '') == 'asset',
        Eval('booktransf_feature', '') == 'asset',
    ))


class SplitLine(SecondUomMixin, metaclass=PoolMeta):
    __name__ = 'cashbook.split'

    quantity = fields.Numeric(
        string='Quantity', digits=(16, Eval('quantity_digits', 4)),
        states=STATESQ1A, depends=DEPENDSQ1)
    quantity_digits = fields.Function(fields.Integer(
        string='Digits', readonly=True, states={'invisible': True}),
        'on_change_with_quantity_digits')
    quantity_uom = fields.Function(fields.Many2One(
        string='Symbol', readonly=True, model_name='product.uom'),
        'on_change_with_quantity_uom')

    def get_rec_name(self, name):
        """ add quantities - if its a asset-cashbook
        """
        recname = super(SplitLine, self).get_rec_name(name)
        if self.line.cashbook.feature == 'asset':
            recname += '|%(quantity)s %(uom_symbol)s' % {
                'quantity': Report.format_number(
                    self.quantity or 0.0, None,
                    digits=self.quantity_digits),
                'uom_symbol': self.quantity_uom.symbol}
        return recname

    @fields.depends(
        'line', '_parent_line.cashbook', 'booktransf',
        '_parent_booktransf.feature', '_parent_booktransf.quantity_uom')
    def on_change_with_quantity_uom(self, name=None):
        """ get quantity-unit of asset
        """
        if self.line:
            if self.line.cashbook.feature == 'asset':
                if self.line.cashbook.quantity_uom:
                    return self.cashbook.quantity_uom.id
        if self.booktransf:
            if self.booktransf.feature == 'asset':
                if self.booktransf.quantity_uom:
                    return self.booktransf.quantity_uom.id

    @fields.depends(
        'line', '_parent_line.cashbook', 'booktransf',
        '_parent_booktransf.feature', '_parent_booktransf.quantity_digits')
    def on_change_with_quantity_digits(self, name=None):
        """ get digits from cashbook
        """
        if self.line:
            if self.line.cashbook.feature == 'asset':
                return self.line.cashbook.quantity_digits
        if self.booktransf:
            if self.booktransf.feature == 'asset':
                return self.booktransf.quantity_digits
        return 4

    @classmethod
    def add_2nd_unit_values(cls, values):
        """ extend create-values
        """
        Line2 = Pool().get('cashbook.line')

        values = super(SplitLine, cls).add_2nd_unit_values(values)
        line = Line2(values.get('line', None))

        if line:
            values.update(cls.add_2nd_quantity(
                values, line.cashbook.quantity_uom))
        return values

# end SplitLine
