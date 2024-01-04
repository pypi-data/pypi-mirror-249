# -*- coding: utf-8 -*-
# This file is part of the cashbook-module from m-ds.de for Tryton.
# The COPYRIGHT file at the top level of this repository contains the
# full copyright notices and license terms.

from trytond.model import fields
from trytond.pyson import Eval, Bool, Or
from trytond.pool import Pool
from trytond.exceptions import UserError
from trytond.i18n import gettext
from trytond.modules.product.uom import uom_conversion_digits
from trytond.modules.cashbook.mixin import STATES, DEPENDS
from decimal import Decimal

STATESQ = {}
STATESQ.update(STATES)
DEPENDSQ = []
DEPENDSQ.extend(DEPENDS)


class SecondUomMixin(object):
    """ two fields for second uom: quantity, rate
    """
    __slots__ = ()

    quantity_2nd_uom = fields.Numeric(
        string='Quantity Second UOM',
        digits=(16, Eval('quantity2nd_digits', 4)),
        states={
            'readonly': Or(
                STATESQ['readonly'],
                ~Bool(Eval('quantity2nd'))),
            'required': Bool(Eval('quantity2nd')),
            'invisible': ~Bool(Eval('quantity2nd'))},
        depends=DEPENDSQ+['quantity2nd_digits', 'quantity2nd'])
    factor_2nd_uom = fields.Function(fields.Numeric(
        string='Conversion factor',
        help='Conversion factor between the units of the ' +
        'participating cash books.',
        digits=uom_conversion_digits,
        states={
            'readonly': Or(
                STATESQ['readonly'],
                ~Bool(Eval('quantity2nd'))),
            'required': Bool(Eval('quantity2nd')),
            'invisible': ~Bool(Eval('quantity2nd'))},
        depends=DEPENDSQ+['quantity2nd_digits', 'quantity2nd']),
        'on_change_with_factor_2nd_uom', setter='set_factor_2nd_uom')

    quantity2nd = fields.Function(fields.Many2One(
        model_name='product.uom',
        string="2nd UOM", readonly=True), 'on_change_with_quantity2nd')
    quantity2nd_digits = fields.Function(fields.Integer(
        string='2nd UOM Digits', readonly=True),
        'on_change_with_quantity2nd_digits')

    def quantize_quantity(self, value):
        """ quantize for line-quantity
        """
        return Decimal(value).quantize(
            Decimal(Decimal(1) / 10 ** self.quantity_digits))

    @classmethod
    def add_2nd_quantity(cls, values, from_uom):
        """ add second uom quantity if missing
        """
        pool = Pool()
        UOM = pool.get('product.uom')
        Cashbook = pool.get('cashbook.book')

        booktransf = values.get('booktransf', None)
        quantity = values.get('quantity', None)
        quantity_2nd_uom = values.get('quantity_2nd_uom', None)

        if (quantity is not None) and (booktransf is not None) and \
                (from_uom is not None):
            if quantity_2nd_uom is None:
                booktransf = Cashbook(booktransf)
                if booktransf.quantity_uom:
                    if from_uom.id != booktransf.quantity_uom.id:
                        # deny impossible transfer
                        if from_uom.category.id != \
                                booktransf.quantity_uom.category.id:
                            raise UserError(gettext(
                                'cashbook_investment.msg_uomcat_mismatch',
                                cat1=from_uom.category.rec_name,
                                cat2=booktransf.quantity_uom.category.rec_name))

                        values['quantity_2nd_uom'] = Decimal(UOM.compute_qty(
                                from_uom,
                                float(quantity),
                                booktransf.quantity_uom,
                                round=False,
                            )).quantize(Decimal(
                                    Decimal(1) /
                                    10 ** booktransf.quantity_digits))
        return values

    @classmethod
    def set_factor_2nd_uom(cls, lines, name, value):
        """ compute quantity_2nd_uom, write to db
        """
        Line2 = Pool().get(cls.__name__)

        to_write = []

        if name != 'factor_2nd_uom':
            return

        for line in lines:
            if line.booktransf is None:
                continue
            if (line.cashbook.quantity_uom is None) or \
                    (line.booktransf.quantity_uom is None):
                continue

            if line.cashbook.quantity_uom.id == line.booktransf.quantity_uom.id:
                continue

            to_write.extend([
                [line],
                {
                    'quantity_2nd_uom': line.quantize_quantity(
                        line.booktransf.quantity_uom.round(
                            float(line.quantity * value))
                        ),
                }])

        if len(to_write) > 0:
            Line2.write(*to_write)

    @fields.depends(
        'booktransf', '_parent_booktransf.quantity_uom',
        'quantity_uom', 'quantity_digits', 'quantity',
        'quantity_2nd_uom', 'factor_2nd_uom')
    def on_change_booktransf(self):
        """ update quantity_2nd_uom
        """
        self.on_change_factor_2nd_uom()

    @fields.depends(
        'booktransf', '_parent_booktransf.quantity_uom',
        'quantity_uom', 'quantity_digits', 'quantity',
        'quantity_2nd_uom', 'factor_2nd_uom')
    def on_change_quantity(self):
        """ update quantity_2nd_uom
        """
        self.on_change_factor_2nd_uom()

    @fields.depends(
        'booktransf', '_parent_booktransf.quantity_uom',
        'quantity_uom', 'quantity_digits', 'quantity',
        'quantity_2nd_uom', 'factor_2nd_uom')
    def on_change_factor_2nd_uom(self):
        """ update quantity_2nd_uom + factor_2nd_uom
        """
        UOM = Pool().get('product.uom')

        if (self.quantity is None) or (self.booktransf is None):
            self.quantity_2nd_uom = None
            self.factor_2nd_uom = None
            return
        if (self.booktransf.quantity_uom is None) or \
                (self.quantity_uom is None):
            return

        if self.factor_2nd_uom is None:
            # no factor set, use factor of target-uom
            self.quantity_2nd_uom = self.quantize_quantity(
                UOM.compute_qty(
                    self.quantity_uom,
                    float(self.quantity),
                    self.booktransf.quantity_uom,
                    round=False))
            if self.quantity != Decimal('0.0'):
                self.factor_2nd_uom = (
                        self.quantity_2nd_uom / self.quantity
                    ).quantize(Decimal(
                        Decimal(1) / 10 ** uom_conversion_digits[1]))
        else:
            self.quantity_2nd_uom = self.quantize_quantity(
                    self.quantity * self.factor_2nd_uom)

    @fields.depends('quantity', 'quantity_2nd_uom', 'factor_2nd_uom')
    def on_change_quantity_2nd_uom(self):
        """ update factor_2nd_uom by quantity
        """
        self.factor_2nd_uom = self.on_change_with_factor_2nd_uom()

    @fields.depends('quantity', 'quantity_2nd_uom')
    def on_change_with_factor_2nd_uom(self, name=None):
        """ get factor from uom
        """
        if (self.quantity is not None) and (self.quantity_2nd_uom is not None):
            if self.quantity != Decimal('0.0'):
                exp = Decimal(Decimal(1) / 10 ** uom_conversion_digits[1])
                return (self.quantity_2nd_uom / self.quantity).quantize(exp)

    @fields.depends(
        'booktransf', '_parent_booktransf.quantity_uom', 'quantity_uom')
    def on_change_with_quantity2nd(self, name=None):
        """ uom of transfer-target
        """
        if self.booktransf:
            if self.quantity_uom:
                if self.booktransf.quantity_uom:
                    if self.quantity_uom.id != \
                            self.booktransf.quantity_uom.id:
                        return self.booktransf.quantity_uom.id

    @fields.depends('booktransf', '_parent_booktransf.quantity_digits')
    def on_change_with_quantity2nd_digits(self, name=None):
        """ uom of transfer-target
        """
        if self.booktransf:
            return self.booktransf.quantity_digits
        else:
            return 2

# end SecondUomMixin
