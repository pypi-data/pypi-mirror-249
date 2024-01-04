# -*- coding: utf-8 -*-
# This file is part of the cashbook-module from m-ds for Tryton.
# The COPYRIGHT file at the top level of this repository contains the
# full copyright notices and license terms.

from trytond.model import fields, SymbolMixin
from trytond.pool import PoolMeta, Pool
from trytond.pyson import Eval, Or, Bool, If
from trytond.modules.cashbook.book import STATES2, DEPENDS2
from trytond.transaction import Transaction
from trytond.report import Report
from trytond.exceptions import UserError
from trytond.i18n import gettext
from decimal import Decimal
from datetime import timedelta
from sql import Literal
from sql.functions import CurrentDate
from sql.aggregate import Sum
from sql.conditionals import Case, Coalesce
from trytond.modules.cashbook.model import (
    sub_ids_hierarchical, AnyInArray)


class Book(SymbolMixin, metaclass=PoolMeta):
    __name__ = 'cashbook.book'

    asset = fields.Many2One(
        string='Asset', select=True,
        model_name='investment.asset', ondelete='RESTRICT',
        states={
            'required': Eval('feature', '') == 'asset',
            'invisible': Eval('feature', '') != 'asset',
            'readonly': Or(
                    STATES2['readonly'],
                    Eval('has_lines', False))},
        depends=DEPENDS2+['feature', 'has_lines'])
    quantity_digits = fields.Integer(
        string='Digits', help='Quantity Digits',
        domain=[
                ('quantity_digits', '>=', 0),
                ('quantity_digits', '<=', 6)],
        states={
            'required': Eval('feature', '') == 'asset',
            'invisible': Eval('feature', '') != 'asset',
            'readonly': Or(
                    STATES2['readonly'],
                    Eval('has_lines', False))},
        depends=DEPENDS2+['feature', 'has_lines'])
    asset_uomcat = fields.Function(fields.Many2One(
        string='UOM Category', readonly=True,
        model_name='product.uom.category',
        states={'invisible': True}), 'on_change_with_asset_uomcat')
    quantity_uom = fields.Many2One(
        string='UOM', select=True,
        model_name='product.uom', ondelete='RESTRICT',
        domain=[('category.id', '=', Eval('asset_uomcat', -1))],
        states={
            'required': Eval('feature', '') == 'asset',
            'invisible': Eval('feature', '') != 'asset',
            'readonly': Or(
                STATES2['readonly'],
                Eval('has_lines', False))},
        depends=DEPENDS2+['feature', 'asset_uomcat', 'has_lines'])
    symbol = fields.Function(fields.Char(
        string='Symbol', readonly=True), 'on_change_with_symbol')
    asset_symbol = fields.Function(fields.Many2One(
        string='Symbol', readonly=True, model_name='cashbook.book'),
        'on_change_with_asset_symbol')
    quantity = fields.Function(fields.Numeric(
        string='Quantity', help='Quantity of assets until to date',
        readonly=True, digits=(16, Eval('quantity_digits', 4)),
        states={'invisible': Eval('feature', '') != 'asset'},
        depends=['quantity_digits', 'feature']),
        'get_asset_quantity', searcher='search_asset_quantity')
    quantity_all = fields.Function(fields.Numeric(
        string='Total Quantity', help='Total quantity of all assets',
        readonly=True, digits=(16, Eval('quantity_digits', 4)),
        states={'invisible': Eval('feature', '') != 'asset'},
        depends=['quantity_digits', 'feature']),
        'get_asset_quantity', searcher='search_asset_quantity')
    current_value = fields.Function(fields.Numeric(
        string='Value',
        help='Valuation of the investment based on the current ' +
        'stock market price.',
        readonly=True, digits=(16, Eval('currency_digits', 2)),
        states={'invisible': ~Eval('show_performance', False)},
        depends=['currency_digits', 'show_performance']),
        'get_asset_quantity', searcher='search_asset_quantity')
    current_value_ref = fields.Function(fields.Numeric(
        string='Value (Ref.)',
        help='Valuation of the investment based on the current stock' +
        ' exchange price, converted into the company currency.',
        readonly=True, digits=(16, Eval('currency_digits', 2)),
        states={
            'invisible': Or(
                ~Eval('show_performance', False),
                ~Bool(Eval('company_currency', -1)))},
        depends=['currency_digits', 'show_performance', 'company_currency']),
        'get_asset_quantity', searcher='search_asset_quantity')

    # performance
    diff_amount = fields.Function(fields.Numeric(
        string='Difference',
        help='Difference between acquisition value and current value',
        readonly=True, digits=(16, Eval('currency_digits', 2)),
        states={'invisible': ~Eval('show_performance', False)},
        depends=['currency_digits', 'show_performance']),
        'get_asset_quantity', searcher='search_asset_quantity')
    diff_percent = fields.Function(fields.Numeric(
        string='Percent',
        help='percentage performance since acquisition',
        readonly=True, digits=(16, Eval('currency_digits', 2)),
        states={'invisible': ~Eval('show_performance', False)},
        depends=['currency_digits', 'show_performance']),
        'get_asset_quantity', searcher='search_asset_quantity')
    show_performance = fields.Function(fields.Boolean(
        string='Performance', readonly=True), 'on_change_with_show_performance')
    current_rate = fields.Function(fields.Numeric(
        string='Rate',
        help='Rate per unit of investment based on current stock ' +
        'exchange price.',
        readonly=True, digits=(16, Eval('currency_digits', 2)),
        states={'invisible': Eval('feature', '') != 'asset'},
        depends=['currency_digits', 'feature']),
        'get_asset_quantity', searcher='search_asset_quantity')
    purchase_amount = fields.Function(fields.Numeric(
        string='Purchase Amount',
        help='Total purchase amount, from shares and fees.',
        readonly=True, digits=(16, Eval('currency_digits', 2)),
        states={'invisible': Eval('feature', '') != 'asset'},
        depends=['currency_digits', 'feature']),
        'get_asset_quantity', searcher='search_asset_quantity')

    # yield
    yield_dividend_total = fields.Function(fields.Numeric(
        string='Dividend', help='Total dividends received',
        readonly=True, digits=(16, Eval('currency_digits', 2)),
        states={'invisible': Eval('feature', '') != 'asset'},
        depends=['currency_digits', 'feature']),
        'get_yield_data', searcher='search_asset_quantity')
    yield_dividend_12m = fields.Function(fields.Numeric(
        string='Dividend 1y',
        help='Dividends received in the last twelve months',
        readonly=True, digits=(16, Eval('currency_digits', 2)),
        states={'invisible': Eval('feature', '') != 'asset'},
        depends=['currency_digits', 'feature']),
        'get_yield_data', searcher='search_asset_quantity')
    yield_fee_total = fields.Function(fields.Numeric(
        string='Trade Fee', help='Total trade fees payed',
        readonly=True, digits=(16, Eval('currency_digits', 2)),
        states={'invisible': Eval('feature', '') != 'asset'},
        depends=['currency_digits', 'feature']),
        'get_yield_data', searcher='search_asset_quantity')
    yield_fee_12m = fields.Function(fields.Numeric(
        string='Trade Fee 1y',
        help='Trade fees payed in the last twelve month',
        readonly=True, digits=(16, Eval('currency_digits', 2)),
        states={'invisible': Eval('feature', '') != 'asset'},
        depends=['currency_digits', 'feature']),
        'get_yield_data', searcher='search_asset_quantity')
    yield_sales = fields.Function(fields.Numeric(
        string='Sales', help='Total profit or loss on sale of shares.',
        readonly=True, digits=(16, Eval('currency_digits', 2)),
        states={'invisible': Eval('feature', '') != 'asset'},
        depends=['currency_digits', 'feature']),
        'get_yield_data', searcher='search_asset_quantity')
    yield_sales_12m = fields.Function(fields.Numeric(
        string='Sales 1y',
        help='Total profit or loss on sale of shares in the last twelve month.',
        readonly=True, digits=(16, Eval('currency_digits', 2)),
        states={'invisible': Eval('feature', '') != 'asset'},
        depends=['currency_digits', 'feature']),
        'get_yield_data', searcher='search_asset_quantity')
    yield_balance = fields.Function(fields.Numeric(
        string='Total Yield',
        help='Total income: price gain + dividends + sales gains - fees',
        readonly=True, digits=(16, Eval('currency_digits', 2)),
        states={'invisible': Eval('feature', '') != 'asset'},
        depends=['currency_digits', 'feature']),
        'get_yield_balance_data', searcher='search_asset_quantity')

    @classmethod
    def view_attributes(cls):
        return super(Book, cls).view_attributes() + [
            ('/tree', 'visual',
                If(Eval('show_performance', False),
                    If(Eval('diff_percent', 0) < 0, 'danger',
                        If(Eval('diff_percent', 0) > 0,
                            'success', '')), '')),
            ]

    def get_rec_name(self, name):
        """ add quantities - if its a asset-cashbook
        """
        recname = super(Book, self).get_rec_name(name)
        if self.feature == 'asset':
            recname += ' | %(quantity)s %(uom_symbol)s' % {
                'quantity': Report.format_number(
                    self.quantity or 0.0, None,
                    digits=self.quantity_digits),
                'uom_symbol': getattr(self.quantity_uom, 'symbol', '-'),
                }
        return recname

    @classmethod
    def work_order_assets(cls, tables, field_name):
        """ get order-query
        """
        Book2 = Pool().get('cashbook.book')

        if 'date' in Transaction().context:
            raise UserError(gettext(
                'cashbook.msg_nosearch_with_date',
                fname=field_name, model=Book2.__name__))
        return Book2.work_order_balance(tables, field_name)

    @staticmethod
    def order_current_value(tables):
        """ order by current_value
        """
        Book2 = Pool().get('cashbook.book')
        return Book2.work_order_assets(tables, 'current_value')

    @staticmethod
    def order_purchase_amount(tables):
        """ order by purchase_amount
        """
        Book2 = Pool().get('cashbook.book')
        return Book2.work_order_assets(tables, 'purchase_amount')

    @staticmethod
    def order_diff_amount(tables):
        """ order by diff_amount
        """
        Book2 = Pool().get('cashbook.book')
        return Book2.work_order_assets(tables, 'diff_amount')

    @staticmethod
    def order_yield_balance(tables):
        """ order by yield_balance
        """
        Book2 = Pool().get('cashbook.book')
        return Book2.work_order_assets(tables, 'yield_balance')

    @staticmethod
    def order_diff_percent(tables):
        """ order by diff_percent
        """
        Book2 = Pool().get('cashbook.book')
        return Book2.work_order_assets(tables, 'diff_percent')

    @staticmethod
    def order_quantity(tables):
        """ order by quantity
        """
        Book2 = Pool().get('cashbook.book')
        return Book2.work_order_assets(tables, 'quantity')

    @staticmethod
    def order_quantity_all(tables):
        """ order by quantity_all
        """
        Book2 = Pool().get('cashbook.book')
        return Book2.work_order_assets(tables, 'quantity_all')

    @staticmethod
    def order_yield_sales(tables):
        """ order by yield_sales
        """
        Book2 = Pool().get('cashbook.book')
        return Book2.work_order_assets(tables, 'yield_sales')

    @staticmethod
    def order_yield_sales_12m(tables):
        """ order by yield_sales_12m
        """
        Book2 = Pool().get('cashbook.book')
        return Book2.work_order_assets(tables, 'yield_sales_12m')

    @staticmethod
    def order_yield_dividend_total(tables):
        """ order by yield_dividend_total
        """
        Book2 = Pool().get('cashbook.book')
        return Book2.work_order_assets(tables, 'yield_dividend_total')

    @staticmethod
    def order_yield_dividend_12m(tables):
        """ order by yield_dividend_12m
        """
        Book2 = Pool().get('cashbook.book')
        return Book2.work_order_assets(tables, 'yield_dividend_12m')

    @staticmethod
    def order_yield_fee_total(tables):
        """ order by yield_fee_total
        """
        Book2 = Pool().get('cashbook.book')
        return Book2.work_order_assets(tables, 'yield_fee_total')

    @staticmethod
    def order_yield_fee_12m(tables):
        """ order by yield_fee_12m
        """
        Book2 = Pool().get('cashbook.book')
        return Book2.work_order_assets(tables, 'yield_fee_12m')

    @fields.depends('asset', 'quantity_uom')
    def on_change_asset(self):
        """ get uom from asset
        """
        if self.asset:
            self.quantity_uom = self.asset.uom.id

    @classmethod
    def default_quantity_digits(cls):
        """ default: 4
        """
        return 4

    @classmethod
    def get_yield_balance_data(cls, cashbooks, names):
        """ calculate yield total
            fee is already contained in 'diff_amount'
        """
        context = Transaction().context

        result = {x: {y.id: Decimal('0.0') for y in cashbooks} for x in names}

        query_date = context.get('date', None)
        if context.get(
                'compute_yield_balance',
                False) or query_date is not None:
            amounts = {}
            amounts.update(cls.get_asset_quantity(cashbooks, ['diff_amount']))
            amounts.update(cls.get_yield_data(
                cashbooks,
                ['yield_dividend_total', 'yield_sales']))

            for cashbook in cashbooks:
                sum_lst = [
                    amounts[x][cashbook.id]
                    for x in [
                        'diff_amount', 'yield_dividend_total',
                        'yield_sales']]
                sum2 = sum([x for x in sum_lst if x is not None])
                result['yield_balance'][cashbook.id] = sum2
        else:
            for cashbook in cashbooks:
                for value in cashbook.value_store:
                    if value.field_name in names:
                        result[value.field_name][cashbook.id] = value.numvalue
        return result

    @classmethod
    def get_yield_data_sql(cls, date_from=None, date_to=None):
        """ collect yield data
        """
        pool = Pool()
        Line = pool.get('cashbook.line')
        Currency = pool.get('currency.currency')
        (tab_line1, tab_line_yield) = Line.get_yield_data_sql()
        (tab_line2, tab_line_gainloss) = Line.get_gainloss_data_sql()
        tab_book = cls.__table__()
        tab_line = Line.__table__()
        tab_cur = Currency.__table__()

        where = Literal(True)
        if date_from:
            where &= tab_line.date >= date_from
        if date_to:
            where &= tab_line.date <= date_to

        query = tab_book.join(
                tab_line,
                condition=tab_line.cashbook == tab_book.id,
            ).join(
                tab_cur,
                condition=tab_cur.id == tab_book.currency,
            ).join(
                tab_line_yield,
                condition=tab_line_yield.id == tab_line.id,
            ).join(
                tab_line_gainloss,
                condition=tab_line_gainloss.id == tab_line.id,
            ).select(
                tab_book.id,
                Sum(tab_line_yield.fee).as_('fee'),
                Sum(tab_line_yield.dividend).as_('dividend'),
                Sum(tab_line_gainloss.gainloss).as_('gainloss'),
                tab_cur.digits.as_('currency_digits'),
                group_by=[tab_book.id, tab_cur.digits],
                where=where)
        return (tab_book, query)

    @classmethod
    def get_yield_data(cls, cashbooks, names):
        """ get yield data - stored or computed
        """
        context = Transaction().context

        result = {x: {y.id: Decimal('0.0') for y in cashbooks} for x in names}

        # return computed values if 'date' is in context
        query_date = context.get('date', None)
        if query_date is not None:
            return cls.get_yield_values(cashbooks, names)

        for cashbook in cashbooks:
            for value in cashbook.value_store:
                if value.field_name in names:
                    result[value.field_name][cashbook.id] = value.numvalue
        return result

    @classmethod
    def get_yield_values(cls, cashbooks, names):
        """ collect yield data
        """
        pool = Pool()
        IrDate = pool.get('ir.date')
        cursor = Transaction().connection.cursor()
        context = Transaction().context
        result = {
            x: {y.id: Decimal('0.0') for y in cashbooks}
            for x in [
                'yield_fee_total', 'yield_dividend_total',
                'yield_sales', 'yield_fee_12m', 'yield_dividend_12m',
                'yield_sales_12m']}

        def quantize_val(value, digits):
            """ quantize...
            """
            return (
                    value or Decimal('0.0')
                ).quantize(Decimal(str(1/10 ** digits)))

        query_date = context.get('date', IrDate.today())

        # results for 'total'
        records_total = []
        records_12m = []
        if cashbooks:
            (tab_book1, query_total) = cls.get_yield_data_sql()
            query_total.where &= tab_book1.id.in_([x.id for x in cashbooks])
            cursor.execute(*query_total)
            records_total = cursor.fetchall()

            # results for 12 months
            (tab_book2, query_12m) = cls.get_yield_data_sql(
                    date_to=query_date,
                    date_from=query_date - timedelta(days=365),
                )
            query_12m.where &= tab_book2.id.in_([x.id for x in cashbooks])
            cursor.execute(*query_12m)
            records_12m = cursor.fetchall()

        for record in records_total:
            result['yield_fee_total'][record[0]] = quantize_val(
                record[1], record[4])
            result['yield_dividend_total'][record[0]] = quantize_val(
                record[2], record[4])
            result['yield_sales'][record[0]] = quantize_val(
                record[3], record[4])

        for record in records_12m:
            result['yield_fee_12m'][record[0]] = quantize_val(
                record[1], record[4])
            result['yield_dividend_12m'][record[0]] = quantize_val(
                record[2], record[4])
            result['yield_sales_12m'][record[0]] = quantize_val(
                record[3], record[4])
        return {x: result[x] for x in names}

    @classmethod
    def get_asset_quantity_sql(cls):
        """ get table of asset and its value, rate, ...
        """
        pool = Pool()
        CBook = pool.get('cashbook.book')
        BookType = pool.get('cashbook.type')
        Line = pool.get('cashbook.line')
        Asset = pool.get('investment.asset')
        Currency = pool.get('currency.currency')
        tab_book = CBook.__table__()
        tab_type = BookType.__table__()
        tab_line = Line.__table__()
        tab_cur = Currency.__table__()
        tab_asset = Asset.__table__()
        (tab_rate, tab2) = Asset.get_rate_data_sql()
        (tab_balance, tab2) = CBook.get_balance_of_cashbook_sql()
        (tab_line_yield, query_yield) = Line.get_yield_data_sql()
        context = Transaction().context

        query_date = context.get('date', CurrentDate())
        query = tab_book.join(
                tab_line,
                condition=(tab_book.id == tab_line.cashbook),
            ).join(
                tab_type,
                condition=tab_book.btype == tab_type.id,
            ).join(
                tab_cur,
                condition=tab_book.currency == tab_cur.id,
            ).join(
                tab_asset,
                condition=tab_book.asset == tab_asset.id,
            ).join(
                query_yield,
                condition=query_yield.id == tab_line.id,
            ).join(
                tab_balance,
                condition=tab_book.id == tab_balance.cashbook,
                type_='LEFT OUTER',
            ).join(
                tab_rate,
                condition=tab_book.asset == tab_rate.id,
                type_='LEFT OUTER',
            ).select(
                tab_book.id,    # 0
                Coalesce(Sum(Case(
                    (tab_line.date <= query_date,
                        tab_line.quantity_credit - tab_line.quantity_debit),
                    else_=Decimal('0.0'),
                )), Decimal('0.0')).as_('quantity'),    # 1
                Sum(
                    tab_line.quantity_credit -
                    tab_line.quantity_debit).as_('quantity_all'),   # 2
                Coalesce(tab_rate.rate, Decimal('0.0')).as_('rate'),    # 3
                tab_book.currency,  # 4
                tab_cur.digits.as_('currency_digits'),     # 5
                tab_asset.uom,          # 6
                tab_book.quantity_uom,  # 7
                tab_asset.currency.as_('asset_currency'),   # 8
                (
                    Sum(query_yield.fee) + tab_balance.balance
                ).as_('purchase_amount'),   # 9
                group_by=[
                    tab_book.id, tab_rate.rate,
                    tab_book.currency, tab_cur.digits, tab_asset.uom,
                    tab_book.quantity_uom, tab_asset.currency,
                    tab_balance.balance],
                where=(tab_type.feature == 'asset'))
        return (query, tab_book)

    @classmethod
    def get_asset_quantity_values(cls, cashbooks, names):
        """ get quantities
            field: quantity, quantity_all, current_value,
                current_value_ref, diff_amount, diff_percent,
                current_rate, purchase_amount
        """
        pool = Pool()
        CBook = pool.get('cashbook.book')
        Uom = pool.get('product.uom')
        Currency = pool.get('currency.currency')
        cursor = Transaction().connection.cursor()
        (query, tab_book) = cls.get_asset_quantity_sql()

        company_currency = CBook.default_currency()
        result = {
            x: {y.id: None for y in cashbooks}
            for x in [
                'quantity', 'quantity_all', 'current_value',
                'current_value_ref', 'diff_amount', 'diff_percent',
                'current_rate', 'purchase_amount', 'purchase_amount_ref',
                'digits']
            }

        def values_from_record(rdata):
            """ compute values for record
            """
            # uom-factor
            if rdata[6] == rdata[7]:
                uom_factor = Decimal('1.0')
            else:
                uom_factor = Decimal(
                    Uom.compute_qty(
                        Uom(rdata[6]), 1.0,
                        Uom(rdata[7]), round=False))

            current_value = Currency.compute(
                    rdata[8],
                    rdata[3] * rdata[1] / uom_factor,
                    rdata[4])
            return (record[0], {
                'quantity': rdata[1],
                'quantity_all': rdata[2],
                'current_value': current_value,
                'current_value_ref': Currency.compute(
                        rdata[8],
                        rdata[3] * rdata[1] / uom_factor,
                        company_currency
                        if company_currency is not None else rdata[8]),
                'diff_amount': current_value - rdata[9],
                'diff_percent': (
                        Decimal('100.0') * current_value /
                        rdata[9] - Decimal('100.0')
                    ).quantize(Decimal(str(1/10**rdata[5])))
                if rdata[9] != Decimal('0.0') else None,
                'current_rate': (
                        current_value / rdata[1]
                    ).quantize(Decimal(str(1/10**rdata[5])))
                if rdata[1] != Decimal('0.0') else None,
                'purchase_amount': record[9].quantize(
                    Decimal(str(1/10**rdata[5]))),
                'purchase_amount_ref': Currency.compute(
                        rdata[4],
                        record[9],
                        company_currency
                        if company_currency is not None else rdata[4]),
                })

        ids_assetbooks = []
        ids_nonebtypes = []
        for x in cashbooks:
            if x.btype is None:
                if x.id not in ids_nonebtypes:
                    ids_nonebtypes.append(x.id)
            else:
                if x.id not in ids_assetbooks:
                    ids_assetbooks.append(x.id)

        # get values of asset-cashbooks in 'cashbooks' of type=asset
        if len(ids_assetbooks) > 0:
            query.where &= tab_book.id.in_(ids_assetbooks)
            cursor.execute(*query)
            records = cursor.fetchall()

            for record in records:
                (book_id, values) = values_from_record(record)

                for name in values.keys():
                    result[name][book_id] = values[name]

        # add aggregated values of cashbooks without type
        aggr_names = [
            'current_value', 'current_value_ref',
            'diff_amount', 'diff_percent']
        queried_names = list(set(aggr_names).intersection(set(names)))

        if (len(queried_names) > 0) and (len(ids_nonebtypes) > 0):
            # query all subordered asset-cashbooks to get values for
            # cashbooks without type

            (tab_quantity, tab_book) = cls.get_asset_quantity_sql()
            tab_subids = sub_ids_hierarchical('cashbook.book')
            query = tab_book.join(
                    tab_subids,
                    condition=tab_book.id == tab_subids.parent,
                ).join(
                    tab_quantity,
                    condition=tab_quantity.id == AnyInArray(tab_subids.subids),
                ).select(
                    tab_book.id,
                    Sum(tab_quantity.quantity),                 # 1
                    Sum(tab_quantity.quantity_all),             # 2
                    tab_quantity.rate,                          # 3
                    tab_quantity.currency,                      # 4
                    tab_quantity.currency_digits,               # 5
                    tab_quantity.uom,                           # 6
                    tab_quantity.quantity_uom,                  # 7
                    tab_quantity.asset_currency,                # 8
                    Sum(tab_quantity.purchase_amount),          # 9
                    tab_book.currency.as_('currency_book'),     # 10
                    where=tab_book.id.in_(ids_nonebtypes),
                    group_by=[
                        tab_book.id, tab_quantity.rate,
                        tab_quantity.currency, tab_quantity.currency_digits,
                        tab_quantity.uom, tab_quantity.quantity_uom,
                        tab_quantity.asset_currency, tab_book.currency])
            cursor.execute(*query)
            records = cursor.fetchall()

            for record in records:
                (book_id, values) = values_from_record(record)

                for name in [
                        'current_value', 'diff_amount',
                        'current_value_ref', 'purchase_amount_ref']:
                    if result[name][book_id] is None:
                        result[name][book_id] = Decimal('0.0')

                    value = Decimal('0.0')
                    if name == 'current_value':
                        value = Currency.compute(
                            company_currency
                            if company_currency is not None else record[4],
                            values['current_value_ref'],
                            record[10])
                    elif name == 'diff_amount':
                        value = Currency.compute(
                            company_currency
                            if company_currency is not None else record[4],
                            values['current_value_ref'] -
                            values['purchase_amount_ref'],
                            record[10])
                    elif name in ['current_value_ref', 'purchase_amount_ref']:
                        value = values[name]
                        result['digits'][book_id] = record[5]
                    result[name][book_id] += value

            # diff_percent
            for id_book in ids_nonebtypes:
                c_val = result['current_value_ref'][id_book]
                p_amount = result['purchase_amount_ref'][id_book]
                digits = result['digits'][id_book]

                if (p_amount == Decimal('0.0')) or \
                        (p_amount is None) or (c_val is None):
                    continue

                result['diff_percent'][id_book] = (
                        Decimal('100.0') * c_val / p_amount - Decimal('100.0')
                    ).quantize(Decimal(str(1/10 ** digits)))
                result['digits'][id_book] = None
        return {x: result[x] for x in names}

    @classmethod
    def get_asset_quantity(cls, cashbooks, names):
        """ get quantities - stored or computed
        """
        context = Transaction().context

        result = {x: {y.id: Decimal('0.0') for y in cashbooks} for x in names}

        # return computed values if 'date' is in context
        query_date = context.get('date', None)
        if query_date is not None:
            return cls.get_asset_quantity_values(cashbooks, names)

        for cashbook in cashbooks:
            for value in cashbook.value_store:
                if value.field_name in names:
                    result[value.field_name][cashbook.id] = value.numvalue
        return result

    @classmethod
    def search_asset_quantity(cls, name, clause):
        """ search in stored data
        """
        ValueStore = Pool().get('cashbook.values')
        context = Transaction().context

        query_date = context.get('date', None)
        if query_date is not None:
            raise UserError(gettext(
                'cashbook.msg_nosearch_with_date',
                fname=name, model=cls.__name__))
        else:
            value_query = ValueStore.search([
                ('field_name', '=', clause[0]),
                ('numvalue',) + tuple(clause[1:]),
                ],
                query=True)
            return [('value_store', 'in', value_query)]

    @classmethod
    def valuestore_fields(cls):
        """ field to update
        """
        result = super(Book, cls).valuestore_fields()

        # get_asset_quantity_values
        result.extend([
            'quantity', 'quantity_all', 'current_value', 'current_value_ref',
            'diff_amount', 'diff_percent', 'current_rate', 'purchase_amount',
            'yield_fee_total', 'yield_dividend_total', 'yield_sales',
            'yield_fee_12m', 'yield_dividend_12m', 'yield_sales_12m',
            'yield_balance'])
        return result

    @classmethod
    def valuestore_update_records(cls, records):
        """ compute current values of records,
            store to global storage
        """
        ValStore = Pool().get('cashbook.values')

        super(Book, cls).valuestore_update_records(records)

        if records:
            ValStore.update_values(
                cls.get_asset_quantity_values(
                    records, [
                        'quantity', 'quantity_all', 'current_value',
                        'current_value_ref', 'diff_amount', 'diff_percent',
                        'current_rate', 'purchase_amount']))
            ValStore.update_values(
                cls.get_yield_values(
                    records, [
                        'yield_fee_total', 'yield_dividend_total',
                        'yield_sales', 'yield_fee_12m', 'yield_dividend_12m',
                        'yield_sales_12m']))
            with Transaction().set_context({
                    'compute_yield_balance': True}):
                ValStore.update_values(
                    cls.get_yield_balance_data(records, ['yield_balance']))

    @fields.depends('id')
    def on_change_with_show_performance(self, name=None):
        """ return True if current or subordered cashbooks
            are of type=asset
        """
        Book2 = Pool().get('cashbook.book')

        if Book2.search_count([
                ('btype.feature', '=', 'asset'),
                ('parent', 'child_of', [self.id])]) > 0:
            return True
        return False

    @fields.depends('id')
    def on_change_with_asset_symbol(self, name=None):
        """ get current cashbook to enable usage of 'symbol'
            in the form
        """
        return self.id

    @fields.depends('quantity_uom', 'currency')
    def on_change_with_symbol(self, name=None):
        """ get symbol for asset
        """
        return '%(currency)s/%(unit)s' % {
            'currency': getattr(self.currency, 'symbol', '-'),
            'unit': getattr(self.quantity_uom, 'symbol', '-')}

    @fields.depends('asset', '_parent_asset.uom')
    def on_change_with_asset_uomcat(self, name=None):
        """ get uom-category of asset
        """
        if self.asset:
            return self.asset.uom.category.id

# end Book
