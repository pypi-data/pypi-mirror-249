# -*- coding: utf-8 -*-
# This file is part of the cashbook-module from m-ds for Tryton.
# The COPYRIGHT file at the top level of this repository contains the
# full copyright notices and license terms.

from decimal import Decimal
from datetime import date
from trytond.pool import Pool
from trytond.transaction import Transaction
from trytond.tests.test_tryton import with_transaction


class YieldTestCase(object):
    """ test yield
    """
    def prep_yield_config(self, fee, dividend, gainloss, company):
        """ add config for yield-calculation
            fee: name of fee-category,
            dividend: name of fee-category,
            gainloss: name of cashbook for gain/loss booking
        """
        pool = Pool()
        Category = pool.get('cashbook.category')
        Cashbook = pool.get('cashbook.book')
        AssetConf = pool.get('cashbook.assetconf')

        fee_cat = Category.search([('name', '=', fee)])
        if len(fee_cat) > 0:
            fee_cat = fee_cat[0]
        else:
            fee_cat, = Category.create([{
                'name': fee,
                'company': company.id,
                'cattype': 'out',
                }])

        dividend_cat = Category.search([('name', '=', dividend)])
        if len(dividend_cat) > 0:
            dividend_cat = dividend_cat[0]
        else:
            dividend_cat, = Category.create([{
                'name': dividend,
                'company': company.id,
                'cattype': 'in',
                }])

        gainloss_book = Cashbook.search([('name', '=', gainloss)])
        if len(gainloss_book) > 0:
            gainloss_book = gainloss_book[0]
        else:
            types = self.prep_type()
            gainloss_book, = Cashbook.create([{
                'name': gainloss,
                'btype': types.id,
                'company': company.id,
                'currency': company.currency.id,
                'number_sequ': self.prep_sequence().id,
                'start_date': date(2022, 5, 1),
                }])

        as_cfg = None
        with Transaction().set_context({
                'company': company.id}):
            as_cfg, = AssetConf.create([{
                'fee_category': fee_cat.id,
                'dividend_category': dividend_cat.id,
                'gainloss_book': gainloss_book.id,
                }])
            self.assertEqual(as_cfg.fee_category.rec_name, fee)
            self.assertEqual(as_cfg.fee_category.cattype, 'out')

            self.assertEqual(as_cfg.dividend_category.rec_name, dividend)
            self.assertEqual(as_cfg.dividend_category.cattype, 'in')

            self.assertEqual(
                as_cfg.gainloss_book.rec_name,
                '%s | 0.00 usd | Open' % gainloss)
        return as_cfg

    @with_transaction()
    def test_yield_config(self):
        """ check config
        """
        company = self.prep_company()

        with Transaction().set_context({'company': company.id}):
            as_cfg = self.prep_yield_config(
                'Fee', 'Dividend', 'GainLoss', company)
            self.assertEqual(as_cfg.fee_category.rec_name, 'Fee')
            self.assertEqual(as_cfg.dividend_category.rec_name, 'Dividend')
            self.assertEqual(
                as_cfg.gainloss_book.rec_name,
                'GainLoss | 0.00 usd | Open')

    @with_transaction()
    def test_yield_fee_category_in_out(self):
        """ check out-booking, category in/out
        """
        pool = Pool()
        Cashbook = pool.get('cashbook.book')
        BType = pool.get('cashbook.type')
        Line = pool.get('cashbook.line')

        company = self.prep_company()
        with Transaction().set_context({'company': company.id}):
            as_cfg = self.prep_yield_config(
                'Fee', 'Dividend', 'Profit-Loss', company)

            type_depot = self.prep_type('Depot', 'D')
            BType.write(*[
                [type_depot],
                {
                    'feature': 'asset',
                }])

            asset = self.prep_asset_item(
                company=company,
                product=self.prep_asset_product(name='Product 1'))
            self.assertEqual(asset.symbol, 'usd/u')

            book_asset, = Cashbook.create([{
                'name': 'Depot',
                'btype': type_depot.id,
                'company': company.id,
                'currency': company.currency.id,
                'number_sequ': self.prep_sequence().id,
                'asset': asset.id,
                'quantity_uom': asset.uom.id,
                'start_date': date(2022, 5, 1),
                'lines': [('create', [{
                    'bookingtype': 'in',
                    'date': date(2022, 5, 1),
                    'amount': Decimal('23.50'),
                    'quantity': Decimal('3.0'),
                    'category': as_cfg.dividend_category.id,
                    'description': 'Initial (1)',
                    }, ])],
                }])

            self.assertEqual(
                book_asset.rec_name,
                'Depot | 23.50 usd | Open | 3.0000 u')
            lines = Line.create([{
                'cashbook': book_asset.id,
                'date': date(2022, 5, 2),
                'bookingtype': 'out',
                'description': 'trade fee, payed from asset',
                'category': as_cfg.fee_category.id,
                'amount': Decimal('4.0'),
                'quantity': Decimal('0.0'),
                }])

            self.assertEqual(len(lines), 1)
            Line.wfcheck(lines)
            self.prep_valstore_run_worker()

            self.assertEqual(
                lines[0].rec_name,
                '05/02/2022|Exp|-4.00 usd|trade fee, payed from asset' +
                ' [Fee]|0.0000 u')

            self.assertEqual(lines[0].asset_gainloss, Decimal('0.0'))
            self.assertEqual(lines[0].asset_dividend, Decimal('0.0'))
            self.assertEqual(lines[0].trade_fee, Decimal('4.0'))
            self.assertEqual(
                book_asset.rec_name,
                'Depot | 19.50 usd | Open | 3.0000 u')

            self.assertEqual(book_asset.yield_dividend_total, Decimal('23.5'))
            self.assertEqual(book_asset.yield_fee_total, Decimal('4.0'))
            self.assertEqual(book_asset.yield_sales, Decimal('0.0'))
            self.assertEqual(book_asset.diff_amount, Decimal('-23.5'))
            self.assertEqual(book_asset.yield_balance, Decimal('0.0'))

    @with_transaction()
    def test_yield_fee_transfer_from_splitbooking_cash_out(self):
        """ check out-booking, transfer from cash --> asset,
            fee on counterpart of splitbooking
        """
        pool = Pool()
        Cashbook = pool.get('cashbook.book')
        BType = pool.get('cashbook.type')
        Line = pool.get('cashbook.line')

        company = self.prep_company()
        with Transaction().set_context({'company': company.id}):
            as_cfg = self.prep_yield_config(
                'Fee', 'Dividend', 'Profit-Loss', company)

            type_depot = self.prep_type('Depot', 'D')
            type_cash = self.prep_type('Cash', 'C')
            BType.write(*[
                [type_depot],
                {
                    'feature': 'asset',
                }])

            asset = self.prep_asset_item(
                company=company,
                product=self.prep_asset_product(name='Product 1'))
            self.assertEqual(asset.symbol, 'usd/u')

            book_cash, = Cashbook.create([{
                'name': 'Cash',
                'btype': type_cash.id,
                'company': company.id,
                'currency': company.currency.id,
                'number_sequ': self.prep_sequence().id,
                'start_date': date(2022, 5, 1),
                }])

            book_asset, = Cashbook.create([{
                'name': 'Depot',
                'btype': type_depot.id,
                'company': company.id,
                'currency': company.currency.id,
                'number_sequ': self.prep_sequence().id,
                'asset': asset.id,
                'quantity_uom': asset.uom.id,
                'start_date': date(2022, 5, 1),
                'lines': [('create', [{
                    'bookingtype': 'in',
                    'date': date(2022, 5, 1),
                    'amount': Decimal('23.50'),
                    'quantity': Decimal('3.0'),
                    'category': as_cfg.dividend_category.id,
                    'description': 'Initial',
                    }, ])],
                }])

            self.assertEqual(
                book_asset.rec_name,
                'Depot | 23.50 usd | Open | 3.0000 u')
            self.assertEqual(len(book_asset.lines), 1)
            self.assertEqual(book_cash.rec_name, 'Cash | 0.00 usd | Open')
            self.assertEqual(len(book_cash.lines), 0)

            Cashbook.write(*[
                [book_cash],
                {
                    'lines': [('create', [{
                        'bookingtype': 'spout',
                        'date': date(2022, 5, 2),
                        'description': 'buy shares, fee',
                        'splitlines': [('create', [{
                            'splittype': 'tr',
                            'booktransf': book_asset.id,
                            'description': 'buy shares',
                            'quantity': Decimal('1.0'),
                            'amount': Decimal('30.0'),
                            }, {
                            'splittype': 'cat',
                            'category': as_cfg.fee_category.id,
                            'description': 'trade fee',
                            'amount': Decimal('3.0'),
                            }])],
                        }])],
                }])

            Line.wfcheck(book_cash.lines)
            self.prep_valstore_run_worker()

            self.assertEqual(
                book_asset.rec_name,
                'Depot | 53.50 usd | Open | 4.0000 u')
            self.assertEqual(len(book_asset.lines), 2)
            self.assertEqual(book_cash.rec_name, 'Cash | -33.00 usd | Open')
            self.assertEqual(len(book_cash.lines), 1)

            self.assertEqual(
                book_asset.lines[0].rec_name,
                '05/02/2022|from|30.00 usd|buy shares [Cash | ' +
                '-33.00 usd | Open]|1.0000 u')
            self.assertEqual(
                book_asset.lines[1].rec_name,
                '05/01/2022|Rev|23.50 usd|Initial [Dividend]|3.0000 u')
            self.assertEqual(
                book_cash.lines[0].rec_name,
                '05/02/2022|Exp/Sp|-33.00 usd|buy shares, fee [-]')

            self.assertEqual(book_asset.lines[0].asset_gainloss, Decimal('0.0'))
            self.assertEqual(book_asset.lines[0].asset_dividend, Decimal('0.0'))
            self.assertEqual(book_asset.lines[0].trade_fee, Decimal('3.0'))

    @with_transaction()
    def test_yield_fee_transfer_from_splitbooking_asset_out(self):
        """ check out-booking, transfer from asset --> cash,
            fee on counterpart of splitbooking
        """
        pool = Pool()
        Cashbook = pool.get('cashbook.book')
        BType = pool.get('cashbook.type')
        Line = pool.get('cashbook.line')

        company = self.prep_company()
        with Transaction().set_context({'company': company.id}):
            as_cfg = self.prep_yield_config(
                'Fee', 'Dividend', 'Profit-Loss', company)

            type_depot = self.prep_type('Depot', 'D')
            type_cash = self.prep_type('Cash', 'C')
            BType.write(*[
                [type_depot],
                {
                    'feature': 'asset',
                }])

            asset = self.prep_asset_item(
                company=company,
                product=self.prep_asset_product(name='Product 1'))
            self.assertEqual(asset.symbol, 'usd/u')

            book_cash, = Cashbook.create([{
                'name': 'Cash',
                'btype': type_cash.id,
                'company': company.id,
                'currency': company.currency.id,
                'number_sequ': self.prep_sequence().id,
                'start_date': date(2022, 5, 1),
                }])

            book_asset, = Cashbook.create([{
                'name': 'Depot',
                'btype': type_depot.id,
                'company': company.id,
                'currency': company.currency.id,
                'number_sequ': self.prep_sequence().id,
                'asset': asset.id,
                'quantity_uom': asset.uom.id,
                'start_date': date(2022, 5, 1),
                'lines': [('create', [{
                    'bookingtype': 'in',
                    'date': date(2022, 5, 1),
                    'amount': Decimal('23.50'),
                    'quantity': Decimal('3.0'),
                    'category': as_cfg.dividend_category.id,
                    'description': 'Initial',
                    }, ])],
                }])

            self.assertEqual(
                book_asset.rec_name, 'Depot | 23.50 usd | Open | 3.0000 u')
            self.assertEqual(len(book_asset.lines), 1)
            self.assertEqual(book_cash.rec_name, 'Cash | 0.00 usd | Open')
            self.assertEqual(len(book_cash.lines), 0)

            Cashbook.write(*[
                [book_asset],
                {
                    'lines': [('create', [{
                        'bookingtype': 'spout',
                        'date': date(2022, 5, 2),
                        'description': 'sell shares, fee',
                        'splitlines': [('create', [{
                            'splittype': 'tr',
                            'booktransf': book_cash.id,
                            'description': 'sell shares',
                            'quantity': Decimal('1.0'),
                            'amount': Decimal('20.0'),
                            }, {
                            'splittype': 'cat',
                            'category': as_cfg.fee_category.id,
                            'description': 'trade fee',
                            'amount': Decimal('3.0'),
                            'quantity': Decimal('0.0'),
                            }])],
                        }])],
                }])

            Line.wfcheck(book_asset.lines)
            self.prep_valstore_run_worker()

            self.assertEqual(
                book_asset.rec_name,
                'Depot | 0.50 usd | Open | 2.0000 u')
            self.assertEqual(len(book_asset.lines), 2)
            self.assertEqual(book_cash.rec_name, 'Cash | 20.00 usd | Open')
            self.assertEqual(len(book_cash.lines), 1)

            self.assertEqual(
                book_asset.lines[0].rec_name,
                '05/01/2022|Rev|23.50 usd|Initial [Dividend]|3.0000 u')
            self.assertEqual(
                book_asset.lines[1].rec_name,
                '05/02/2022|Exp/Sp|-23.00 usd|sell shares, fee [-]|-1.0000 u')
            self.assertEqual(
                book_cash.lines[0].rec_name,
                '05/02/2022|from|20.00 usd|sell shares [Depot | ' +
                '0.50 usd | Open | 2.0000 u]')

            self.assertEqual(book_asset.lines[1].asset_gainloss, Decimal('0.0'))
            self.assertEqual(book_asset.lines[1].asset_dividend, Decimal('0.0'))
            self.assertEqual(book_asset.lines[1].trade_fee, Decimal('3.0'))

    @with_transaction()
    def test_yield_dividend_category_in(self):
        """ check out-booking, dividend in/out
        """
        pool = Pool()
        Cashbook = pool.get('cashbook.book')
        BType = pool.get('cashbook.type')
        Line = pool.get('cashbook.line')

        company = self.prep_company()
        with Transaction().set_context({'company': company.id}):
            as_cfg = self.prep_yield_config(
                'Fee', 'Dividend', 'Profit-Loss', company)

            type_depot = self.prep_type('Depot', 'D')
            self.prep_type('Cash', 'C')
            category_in = self.prep_category(name='Income', cattype='in')
            BType.write(*[
                [type_depot],
                {
                    'feature': 'asset',
                }])

            asset = self.prep_asset_item(
                company=company,
                product=self.prep_asset_product(name='Product 1'))
            self.assertEqual(asset.symbol, 'usd/u')

            book_asset, = Cashbook.create([{
                'name': 'Depot',
                'btype': type_depot.id,
                'company': company.id,
                'currency': company.currency.id,
                'number_sequ': self.prep_sequence().id,
                'asset': asset.id,
                'quantity_uom': asset.uom.id,
                'start_date': date(2022, 5, 1),
                'lines': [('create', [{
                    'bookingtype': 'in',
                    'date': date(2022, 5, 2),
                    'amount': Decimal('23.50'),
                    'quantity': Decimal('3.0'),
                    'category': category_in.id,
                    'description': 'Initial',
                    }, ])],
                }])

            self.assertEqual(
                book_asset.rec_name,
                'Depot | 23.50 usd | Open | 3.0000 u')
            lines = Line.create([{
                'cashbook': book_asset.id,
                'date': date(2022, 5, 2),
                'bookingtype': 'in',
                'description': 'dividend',
                'category': as_cfg.dividend_category.id,
                'amount': Decimal('4.0'),
                'quantity': Decimal('0.0'),
                }])

            self.assertEqual(len(lines), 1)
            Line.wfcheck(lines)
            self.prep_valstore_run_worker()

            self.assertEqual(
                lines[0].rec_name,
                '05/02/2022|Rev|4.00 usd|dividend [Dividend]|0.0000 u')

            self.assertEqual(lines[0].asset_gainloss, Decimal('0.0'))
            self.assertEqual(lines[0].asset_dividend, Decimal('4.0'))
            self.assertEqual(lines[0].trade_fee, Decimal('0.0'))
            self.assertEqual(
                book_asset.rec_name,
                'Depot | 27.50 usd | Open | 3.0000 u')

    @with_transaction()
    def test_yield_dividend_category_out(self):
        """ check out-booking, dividend in/out
        """
        pool = Pool()
        Cashbook = pool.get('cashbook.book')
        BType = pool.get('cashbook.type')
        Category = pool.get('cashbook.category')
        Line = pool.get('cashbook.line')

        company = self.prep_company()
        with Transaction().set_context({'company': company.id}):
            as_cfg = self.prep_yield_config(
                'Fee', 'Dividend', 'Profit-Loss', company)

            type_depot = self.prep_type('Depot', 'D')
            self.prep_type('Cash', 'C')
            category_in = self.prep_category(name='Income', cattype='in')
            BType.write(*[
                [type_depot],
                {
                    'feature': 'asset',
                }])

            asset = self.prep_asset_item(
                company=company,
                product=self.prep_asset_product(name='Product 1'))
            self.assertEqual(asset.symbol, 'usd/u')

            book_asset, = Cashbook.create([{
                'name': 'Depot',
                'btype': type_depot.id,
                'company': company.id,
                'currency': company.currency.id,
                'number_sequ': self.prep_sequence().id,
                'asset': asset.id,
                'quantity_uom': asset.uom.id,
                'start_date': date(2022, 5, 1),
                'lines': [('create', [{
                    'bookingtype': 'in',
                    'date': date(2022, 5, 2),
                    'amount': Decimal('23.50'),
                    'quantity': Decimal('3.0'),
                    'category': category_in.id,
                    'description': 'Initial',
                    }, ])],
                }])

            Category.write(*[
                [as_cfg.dividend_category],
                {
                    'cattype': 'out',
                }])

            self.assertEqual(
                book_asset.rec_name,
                'Depot | 23.50 usd | Open | 3.0000 u')
            lines = Line.create([{
                'cashbook': book_asset.id,
                'date': date(2022, 5, 2),
                'bookingtype': 'out',
                'description': 'dividend minus',
                'category': as_cfg.dividend_category.id,
                'amount': Decimal('4.0'),
                'quantity': Decimal('0.0'),
                }])

            self.assertEqual(len(lines), 1)
            Line.wfcheck(lines)
            self.prep_valstore_run_worker()

            self.assertEqual(
                lines[0].rec_name,
                '05/02/2022|Exp|-4.00 usd|dividend minus [Dividend]|0.0000 u')

            self.assertEqual(lines[0].asset_gainloss, Decimal('0.0'))
            self.assertEqual(lines[0].asset_dividend, Decimal('-4.0'))
            self.assertEqual(lines[0].trade_fee, Decimal('0.0'))
            self.assertEqual(
                book_asset.rec_name,
                'Depot | 19.50 usd | Open | 3.0000 u')

    @with_transaction()
    def test_yield_dividend_transfer_from_splitbooking_cash_out(self):
        """ check out-booking, transfer from cash --> asset,
            dividend on counterpart of splitbooking
        """
        pool = Pool()
        Cashbook = pool.get('cashbook.book')
        BType = pool.get('cashbook.type')
        Line = pool.get('cashbook.line')

        company = self.prep_company()
        with Transaction().set_context({'company': company.id}):
            as_cfg = self.prep_yield_config(
                'Fee', 'Dividend', 'Profit-Loss', company)

            type_depot = self.prep_type('Depot', 'D')
            type_cash = self.prep_type('Cash', 'C')
            BType.write(*[
                [type_depot],
                {
                    'feature': 'asset',
                }])

            asset = self.prep_asset_item(
                company=company,
                product=self.prep_asset_product(name='Product 1'))
            self.assertEqual(asset.symbol, 'usd/u')
            category_in = self.prep_category(name='Income', cattype='in')

            book_cash, = Cashbook.create([{
                'name': 'Cash',
                'btype': type_cash.id,
                'company': company.id,
                'currency': company.currency.id,
                'number_sequ': self.prep_sequence().id,
                'start_date': date(2022, 5, 1),
                }])

            book_asset, = Cashbook.create([{
                'name': 'Depot',
                'btype': type_depot.id,
                'company': company.id,
                'currency': company.currency.id,
                'number_sequ': self.prep_sequence().id,
                'asset': asset.id,
                'quantity_uom': asset.uom.id,
                'start_date': date(2022, 5, 1),
                'lines': [('create', [{
                    'bookingtype': 'in',
                    'date': date(2022, 5, 1),
                    'amount': Decimal('23.50'),
                    'quantity': Decimal('3.0'),
                    'category': category_in.id,
                    'description': 'Initial',
                    }, ])],
                }])

            self.assertEqual(
                book_asset.rec_name,
                'Depot | 23.50 usd | Open | 3.0000 u')
            self.assertEqual(len(book_asset.lines), 1)
            self.assertEqual(book_cash.rec_name, 'Cash | 0.00 usd | Open')
            self.assertEqual(len(book_cash.lines), 0)

            Cashbook.write(*[
                [book_cash],
                {
                    'lines': [('create', [{
                        'bookingtype': 'spin',
                        'date': date(2022, 5, 2),
                        'description': 'buy shares, dividend',
                        'splitlines': [('create', [{
                            'splittype': 'tr',
                            'booktransf': book_asset.id,
                            'description': 'sell shares',
                            'quantity': Decimal('1.0'),
                            'amount': Decimal('10.0'),
                            }, {
                            'splittype': 'cat',
                            'category': as_cfg.dividend_category.id,
                            'description': 'dividend',
                            'amount': Decimal('10.0'),
                            }])],
                        }])],
                }])

            Line.wfcheck(book_cash.lines)
            self.prep_valstore_run_worker()

            self.assertEqual(
                book_asset.rec_name,
                'Depot | 13.50 usd | Open | 2.0000 u')
            self.assertEqual(len(book_asset.lines), 2)
            self.assertEqual(book_cash.rec_name, 'Cash | 20.00 usd | Open')
            self.assertEqual(len(book_cash.lines), 1)

            self.assertEqual(
                book_asset.lines[0].rec_name,
                '05/02/2022|to|-10.00 usd|sell shares [Cash | ' +
                '20.00 usd | Open]|-1.0000 u')
            self.assertEqual(
                book_asset.lines[1].rec_name,
                '05/01/2022|Rev|23.50 usd|Initial [Income]|3.0000 u')
            self.assertEqual(
                book_cash.lines[0].rec_name,
                '05/02/2022|Rev/Sp|20.00 usd|buy shares, dividend [-]')

            self.assertEqual(book_asset.lines[0].asset_gainloss, Decimal('0.0'))
            self.assertEqual(
                book_asset.lines[0].asset_dividend, Decimal('10.0'))
            self.assertEqual(book_asset.lines[0].trade_fee, Decimal('0.0'))

    @with_transaction()
    def test_yield_dividend_transfer_to_splitbooking_aset(self):
        """ check out-booking, transfer from asset --> cash,
            dividend on counterpart of splitbooking
        """
        pool = Pool()
        Cashbook = pool.get('cashbook.book')
        BType = pool.get('cashbook.type')
        Line = pool.get('cashbook.line')

        company = self.prep_company()
        with Transaction().set_context({'company': company.id}):
            as_cfg = self.prep_yield_config(
                'Fee', 'Dividend', 'Profit-Loss', company)

            type_depot = self.prep_type('Depot', 'D')
            type_cash = self.prep_type('Cash', 'C')
            BType.write(*[
                [type_depot],
                {
                    'feature': 'asset',
                }])

            asset = self.prep_asset_item(
                company=company,
                product=self.prep_asset_product(name='Product 1'))
            self.assertEqual(asset.symbol, 'usd/u')
            category_in = self.prep_category(name='Income', cattype='in')

            book_cash, = Cashbook.create([{
                'name': 'Cash',
                'btype': type_cash.id,
                'company': company.id,
                'currency': company.currency.id,
                'number_sequ': self.prep_sequence().id,
                'start_date': date(2022, 5, 1),
                }])

            book_asset, = Cashbook.create([{
                'name': 'Depot',
                'btype': type_depot.id,
                'company': company.id,
                'currency': company.currency.id,
                'number_sequ': self.prep_sequence().id,
                'asset': asset.id,
                'quantity_uom': asset.uom.id,
                'start_date': date(2022, 5, 1),
                'lines': [('create', [{
                    'bookingtype': 'in',
                    'date': date(2022, 5, 1),
                    'amount': Decimal('23.50'),
                    'quantity': Decimal('3.0'),
                    'category': category_in.id,
                    'description': 'Initial',
                    }, ])],
                }])

            self.assertEqual(
                book_asset.rec_name,
                'Depot | 23.50 usd | Open | 3.0000 u')
            self.assertEqual(len(book_asset.lines), 1)
            self.assertEqual(book_cash.rec_name, 'Cash | 0.00 usd | Open')
            self.assertEqual(len(book_cash.lines), 0)

            Cashbook.write(*[
                [book_asset],
                {
                    'lines': [('create', [{
                        'bookingtype': 'spin',
                        'date': date(2022, 5, 2),
                        'description': 'buy shares, dividend',
                        'splitlines': [('create', [{
                            'splittype': 'tr',
                            'booktransf': book_cash.id,
                            'description': 'buy shares',
                            'quantity': Decimal('1.0'),
                            'amount': Decimal('10.0'),
                            }, {
                            'splittype': 'cat',
                            'category': as_cfg.dividend_category.id,
                            'description': 'dividend',
                            'amount': Decimal('10.0'),
                            'quantity': Decimal('0.0'),
                            }])],
                        }])],
                }])

            Line.wfcheck(book_asset.lines)
            self.prep_valstore_run_worker()

            self.assertEqual(
                book_asset.rec_name,
                'Depot | 43.50 usd | Open | 4.0000 u')
            self.assertEqual(len(book_asset.lines), 2)
            self.assertEqual(book_cash.rec_name, 'Cash | -10.00 usd | Open')
            self.assertEqual(len(book_cash.lines), 1)

            self.assertEqual(
                book_asset.lines[0].rec_name,
                '05/01/2022|Rev|23.50 usd|Initial [Income]|3.0000 u')
            self.assertEqual(
                book_asset.lines[1].rec_name,
                '05/02/2022|Rev/Sp|20.00 usd|buy shares, dividend [-]|1.0000 u')
            self.assertEqual(
                book_cash.lines[0].rec_name,
                '05/02/2022|to|-10.00 usd|buy shares [Depot | ' +
                '43.50 usd | Open | 4.0000 u]')

            self.assertEqual(book_asset.lines[0].asset_gainloss, Decimal('0.0'))
            self.assertEqual(
                book_asset.lines[0].asset_dividend,
                Decimal('00.0'))
            self.assertEqual(book_asset.lines[0].trade_fee, Decimal('0.0'))

            self.assertEqual(book_asset.lines[1].asset_gainloss, Decimal('0.0'))
            self.assertEqual(
                book_asset.lines[1].asset_dividend,
                Decimal('10.0'))
            self.assertEqual(book_asset.lines[1].trade_fee, Decimal('0.0'))

    @with_transaction()
    def test_yield_gainloss_spout(self):
        """ check out-booking, split with fee and profit (1)
        """
        pool = Pool()
        Cashbook = pool.get('cashbook.book')
        BType = pool.get('cashbook.type')
        Line = pool.get('cashbook.line')

        company = self.prep_company()
        with Transaction().set_context({'company': company.id}):
            as_cfg = self.prep_yield_config(
                'Fee', 'Dividend', 'Profit-Loss', company)

            type_depot = self.prep_type('Depot', 'D')
            type_cash = self.prep_type('Cash', 'C')
            BType.write(*[
                [type_depot],
                {
                    'feature': 'asset',
                }])

            asset = self.prep_asset_item(
                company=company,
                product=self.prep_asset_product(name='Product 1'))
            self.assertEqual(asset.symbol, 'usd/u')

            book_cash, = Cashbook.create([{
                'name': 'Cash',
                'btype': type_cash.id,
                'company': company.id,
                'currency': company.currency.id,
                'number_sequ': self.prep_sequence().id,
                'start_date': date(2022, 5, 1),
                }])

            book_asset, = Cashbook.create([{
                'name': 'Depot',
                'btype': type_depot.id,
                'company': company.id,
                'currency': company.currency.id,
                'number_sequ': self.prep_sequence().id,
                'asset': asset.id,
                'quantity_uom': asset.uom.id,
                'start_date': date(2022, 5, 1),
                'lines': [('create', [{
                    'bookingtype': 'in',
                    'date': date(2022, 5, 1),
                    'amount': Decimal('23.50'),
                    'quantity': Decimal('3.0'),
                    'category': as_cfg.dividend_category.id,
                    'description': 'Initial (1)',
                    }, ])],
                }])

            # add counter-account for profit or loss of
            # depot-account
            book_gainloss = as_cfg.gainloss_book
            # sale all shares with profit and fee
            # buy:  23.50
            # sale: 32.90 (+40%)
            # fee:   2.50
            #                  asset (buy amount):   23.50
            # booking: asset -> cash:              - 30.40
            #          asset -> (category) fee:    -  2.50
            #          asset <- gain-loss:            9.40
            #                                      -------
            #                                         0.00
            self.assertEqual(
                book_asset.rec_name,
                'Depot | 23.50 usd | Open | 3.0000 u')
            self.assertEqual(
                book_gainloss.rec_name,
                'Profit-Loss | 0.00 usd | Open')
            lines = Line.create([{
                'cashbook': book_asset.id,
                'date': date(2022, 5, 2),
                'bookingtype': 'spout',
                'description': 'all out (1)',
                'splitlines': [('create', [{
                    'splittype': 'tr',
                    'booktransf': book_cash.id,
                    'description': 'sale with 40% profit (1)',
                    'quantity': Decimal('3.0'),
                    'amount': Decimal('30.4'),
                    }, {
                    'splittype': 'cat',
                    'description': 'trade fee (1)',
                    'category': as_cfg.fee_category.id,
                    'amount': Decimal('2.5'),
                    'quantity': Decimal('0.0'),
                    }, {
                    'splittype': 'tr',
                    'booktransf': book_gainloss.id,
                    'description': 'profit of sale (1)',
                    'amount': Decimal('-9.4'),
                    'quantity': Decimal('0.0'),
                    }])],
                }])

            self.assertEqual(len(lines), 1)
            self.assertEqual(
                lines[0].rec_name,
                '05/02/2022|Exp/Sp|-23.50 usd|all out (1) [-]|-3.0000 u')
            Line.wfcheck(lines)
            self.prep_valstore_run_worker()

            self.assertEqual(
                lines[0].rec_name,
                '05/02/2022|Exp/Sp|-23.50 usd|all out (1) [-]|-3.0000 u')
            self.assertEqual(len(lines[0].splitlines), 3)
            self.assertEqual(lines[0].reference, None)
            self.assertEqual(len(lines[0].references), 2)
            self.assertEqual(
                lines[0].references[0].rec_name,
                '05/02/2022|from|30.40 usd|sale with 40% profit (1) ' +
                '[Depot | 0.00 usd | Open | 0.0000 u]')
            self.assertEqual(
                lines[0].references[1].rec_name,
                '05/02/2022|from|-9.40 usd|profit of sale (1) ' +
                '[Depot | 0.00 usd | Open | 0.0000 u]')

            self.assertEqual(lines[0].asset_gainloss, Decimal('9.4'))
            self.assertEqual(lines[0].asset_dividend, Decimal('0.0'))
            self.assertEqual(lines[0].trade_fee, Decimal('2.5'))

            self.assertEqual(
                book_asset.rec_name,
                'Depot | 0.00 usd | Open | 0.0000 u')
            # negative amount on profit/loss-account means success
            self.assertEqual(
                book_gainloss.rec_name,
                'Profit-Loss | -9.40 usd | Open')

            # check searcher
            lines = Line.search([('asset_gainloss', '=', Decimal('9.4'))])
            self.assertEqual(len(lines), 1)
            self.assertEqual(
                lines[0].rec_name,
                '05/02/2022|Exp/Sp|-23.50 usd|all out (1) [-]|-3.0000 u')

    @with_transaction()
    def test_yield_gainloss_spin(self):
        """ check in-booking, split with profit (2)
        """
        pool = Pool()
        Cashbook = pool.get('cashbook.book')
        BType = pool.get('cashbook.type')
        Line = pool.get('cashbook.line')

        company = self.prep_company()
        with Transaction().set_context({'company': company.id}):
            as_cfg = self.prep_yield_config(
                'Fee', 'Dividend', 'Profit-Loss', company)

            type_depot = self.prep_type('Depot', 'D')
            type_cash = self.prep_type('Cash', 'C')
            BType.write(*[
                [type_depot],
                {
                    'feature': 'asset',
                }])

            asset = self.prep_asset_item(
                company=company,
                product=self.prep_asset_product(name='Product 1'))
            self.assertEqual(asset.symbol, 'usd/u')

            book_cash, = Cashbook.create([{
                'name': 'Cash',
                'btype': type_cash.id,
                'company': company.id,
                'currency': company.currency.id,
                'number_sequ': self.prep_sequence().id,
                'start_date': date(2022, 5, 1),
                }])

            book_asset, = Cashbook.create([{
                'name': 'Depot',
                'btype': type_depot.id,
                'company': company.id,
                'currency': company.currency.id,
                'number_sequ': self.prep_sequence().id,
                'asset': asset.id,
                'quantity_uom': asset.uom.id,
                'start_date': date(2022, 5, 1),
                'lines': [('create', [{
                    'bookingtype': 'in',
                    'date': date(2022, 5, 1),
                    'amount': Decimal('23.50'),
                    'quantity': Decimal('3.0'),
                    'category': as_cfg.dividend_category.id,
                    'description': 'Initial (2)',
                    }, ])],
                }])

            # add counter-account for profit or loss of
            # depot-account
            book_gainloss = as_cfg.gainloss_book

            self.assertEqual(
                book_asset.rec_name,
                'Depot | 23.50 usd | Open | 3.0000 u')
            self.assertEqual(
                book_gainloss.rec_name,
                'Profit-Loss | 0.00 usd | Open')
            lines = Line.create([{
                'cashbook': book_cash.id,
                'date': date(2022, 5, 2),
                'bookingtype': 'spin',
                'description': 'all out (2)',
                'splitlines': [('create', [{
                    'splittype': 'tr',
                    'booktransf': book_asset.id,
                    'description': 'sale with 40% profit (2)',
                    'quantity': Decimal('3.0'),
                    'amount': Decimal('30.4'),
                    }, ])],
                }, {
                'cashbook': book_gainloss.id,
                'date': date(2022, 5, 2),
                'bookingtype': 'spin',
                'description': 'profit (2)',
                'splitlines': [('create', [{
                    'splittype': 'tr',
                    'booktransf': book_asset.id,
                    'description': 'profit of sale (2)',
                    'amount': Decimal('-9.4'),
                    'quantity': Decimal('0.0'),
                    }])],
                }])

            self.assertEqual(len(lines), 2)
            Line.wfcheck(lines)
            self.prep_valstore_run_worker()

            self.assertEqual(
                lines[0].rec_name,
                '05/02/2022|Rev/Sp|30.40 usd|all out (2) [-]')
            self.assertEqual(len(lines[0].splitlines), 1)
            self.assertEqual(lines[0].reference, None)
            self.assertEqual(len(lines[0].references), 1)
            self.assertEqual(
                lines[0].references[0].rec_name,
                '05/02/2022|to|-30.40 usd|sale with 40% profit (2) ' +
                '[Cash | 30.40 usd | Open]|-3.0000 u')

            self.assertEqual(lines[0].asset_gainloss, None)
            self.assertEqual(lines[0].asset_dividend, None)
            self.assertEqual(lines[0].trade_fee, None)
            self.assertEqual(
                lines[0].references[0].asset_gainloss, Decimal('0.0'))
            self.assertEqual(
                lines[0].references[0].asset_dividend, Decimal('0.0'))
            self.assertEqual(
                lines[0].references[0].trade_fee, Decimal('0.0'))

            self.assertEqual(
                lines[1].rec_name,
                '05/02/2022|Rev/Sp|-9.40 usd|profit (2) [-]')
            self.assertEqual(len(lines[1].splitlines), 1)
            self.assertEqual(lines[1].reference, None)
            self.assertEqual(len(lines[1].references), 1)
            self.assertEqual(
                lines[1].references[0].rec_name,
                '05/02/2022|to|9.40 usd|profit of sale (2) [Profit-Loss' +
                ' | -9.40 usd | Open]|0.0000 u')

            self.assertEqual(lines[1].asset_gainloss, None)
            self.assertEqual(lines[1].asset_dividend, None)
            self.assertEqual(lines[1].trade_fee, None)
            self.assertEqual(
                lines[1].references[0].asset_gainloss, Decimal('9.4'))
            self.assertEqual(
                lines[1].references[0].asset_dividend, Decimal('0.0'))
            self.assertEqual(
                lines[1].references[0].trade_fee, Decimal('0.0'))

            self.assertEqual(
                book_asset.rec_name, 'Depot | 2.50 usd | Open | 0.0000 u')
            # negative amount on profit/loss-account means success
            self.assertEqual(
                book_gainloss.rec_name, 'Profit-Loss | -9.40 usd | Open')

            # check searcher
            lines = Line.search([('asset_gainloss', '=', Decimal('9.4'))])
            self.assertEqual(len(lines), 1)
            self.assertEqual(
                lines[0].rec_name,
                '05/02/2022|to|9.40 usd|profit of sale (2) [Profit-Loss' +
                ' | -9.40 usd | Open]|0.0000 u')

    @with_transaction()
    def test_yield_gainloss_spin2(self):
        """ check in-booking, split with profit (5)
        """
        pool = Pool()
        Cashbook = pool.get('cashbook.book')
        BType = pool.get('cashbook.type')
        Line = pool.get('cashbook.line')

        company = self.prep_company()
        with Transaction().set_context({'company': company.id}):
            as_cfg = self.prep_yield_config(
                'Fee', 'Dividend', 'Profit-Loss', company)

            type_depot = self.prep_type('Depot', 'D')
            type_cash = self.prep_type('Cash', 'C')
            BType.write(*[
                [type_depot],
                {
                    'feature': 'asset',
                }])

            asset = self.prep_asset_item(
                company=company,
                product=self.prep_asset_product(name='Product 1'))
            self.assertEqual(asset.symbol, 'usd/u')

            book_cash, = Cashbook.create([{
                'name': 'Cash',
                'btype': type_cash.id,
                'company': company.id,
                'currency': company.currency.id,
                'number_sequ': self.prep_sequence().id,
                'start_date': date(2022, 5, 1),
                }])

            book_asset, = Cashbook.create([{
                'name': 'Depot',
                'btype': type_depot.id,
                'company': company.id,
                'currency': company.currency.id,
                'number_sequ': self.prep_sequence().id,
                'asset': asset.id,
                'quantity_uom': asset.uom.id,
                'start_date': date(2022, 5, 1),
                'lines': [('create', [{
                    'bookingtype': 'in',
                    'date': date(2022, 5, 1),
                    'amount': Decimal('23.50'),
                    'quantity': Decimal('3.0'),
                    'category': as_cfg.dividend_category.id,
                    'description': 'Initial (2)',
                    }, ])],
                }])

            # add counter-account for profit or loss of
            # depot-account
            book_gainloss = as_cfg.gainloss_book

            self.assertEqual(
                book_asset.rec_name,
                'Depot | 23.50 usd | Open | 3.0000 u')
            self.assertEqual(
                book_gainloss.rec_name,
                'Profit-Loss | 0.00 usd | Open')
            lines = Line.create([{
                'cashbook': book_cash.id,
                'date': date(2022, 5, 2),
                'bookingtype': 'spout',
                'description': 'guv (5)',
                'splitlines': [('create', [{
                    'splittype': 'tr',
                    'booktransf': book_asset.id,
                    'description': 'profit/loss (5)',
                    'quantity': Decimal('-3.0'),
                    'amount': Decimal('-23.5'),
                    }, {
                    'splittype': 'tr',
                    'booktransf': book_gainloss.id,
                    'description': 'profit/loss (5)',
                    'amount': Decimal('-9.4'),
                    }, ])],
                }])

            self.assertEqual(len(lines), 1)
            Line.wfcheck(lines)
            self.prep_valstore_run_worker()

            self.assertEqual(
                lines[0].rec_name,
                '05/02/2022|Exp/Sp|32.90 usd|guv (5) [-]')
            self.assertEqual(len(lines[0].splitlines), 2)
            self.assertEqual(
                lines[0].splitlines[0].rec_name,
                'Exp/Sp|-23.50 usd|profit/loss (5) [Depot | 0.00 usd' +
                ' | Open | 0.0000 u]')
            self.assertEqual(
                lines[0].splitlines[1].rec_name,
                'Exp/Sp|-9.40 usd|profit/loss (5) [Profit-Loss | ' +
                '-9.40 usd | Open]')

            self.assertEqual(lines[0].reference, None)
            self.assertEqual(len(lines[0].references), 2)
            self.assertEqual(
                lines[0].references[0].rec_name,
                '05/02/2022|from|-23.50 usd|profit/loss (5) [Cash | ' +
                '32.90 usd | Open]|-3.0000 u')
            self.assertEqual(
                lines[0].references[1].rec_name,
                '05/02/2022|from|-9.40 usd|profit/loss (5) [Cash | ' +
                '32.90 usd | Open]')

            self.assertEqual(lines[0].asset_gainloss, None)
            self.assertEqual(lines[0].asset_dividend, None)
            self.assertEqual(lines[0].trade_fee, None)
            self.assertEqual(
                lines[0].references[0].asset_gainloss, Decimal('9.4'))
            self.assertEqual(
                lines[0].references[0].asset_dividend, Decimal('0.0'))
            self.assertEqual(
                lines[0].references[0].trade_fee, Decimal('0.0'))

            self.assertEqual(
                book_asset.rec_name, 'Depot | 0.00 usd | Open | 0.0000 u')
            self.assertEqual(
                book_gainloss.rec_name, 'Profit-Loss | -9.40 usd | Open')

            # check searcher
            lines = Line.search([('asset_gainloss', '=', Decimal('9.4'))])
            self.assertEqual(len(lines), 1)
            self.assertEqual(
                lines[0].rec_name,
                '05/02/2022|from|-23.50 usd|profit/loss (5) [Cash | ' +
                '32.90 usd | Open]|-3.0000 u')

    @with_transaction()
    def test_yield_gainloss_mvout(self):
        """ check out-booking, transfer with profit-account, fee
            2x transfer, 1x category, 3x transfers (3)
        """
        pool = Pool()
        Cashbook = pool.get('cashbook.book')
        BType = pool.get('cashbook.type')
        Line = pool.get('cashbook.line')

        company = self.prep_company()
        with Transaction().set_context({'company': company.id}):
            as_cfg = self.prep_yield_config(
                'Fee', 'Dividend', 'Profit-Loss', company)

            type_depot = self.prep_type('Depot', 'D')
            type_cash = self.prep_type('Cash', 'C')
            BType.write(*[
                [type_depot],
                {
                    'feature': 'asset',
                }])

            asset = self.prep_asset_item(
                company=company,
                product=self.prep_asset_product(name='Product 1'))
            self.assertEqual(asset.symbol, 'usd/u')

            book_cash, = Cashbook.create([{
                'name': 'Cash',
                'btype': type_cash.id,
                'company': company.id,
                'currency': company.currency.id,
                'number_sequ': self.prep_sequence().id,
                'start_date': date(2022, 5, 1),
                }])

            book_asset, = Cashbook.create([{
                'name': 'Depot',
                'btype': type_depot.id,
                'company': company.id,
                'currency': company.currency.id,
                'number_sequ': self.prep_sequence().id,
                'asset': asset.id,
                'quantity_uom': asset.uom.id,
                'start_date': date(2022, 5, 1),
                'lines': [('create', [{
                    'bookingtype': 'in',
                    'date': date(2022, 5, 1),
                    'amount': Decimal('23.50'),
                    'quantity': Decimal('3.0'),
                    'category': as_cfg.dividend_category.id,
                    'description': 'Initial (3)',
                    }, ])],
                }])

            # add counter-account for profit or loss of
            # depot-account
            book_gainloss = as_cfg.gainloss_book
            # sale all shares with profit and fee
            # buy:  23.50
            # sale: 32.90 (+40%)
            # fee:   2.50
            #                  asset (buy amount):   23.50
            # booking: asset -> cash:              - 30.40
            #          asset -> (category) fee:    -  2.50
            #          asset <- gain-loss:            9.40
            #                                      -------
            #                                         0.00
            self.assertEqual(
                book_asset.rec_name,
                'Depot | 23.50 usd | Open | 3.0000 u')
            self.assertEqual(
                book_gainloss.rec_name,
                'Profit-Loss | 0.00 usd | Open')
            lines = Line.create([{
                'cashbook': book_asset.id,
                'date': date(2022, 5, 2),
                'bookingtype': 'mvout',
                'booktransf': book_cash.id,
                'description': 'sale with 40% profit (3)',
                'quantity': Decimal('3.0'),
                'amount': Decimal('30.4'),
                }, {
                'cashbook': book_asset.id,
                'date': date(2022, 5, 2),
                'bookingtype': 'out',
                'description': 'trade fee (3)',
                'category': as_cfg.fee_category.id,
                'quantity': Decimal('0.0'),
                'amount': Decimal('2.5'),
                }, {
                'cashbook': book_asset.id,
                'date': date(2022, 5, 2),
                'bookingtype': 'mvin',
                'description': 'profit of sale (3)',
                'booktransf': book_gainloss.id,
                'quantity': Decimal('0.0'),
                'amount': Decimal('9.4'),
                }])

            self.assertEqual(len(lines), 3)
            Line.wfcheck(lines)
            self.prep_valstore_run_worker()

            self.assertEqual(
                lines[0].rec_name,
                '05/02/2022|to|-30.40 usd|sale with 40% profit (3) ' +
                '[Cash | 30.40 usd | Open]|-3.0000 u')
            self.assertEqual(lines[0].asset_gainloss, Decimal('0.0'))
            self.assertEqual(lines[0].asset_dividend, Decimal('0.0'))
            self.assertEqual(lines[0].trade_fee, Decimal('0.0'))

            self.assertEqual(
                lines[1].rec_name,
                '05/02/2022|Exp|-2.50 usd|trade fee (3) [Fee]|0.0000 u')
            self.assertEqual(lines[1].asset_gainloss, Decimal('0.0'))
            self.assertEqual(lines[1].asset_dividend, Decimal('0.0'))
            self.assertEqual(lines[1].trade_fee, Decimal('2.5'))

            self.assertEqual(
                lines[2].rec_name,
                '05/02/2022|from|9.40 usd|profit of sale (3) ' +
                '[Profit-Loss | -9.40 usd | Open]|0.0000 u')
            self.assertEqual(lines[2].asset_gainloss, Decimal('9.4'))
            self.assertEqual(lines[2].asset_dividend, Decimal('0.0'))
            self.assertEqual(lines[2].trade_fee, Decimal('0.0'))

            self.assertEqual(
                book_asset.rec_name, 'Depot | 0.00 usd | Open | 0.0000 u')
            self.assertEqual(
                book_gainloss.rec_name, 'Profit-Loss | -9.40 usd | Open')
            self.assertEqual(
                book_cash.rec_name, 'Cash | 30.40 usd | Open')

            # check searcher
            lines = Line.search([('asset_gainloss', '=', Decimal('9.4'))])
            self.assertEqual(len(lines), 1)

    @with_transaction()
    def test_yield_gainloss_mv_sp(self):
        """ check out-booking, transfer with profit-account, fee
            2x transfer, 1x category, 1x transfer to splitbooking (4)
        """
        pool = Pool()
        Cashbook = pool.get('cashbook.book')
        BType = pool.get('cashbook.type')
        Line = pool.get('cashbook.line')

        company = self.prep_company()
        with Transaction().set_context({'company': company.id}):
            as_cfg = self.prep_yield_config(
                'Fee', 'Dividend', 'Profit-Loss', company)

            type_depot = self.prep_type('Depot', 'D')
            type_cash = self.prep_type('Cash', 'C')
            BType.write(*[
                [type_depot],
                {
                    'feature': 'asset',
                }])

            asset = self.prep_asset_item(
                company=company,
                product=self.prep_asset_product(name='Product 1'))
            self.assertEqual(asset.symbol, 'usd/u')

            book_cash, = Cashbook.create([{
                'name': 'Cash',
                'btype': type_cash.id,
                'company': company.id,
                'currency': company.currency.id,
                'number_sequ': self.prep_sequence().id,
                'start_date': date(2022, 5, 1),
                }])

            book_asset, = Cashbook.create([{
                'name': 'Depot',
                'btype': type_depot.id,
                'company': company.id,
                'currency': company.currency.id,
                'number_sequ': self.prep_sequence().id,
                'asset': asset.id,
                'quantity_uom': asset.uom.id,
                'start_date': date(2022, 5, 1),
                'lines': [('create', [{
                    'bookingtype': 'in',
                    'date': date(2022, 5, 1),
                    'amount': Decimal('23.50'),
                    'quantity': Decimal('3.0'),
                    'category': as_cfg.dividend_category.id,
                    'description': 'Initial (4)',
                    }, ])],
                }])

            # add counter-account for profit or loss of
            # depot-account
            book_gainloss = as_cfg.gainloss_book
            # sale all shares with profit and fee
            # buy:  23.50
            # sale: 32.90 (+40%)
            # fee:   2.50
            #                  asset (buy amount):   23.50
            # booking: asset -> cash:              - 30.40
            #          asset -> (category) fee:    -  2.50
            #          asset <- gain-loss:            9.40
            #                                      -------
            #                                         0.00
            self.assertEqual(
                book_asset.rec_name, 'Depot | 23.50 usd | Open | 3.0000 u')
            self.assertEqual(
                book_gainloss.rec_name, 'Profit-Loss | 0.00 usd | Open')
            lines = Line.create([{
                'cashbook': book_cash.id,
                'date': date(2022, 5, 2),
                'bookingtype': 'spout',     # negate transaction, because the
                'description': 'all out (4)',  # category 'as_cfg.fee_category'
                'splitlines': [('create', [{   # is for out-only
                    'splittype': 'tr',
                    'booktransf': book_asset.id,
                    'description': 'sale with 40% profit (4)',
                    'quantity': Decimal('-3.0'),
                    'amount': Decimal('-32.9'),     # profit + fee
                    }, {
                    'splittype': 'cat',
                    'category': as_cfg.fee_category.id,
                    'description': 'trade fee (4)',
                    'amount': Decimal('2.5'),       # fee
                    }])],
                }, {
                'cashbook': book_asset.id,
                'date': date(2022, 5, 2),
                'bookingtype': 'mvin',
                'booktransf': book_gainloss.id,
                'amount': Decimal('9.4'),
                'quantity': Decimal('0.0'),
                'description': 'gainloss_mv_sp (4)',
                }])

            self.assertEqual(len(lines), 2)
            Line.wfcheck(lines)
            self.prep_valstore_run_worker()

            self.assertEqual(
                lines[0].rec_name,
                '05/02/2022|Exp/Sp|30.40 usd|all out (4) [-]')
            # non-asset cashbook
            self.assertEqual(lines[0].asset_gainloss, None)
            self.assertEqual(lines[0].asset_dividend, None)
            self.assertEqual(lines[0].trade_fee, None)
            self.assertEqual(lines[0].reference, None)
            self.assertEqual(len(lines[0].references), 1)
            self.assertEqual(
                lines[0].references[0].rec_name,
                '05/02/2022|from|-32.90 usd|sale with 40% profit (4) ' +
                '[Cash | 30.40 usd | Open]|-3.0000 u')
            self.assertEqual(
                lines[0].references[0].asset_gainloss, Decimal('0.0'))
            self.assertEqual(
                lines[0].references[0].asset_dividend, Decimal('0.0'))
            self.assertEqual(lines[0].references[0].trade_fee, Decimal('2.5'))

            self.assertEqual(
                lines[1].rec_name,
                '05/02/2022|from|9.40 usd|gainloss_mv_sp (4) [Profit-Loss' +
                ' | -9.40 usd | Open]|0.0000 u')
            self.assertEqual(lines[1].asset_gainloss, Decimal('9.4'))
            self.assertEqual(lines[1].asset_dividend, Decimal('0.0'))
            self.assertEqual(lines[1].trade_fee, Decimal('0.0'))
            self.assertEqual(lines[1].reference, None)
            self.assertEqual(len(lines[1].references), 1)
            self.assertEqual(
                lines[1].references[0].rec_name,
                '05/02/2022|to|-9.40 usd|gainloss_mv_sp (4) [Depot | ' +
                '0.00 usd | Open | 0.0000 u]')

            self.assertEqual(
                book_asset.rec_name, 'Depot | 0.00 usd | Open | 0.0000 u')
            self.assertEqual(
                book_gainloss.rec_name, 'Profit-Loss | -9.40 usd | Open')
            self.assertEqual(
                book_cash.rec_name, 'Cash | 30.40 usd | Open')

            # check searcher
            lines = Line.search([('asset_gainloss', '=', Decimal('9.4'))])
            self.assertEqual(len(lines), 1)

# end YieldTestCase
