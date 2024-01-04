# -*- coding: utf-8 -*-
# This file is part of the cashbook-module from m-ds.de for Tryton.
# The COPYRIGHT file at the top level of this repository contains the
# full copyright notices and license terms.

from decimal import Decimal
from sql.conditionals import Coalesce, Case
from sql.aggregate import Sum
from trytond.model import fields
from trytond.pool import PoolMeta, Pool
from trytond.pyson import Eval, Or, If, And
from trytond.exceptions import UserError
from trytond.i18n import gettext
from trytond.report import Report
from trytond.transaction import Transaction
from trytond.modules.cashbook.line import STATES, DEPENDS
from .mixin import SecondUomMixin

DEF_NONE = None

STATESQ1 = {
    'invisible': And(
        Eval('feature', '') != 'asset',
        Eval('booktransf_feature', '') != 'asset'),
    'required': Or(
        Eval('feature', '') == 'asset',
        Eval('booktransf_feature', '') == 'asset'),
    'readonly': Or(
        STATES['readonly'],
        Eval('bookingtype', '').in_(['spin', 'spout'])),
    }
DEPENDSQ1 = ['feature', 'booktransf_feature', 'quantity_digits', 'bookingtype']
DEPENDSQ1.extend(DEPENDS)

STATESQ1B = {}
STATESQ1B.update(STATESQ1)
STATESQ1B['invisible'] = And(
        Eval('feature', '') != 'asset',
        Eval('booktransf_feature', '') != 'asset',
        ~Eval('splitline_has_quantity', False))


STATESQ2 = {
    'invisible': Eval('feature', '') != 'asset',
    'required': Eval('feature', '') == 'asset'}
DEPENDSQ2 = ['feature', 'quantity_digits', 'bookingtype']


class Line(SecondUomMixin, metaclass=PoolMeta):
    __name__ = 'cashbook.line'

    quantity = fields.Numeric(
        string='Quantity',
        digits=(16, Eval('quantity_digits', 4)),
        states=STATESQ1B, depends=DEPENDSQ1+['splitline_has_quantity'])
    quantity_credit = fields.Numeric(
        string='Quantity Credit',
        digits=(16, Eval('quantity_digits', 4)), readonly=True,
        states=STATESQ2, depends=DEPENDSQ2)
    quantity_debit = fields.Numeric(
        string='Quantity Debit',
        digits=(16, Eval('quantity_digits', 4)), readonly=True,
        states=STATESQ2, depends=DEPENDSQ2)

    quantity_digits = fields.Function(fields.Integer(
        string='Digits', readonly=True, states={'invisible': True}),
        'on_change_with_quantity_digits')
    quantity_uom = fields.Function(fields.Many2One(
        string='Symbol', readonly=True, model_name='product.uom'),
        'on_change_with_quantity_uom')
    asset_rate = fields.Function(fields.Numeric(
        string='Rate', readonly=True,
        digits=(16, If(
            Eval('currency_digits', 2) > Eval('quantity_digits', 2),
            Eval('currency_digits', 2), Eval('quantity_digits', 2))),
        states={'invisible': Eval('feature', '') != 'asset'},
        depends=['currency_digits', 'quantity_digits', 'feature']),
        'on_change_with_asset_rate')
    quantity_balance = fields.Function(fields.Numeric(
        string='Quantity',
        digits=(16, Eval('quantity_digits', 4)), readonly=True,
        help='Number of shares in the cashbook up to the current ' +
        'row if the default sort applies.',
        states={'invisible': Eval('feature', '') != 'asset'},
        depends=['quantity_digits', 'feature']),
        'on_change_with_quantity_balance')
    splitline_has_quantity = fields.Function(fields.Boolean(
        string='has quantity', readonly=True, states={'invisible': True}),
        'on_change_with_splitline_has_quantity')

    # performance
    current_value = fields.Function(fields.Numeric(
        string='Value',
        help='Valuation of the investment based on the current ' +
        'stock market price.',
        readonly=True, digits=(16, Eval('currency_digits', 2)),
        states={'invisible': Eval('feature', '') != 'asset'},
        depends=['currency_digits', 'feature']),
        'on_change_with_current_value')
    diff_amount = fields.Function(fields.Numeric(
        string='Difference',
        help='Difference between acquisition value and current value',
        readonly=True, digits=(16, Eval('currency_digits', 2)),
        states={'invisible': Eval('feature', '') != 'asset'},
        depends=['currency_digits', 'feature']), 'on_change_with_diff_amount')
    diff_percent = fields.Function(fields.Numeric(
        string='Percent',
        help='percentage performance since acquisition',
        readonly=True, digits=(16, Eval('currency_digits', 2)),
        states={'invisible': Eval('feature', '') != 'asset'},
        depends=['currency_digits', 'feature']), 'on_change_with_diff_percent')

    trade_fee = fields.Function(fields.Numeric(
        string='Fee',
        help='Trading fee for the current booking line.',
        readonly=True, digits=(16, Eval('currency_digits', 2)),
        states={'invisible': Eval('feature', '') != 'asset'},
        depends=['currency_digits', 'feature']),
        'get_yield_data', searcher='search_trade_fee')
    asset_dividend = fields.Function(fields.Numeric(
        string='Dividend',
        help='Dividend received at the current booking line.',
        readonly=True, digits=(16, Eval('currency_digits', 2)),
        states={'invisible': Eval('feature', '') != 'asset'},
        depends=['currency_digits', 'feature']),
        'get_yield_data', searcher='search_asset_dividend')
    asset_gainloss = fields.Function(fields.Numeric(
        string='Profit/Loss',
        help='Profit or loss on sale on the current booking line.',
        readonly=True, digits=(16, Eval('currency_digits', 2)),
        states={'invisible': Eval('feature', '') != 'asset'},
        depends=['currency_digits', 'feature']),
        'get_yield_data', searcher='search_asset_gainloss')

    @classmethod
    def get_gainloss_data_sql(cls):
        """ query for gain/loss on sell of shares
        """
        pool = Pool()
        AssetSetting = pool.get('cashbook.assetconf')
        SplitLine = pool.get('cashbook.split')
        tab_line = cls.__table__()
        tab_mvsp_counterpart = cls.__table__()
        tab_mvmv_counterpart = cls.__table__()
        tab_spmv_counterpart = cls.__table__()
        tab_mv_spline = SplitLine.__table__()

        cfg1 = AssetSetting.get_singleton()
        gainloss_book = getattr(getattr(
            cfg1, 'gainloss_book', None), 'id', None)

        tab_assetline = cls.search([
            ('cashbook.btype.feature', '=', 'asset'),
            ], query=True)

        query = tab_line.join(
                tab_assetline,
                condition=(tab_assetline.id == tab_line.id),

            ).join(
                tab_mvsp_counterpart,
                # [MV-SP] transfer booking,
                # select counterpart [1] - a split-booking
                condition=tab_line.bookingtype.in_(['mvin', 'mvout']) &
                ((tab_line.reference == tab_mvsp_counterpart.id) |
                    (tab_line.id == tab_mvsp_counterpart.reference)) &
                (tab_mvsp_counterpart.bookingtype.in_(['spin', 'spout'])),
                type_='LEFT OUTER',
            ).join(
                tab_mv_spline,
                # [MV-SP] line is linked to split-booking-line
                # of counterpart [1]
                condition=(tab_mv_spline.line == tab_mvsp_counterpart.id) &
                (tab_mv_spline.splittype == 'tr') &
                (tab_mv_spline.booktransf != DEF_NONE) &
                (tab_mv_spline.booktransf == gainloss_book),
                type_='LEFT OUTER',

            ).join(
                tab_spmv_counterpart,
                # [SP-MV] split booking, select counterpart [1]
                # - a transfer-booking
                condition=tab_line.bookingtype.in_(['spin', 'spout']) &
                ((tab_line.reference == tab_spmv_counterpart.id) |
                    (tab_line.id == tab_spmv_counterpart.reference)) &
                tab_spmv_counterpart.bookingtype.in_(['mvin', 'mvout']) &
                (tab_spmv_counterpart.cashbook == gainloss_book),
                type_='LEFT OUTER',

            ).join(
                tab_mvmv_counterpart,
                # [MV-MV] transfer booking
                condition=tab_line.bookingtype.in_(['mvin', 'mvout']) &
                ((tab_mvmv_counterpart.reference == tab_line.id) |
                    (tab_mvmv_counterpart.id == tab_line.reference)) &
                tab_mvmv_counterpart.bookingtype.in_(['mvin', 'mvout']) &
                (tab_mvmv_counterpart.cashbook == gainloss_book),
                type_='LEFT OUTER',
            ).select(
                tab_line.id,
                (Coalesce(
                    tab_mvmv_counterpart.credit - tab_mvmv_counterpart.debit,
                    Case(
                        (tab_line.bookingtype == 'mvin', tab_mv_spline.amount),
                        (tab_line.bookingtype == 'mvout',
                            tab_mv_spline.amount * Decimal('-1.0'))),
                    Case(
                        (tab_mvsp_counterpart.cashbook == gainloss_book,
                            tab_line.debit - tab_line.credit)),
                    tab_spmv_counterpart.credit - tab_spmv_counterpart.debit,
                    Decimal('0.0'),
                ) * Decimal('-1.0')).as_('gainloss'),
                tab_line.cashbook)
        return (tab_line, query)

    @classmethod
    def get_yield_data_sql(cls):
        """ query for fee, dividend, gain/loss
        """
        pool = Pool()
        AssetSetting = pool.get('cashbook.assetconf')
        SplitLine = pool.get('cashbook.split')
        tab_line = cls.__table__()
        tab_inout_fee = cls.__table__()
        tab_inout_divi = cls.__table__()
        tab_mv_counterpart = cls.__table__()
        tab_mv_spline_fee = SplitLine.__table__()
        tab_mv_spline_divi = SplitLine.__table__()
        tab_spline_fee = SplitLine.__table__()
        tab_spline_divi = SplitLine.__table__()

        cfg1 = AssetSetting.get_singleton()
        fee_category = getattr(getattr(cfg1, 'fee_category', None), 'id', None)
        dividend_category = getattr(getattr(
            cfg1, 'dividend_category', None), 'id', None)

        tab_assetline = cls.search([
            ('cashbook.btype.feature', '=', 'asset'),
            ], query=True)

        query = tab_line.join(
                tab_assetline,
                condition=(tab_assetline.id == tab_line.id),
            ).join(
                tab_inout_fee,
                # [INOUT] fee, local booked
                condition=(tab_inout_fee.id == tab_line.id) &
                tab_inout_fee.bookingtype.in_(['in', 'out']) &
                (tab_inout_fee.category != DEF_NONE) &
                (tab_inout_fee.category == fee_category),
                type_='LEFT OUTER',
            ).join(
                tab_inout_divi,
                # [INOUT] dividend, local booked
                condition=(tab_inout_divi.id == tab_line.id) &
                tab_inout_divi.bookingtype.in_(['in', 'out']) &
                (tab_inout_divi.category != DEF_NONE) &
                (tab_inout_divi.category == dividend_category),
                type_='LEFT OUTER',

            ).join(
                tab_mv_counterpart,
                # [MV] transfer booking, select counterpart [1]
                # - a split-booking
                condition=tab_line.bookingtype.in_(['mvin', 'mvout']) &
                ((tab_line.reference == tab_mv_counterpart.id) |
                    (tab_line.id == tab_mv_counterpart.reference)) &
                (tab_mv_counterpart.bookingtype.in_(['spin', 'spout'])),
                type_='LEFT OUTER',
            ).join(
                tab_mv_spline_fee,
                # [MV] fee-line is linked to split-booking-line
                # of counterpart [1]
                condition=(tab_mv_spline_fee.line == tab_mv_counterpart.id) &
                (tab_mv_spline_fee.splittype == 'cat') &
                (tab_mv_spline_fee.category != DEF_NONE) &
                (tab_mv_spline_fee.category == fee_category),
                type_='LEFT OUTER',
            ).join(
                tab_mv_spline_divi,
                # [MV] dividend-line is linked to split-booking-line
                # of counterpart [1]
                condition=(tab_mv_spline_divi.line == tab_mv_counterpart.id) &
                (tab_mv_spline_divi.splittype == 'cat') &
                (tab_mv_spline_divi.category != DEF_NONE) &
                (tab_mv_spline_divi.category == dividend_category),
                type_='LEFT OUTER',

            ).join(
                tab_spline_fee,
                # [SP] fee, split booking
                condition=(tab_spline_fee.line == tab_line.id) &
                tab_line.bookingtype.in_(['spin', 'spout']) &
                (tab_spline_fee.splittype == 'cat') &
                (tab_spline_fee.category != DEF_NONE) &
                (tab_spline_fee.category == fee_category),
                type_='LEFT OUTER',
            ).join(
                tab_spline_divi,
                # [SP] dividend, split booking
                condition=(tab_spline_divi.line == tab_line.id) &
                tab_line.bookingtype.in_(['spin', 'spout']) &
                (tab_spline_divi.splittype == 'cat') &
                (tab_spline_divi.category != DEF_NONE) &
                (tab_spline_divi.category == dividend_category),
                type_='LEFT OUTER',
            ).select(
                tab_line.id,
                Sum(Coalesce(
                    # out-booking, positive amount = fee positive
                    tab_inout_fee.debit - tab_inout_fee.credit,
                    # a category-out on splitbooking as counterpart of
                    # transfer = fee is positive
                    tab_mv_spline_fee.amount,
                    Case(
                        (tab_line.bookingtype == 'spin',
                            tab_spline_fee.amount * Decimal('-1.0')),
                        (tab_line.bookingtype == 'spout',
                            tab_spline_fee.amount),
                    ),
                    Decimal('0.0'),
                    )).as_('fee'),
                Sum(Coalesce(
                    tab_inout_divi.credit - tab_inout_divi.debit,
                    tab_mv_spline_divi.amount,
                    Case(
                        (tab_line.bookingtype == 'spin',
                            tab_spline_divi.amount),
                        (tab_line.bookingtype == 'spout',
                            tab_spline_divi.amount * Decimal('-1.0')),
                    ),
                    Decimal('0.0'),
                    )).as_('dividend'),
                tab_line.cashbook,
                group_by=[tab_line.id, tab_line.cashbook])
        return (tab_line, query)

    @classmethod
    def search_trade_fee(cls, name, clause):
        """ search for fees
        """
        Operator = fields.SQL_OPERATORS[clause[1]]
        (tab_line, tab_query) = cls.get_yield_data_sql()

        query = tab_query.select(
                tab_query.id,
                where=Operator(tab_query.fee, clause[2]))
        return [('id', 'in', query)]

    @classmethod
    def search_asset_dividend(cls, name, clause):
        """ search for dividends
        """
        Operator = fields.SQL_OPERATORS[clause[1]]
        (tab_line, tab_query) = cls.get_yield_data_sql()

        query = tab_query.select(
                tab_query.id,
                where=Operator(tab_query.dividend, clause[2]))
        return [('id', 'in', query)]

    @classmethod
    def search_asset_gainloss(cls, name, clause):
        """ search for profit/loss
        """
        Operator = fields.SQL_OPERATORS[clause[1]]
        (tab_line, tab_query) = cls.get_gainloss_data_sql()

        query = tab_query.select(
                tab_query.id,
                where=Operator(tab_query.gainloss, clause[2]))
        return [('id', 'in', query)]

    @classmethod
    def get_yield_data(cls, lines, names):
        """ collect data for fee, dividend, gain/loss per line
        """
        Line2 = Pool().get('cashbook.line')
        cursor = Transaction().connection.cursor()

        def quantize_val(value, line):
            """ quantize...
            """
            return (
                    value or Decimal('0.0')
                ).quantize(Decimal(str(1/10**line.currency_digits)))

        result = {x: {y.id: None for y in lines} for x in names}

        # read fee, dividend
        name_set = set({'trade_fee', 'asset_dividend'}).intersection(set(names))
        if len(name_set) > 0:
            (tab_line, query) = cls.get_yield_data_sql()
            query.where = tab_line.id.in_([x.id for x in lines])
            cursor.execute(*query)
            records = cursor.fetchall()

            for record in records:
                line = Line2(record[0])
                values = {
                    'trade_fee': quantize_val(record[1], line),
                    'asset_dividend': quantize_val(record[2], line)}
                for name in list(name_set):
                    result[name][record[0]] = values[name]

        # read asset_gainloss
        if 'asset_gainloss' in names:
            (tab_line, query) = cls.get_gainloss_data_sql()
            query.where = tab_line.id.in_([x.id for x in lines])
            cursor.execute(*query)
            records = cursor.fetchall()

            for record in records:
                line = Line2(record[0])
                result['asset_gainloss'][record[0]] = quantize_val(
                    record[1], line)
        return result

    def get_rec_name(self, name):
        """ add quantities - if its a asset-cashbook
        """
        recname = super(Line, self).get_rec_name(name)
        if self.cashbook.feature == 'asset':
            credit = self.quantity_credit \
                if self.quantity_credit is not None else Decimal('0.0')
            debit = self.quantity_debit \
                if self.quantity_debit is not None else Decimal('0.0')
            recname += '|%(quantity)s %(uom_symbol)s' % {
                'quantity': Report.format_number(
                    credit - debit,
                    lang=None, digits=self.quantity_digits),
                'uom_symbol': getattr(self.quantity_uom, 'symbol', '-')}
        return recname

    @classmethod
    def get_fields_write_update(cls):
        """ add 'quantity' to updatefields
        """
        result = super(Line, cls).get_fields_write_update()
        result.append('quantity')
        return result

    @classmethod
    def get_debit_credit(cls, values, line=None):
        """ compute quantity_debit/quantity_credit from quantity
        """
        pool = Pool()
        Cashbook = pool.get('cashbook.book')
        Line2 = pool.get('cashbook.line')

        result = super(Line, cls).get_debit_credit(values, line)
        if line:
            cashbook = line.cashbook
        else:
            id_cashbook = values.get('cashbook', None)
            if id_cashbook is None:
                id_cashbook = Line2.default_cashbook()
            cashbook = None
            if id_cashbook:
                cashbook = Cashbook.browse([id_cashbook])[0]

        if isinstance(values, dict):
            type_ = values.get(
                'bookingtype', getattr(line, 'bookingtype', None))
            quantity = values.get('quantity', None)
        else:
            type_ = getattr(
                values, 'bookingtype', getattr(line, 'bookingtype', None))
            quantity = getattr(values, 'quantity', None)

        if (type_ is not None) and (cashbook.feature == 'asset'):
            if quantity is not None:
                if type_ in ['in', 'mvin', 'spin']:
                    result.update({
                        'quantity_debit': Decimal('0.0'),
                        'quantity_credit': quantity,
                        })
                elif type_ in ['out', 'mvout', 'spout']:
                    result.update({
                        'quantity_debit': quantity,
                        'quantity_credit': Decimal('0.0'),
                        })
                else:
                    raise ValueError('invalid "bookingtype"')

        return result

    @classmethod
    def get_counterpart_values(cls, line, splitline=None, values={}):
        """ add quantity to counterpart
        """
        result = super(Line, cls).get_counterpart_values(
                line,
                splitline=splitline,
                values=values)

        line_uom = getattr(line.quantity_uom, 'id', None)
        booktransf_uom = getattr(getattr(
            line.booktransf, 'quantity_uom', {}), 'id', None)

        if getattr(splitline, 'quantity', None) is not None:
            # we add values to the counterpart of a splitbooking-line
            asset_books = sum([
                    1 if splitline.feature == 'asset' else 0,
                    1 if getattr(
                        splitline.booktransf, 'feature', '-') == 'asset' else 0,
                ])
            diff_uom = False
            if asset_books == 2:
                diff_uom = (
                    splitline.quantity_uom !=
                    splitline.booktransf.quantity_uom) and \
                    (splitline.quantity_uom is not None) and \
                    (splitline.booktransf.quantity_uom is not None)

            result.update({
                'quantity': splitline.quantity_2nd_uom
                if (asset_books == 2) and (diff_uom is True)
                else splitline.quantity,
                'quantity_2nd_uom': splitline.quantity
                if (asset_books == 2) and (diff_uom is True) else None})
        elif sum([1 if booktransf_uom is not None else 0,
                  1 if line_uom is not None else 0]) == 1:
            # one of the related cashbooks only is asset-type
            result.update({
                'quantity': line.quantity,
                'quantity_2nd_uom': None})
        elif sum([1 if booktransf_uom is not None else 0,
                  1 if line_uom is not None else 0]) == 2:
            if line_uom == booktransf_uom:
                result.update({
                    'quantity': line.quantity,
                    'quantity_2nd_uom': None})
            else:
                result.update({
                    'quantity': line.quantity_2nd_uom,
                    'quantity_2nd_uom': line.quantity})
        return result

    @fields.depends('amount', 'splitlines', 'quantity')
    def on_change_splitlines(self):
        """ update amount if splitlines change
        """
        super(Line, self).on_change_splitlines()
        quantity = sum([
            x.quantity for x in self.splitlines
            if x.quantity is not None])
        cnt1 = sum([1 for x in self.splitlines if x.quantity is not None])
        if cnt1 > 0:
            self.quantity = quantity

    @fields.depends(
        'quantity', 'cashbook', '_parent_cashbook.current_rate',
        'currency_digits')
    def on_change_with_current_value(self, name=None):
        """ get current value of line by current stock marked price
            and quantity
        """
        if self.cashbook:
            if (self.quantity is not None) and \
                    (self.cashbook.current_rate is not None):
                return (
                        self.quantity * self.cashbook.current_rate
                    ).quantize(Decimal(str(1/10**self.currency_digits)))

    @fields.depends(
        'quantity', 'amount', 'cashbook', '_parent_cashbook.current_rate',
        'currency_digits')
    def on_change_with_diff_amount(self, name=None):
        """ get delta between buy and current value
        """
        if self.cashbook:
            if (self.quantity is not None) and \
                    (self.amount is not None) and \
                    (self.cashbook.current_rate is not None):
                return (
                    self.quantity * self.cashbook.current_rate -
                    self.amount).quantize(
                        Decimal(str(1/10**self.currency_digits)))

    @fields.depends(
        'quantity', 'amount', 'cashbook', '_parent_cashbook.current_rate')
    def on_change_with_diff_percent(self, name=None):
        """ get performane percent
        """
        if self.cashbook:
            if (self.quantity is not None) and \
                    (self.amount is not None) and \
                    (self.amount != Decimal('0.0')) and \
                    (self.cashbook.current_rate is not None):
                return (
                    self.quantity * self.cashbook.current_rate *
                    Decimal('100.0') / self.amount - Decimal('100.0')
                    ).quantize(Decimal(str(1/10**self.currency_digits)))

    @fields.depends('splitlines')
    def on_change_with_splitline_has_quantity(self, name=None):
        """ get True if splitlines are linked to asset-cashbooks
        """
        result = False
        for line in self.splitlines:
            if line.splittype != 'tr':
                continue
            if line.booktransf:
                if line.booktransf.feature == 'asset':
                    result = True
                    break
        return result

    @fields.depends(
        'id', 'date', 'cashbook', 'feature',
        '_parent_cashbook.id', 'reconciliation',
        '_parent_reconciliation.start_quantity',
        '_parent_reconciliation.state')
    def on_change_with_quantity_balance(self, name=None):
        """ get quantity-balance
        """
        Line2 = Pool().get('cashbook.line')

        if self.feature == 'asset':
            return Line2.get_balance_of_line(
                self, field_name='quantity',
                credit_name='quantity_credit',
                debit_name='quantity_debit')

    @fields.depends('quantity', 'amount', 'currency_digits', 'quantity_digits')
    def on_change_with_asset_rate(self, name=None):
        """ get rate
        """
        if (self.quantity is None) or (self.amount is None):
            return
        digit = max(
            self.currency_digits if self.currency_digits is not None else 2,
            self.quantity_digits if self.quantity_digits is not None else 4)
        if self.quantity != Decimal('0.0'):
            return (
                    self.amount / self.quantity
                ).quantize(Decimal(Decimal(1) / 10**digit))

    @fields.depends(
        'feature', 'cashbook', '_parent_cashbook.quantity_uom',
        'booktransf', '_parent_booktransf.quantity_uom',
        '_parent_booktransf.feature')
    def on_change_with_quantity_uom(self, name=None):
        """ get quantity-unit of asset
        """
        if self.feature == 'asset':
            if self.cashbook:
                if self.cashbook.quantity_uom:
                    return self.cashbook.quantity_uom.id
        else:
            if self.booktransf:
                if self.booktransf.feature == 'asset':
                    if self.booktransf.quantity_uom:
                        return self.booktransf.quantity_uom.id

    @fields.depends(
        'feature', 'cashbook', '_parent_cashbook.quantity_digits',
        'booktransf', '_parent_booktransf.quantity_digits',
        '_parent_booktransf.feature', 'bookingtype', 'splitlines')
    def on_change_with_quantity_digits(self, name=None):
        """ get digits from cashbook or related bookings
        """
        digits = 0
        if self.feature == 'asset':
            if self.cashbook:
                digits = self.cashbook.quantity_digits \
                    if self.cashbook.quantity_digits > digits else digits
        else:
            if self.bookingtype in ['mvin', 'mvout']:
                if self.booktransf:
                    if self.booktransf.feature == 'asset':
                        digits = self.booktransf.quantity_digits \
                            if self.booktransf.quantity_digits > digits \
                            else digits
            elif self.bookingtype in ['spin', 'spout']:
                for spline in (self.splitlines or []):
                    if spline.booktransf:
                        if spline.booktransf.feature == 'asset':
                            digits = spline.booktransf.quantity_digits \
                                if spline.booktransf.quantity_digits > digits \
                                else digits
        return digits

    @classmethod
    def validate(cls, lines):
        """ deny pos/neg mismatch
        """
        super(Line, cls).validate(lines)

        for line in lines:
            # ignore non-asset-lines
            if line.cashbook.feature != 'asset':
                continue

            # quantity must be set
            if (line.quantity is None) or \
                (line.quantity_credit is None) or \
                    (line.quantity_debit is None):
                raise UserError(gettext(
                    'cashbook_investment.msg_line_quantity_not_set',
                    linetxt=line.rec_name))

            # quantity and amount must with same sign
            if (line.amount != Decimal('0.0')) and \
                    (line.quantity != Decimal('0.0')):
                (amount_sign, a_dig, a_exp) = line.amount.as_tuple()
                (quantity_sign, q_dig, q_exp) = line.quantity.as_tuple()
                if amount_sign != quantity_sign:
                    raise UserError(gettext(
                        'cashbook_investment.msg_line_sign_mismatch',
                        linetxt=line.rec_name))

    @classmethod
    def update_values_by_splitlines(cls, lines):
        """ add quantity to line
        """
        to_write = super(Line, cls).update_values_by_splitlines(lines)

        for line in lines:
            cnt1 = sum([1 for x in line.splitlines if x.quantity is not None])
            quantity = sum([
                x.quantity or Decimal('0.0') for x in line.splitlines])
            if (cnt1 > 0) and (quantity != line.quantity):
                to_write.extend([[line], {'quantity': quantity}])
        return to_write

    @classmethod
    def add_values_from_splitlines(cls, values):
        """ add values for create to line by settings on splitlines
        """
        values = super(Line, cls).add_values_from_splitlines(values)

        if ('splitlines' in values.keys()) and \
                ('quantity' not in values.keys()):
            for action in values['splitlines']:
                quantity = None
                if action[0] == 'create':
                    cnt1 = sum([
                        1 for x in action[1]
                        if x.get('quantity', None) is not None
                        ])
                    quantity = sum([
                        x.get('quantity', Decimal('0.0')) for x in action[1]
                        ])
                    if cnt1 > 0:
                        values['quantity'] = quantity
        return values

    @classmethod
    def add_2nd_unit_values(cls, values):
        """ extend create-values
        """
        Cashbook = Pool().get('cashbook.book')

        values = super(Line, cls).add_2nd_unit_values(values)
        cashbook = values.get('cashbook', None)

        if cashbook:
            values.update(cls.add_2nd_quantity(
                values,
                Cashbook(cashbook).quantity_uom))
        return values

# end Line
