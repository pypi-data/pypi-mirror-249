# -*- coding: utf-8 -*-
# This file is part of the cashbook-module from m-ds for Tryton.
# The COPYRIGHT file at the top level of this repository contains the
# full copyright notices and license terms.

from trytond.tests.test_tryton import with_transaction
from trytond.pool import Pool
from trytond.transaction import Transaction
from trytond.exceptions import UserError
from datetime import date
from decimal import Decimal


class CbInvTestCase(object):

    @with_transaction()
    def test_assetbook_create(self):
        """ create cashbook, set 'btype' to asset
        """
        pool = Pool()
        Book = pool.get('cashbook.book')
        BType = pool.get('cashbook.type')

        types = self.prep_type()
        company = self.prep_company()
        with Transaction().set_context({'company': company.id}):
            book, = Book.create([{
                'name': 'Book 1',
                'btype': types.id,
                'company': company.id,
                'currency': company.currency.id,
                'number_sequ': self.prep_sequence().id,
                }])

            BType.write(*[
                [types],
                {
                    'feature': 'asset',
                }])

            self.assertEqual(book.name, 'Book 1')
            self.assertEqual(
                book.rec_name, 'Book 1 | 0.00 usd | Open | 0.0000 -')
            self.assertEqual(book.btype.rec_name, 'CAS - Cash')
            self.assertEqual(book.state, 'open')
            self.assertEqual(book.state_string, 'Open')
            self.assertEqual(book.feature, 'asset')
            self.assertEqual(book.quantity_digits, 4)
            self.assertEqual(book.show_performance, True)

            # run sorter
            books = Book.search(
                [],
                order=[
                    ('current_value', 'ASC'),
                    ('purchase_amount', 'ASC'),
                    ('diff_amount', 'ASC'),
                    ('yield_balance', 'ASC'),
                    ('diff_percent', 'ASC'),
                    ('quantity', 'ASC'),
                    ('quantity_all', 'ASC'),
                    ('yield_sales', 'ASC'),
                    ('yield_sales_12m', 'ASC'),
                    ('yield_dividend_total', 'ASC'),
                    ('yield_dividend_12m', 'ASC'),
                    ('yield_fee_total', 'ASC'),
                    ('yield_fee_12m', 'ASC'),
                    ])

    @with_transaction()
    def test_assetbook_aggregated_values(self):
        """ create cashbooks with hierarchy, add lines,
            check values at non-type-books
        """
        pool = Pool()
        Book = pool.get('cashbook.book')
        BType = pool.get('cashbook.type')
        Asset = pool.get('investment.asset')

        company = self.prep_company()
        with Transaction().set_context({'company': company.id}):
            type_depot = self.prep_type('Depot', 'D')
            type_cash = self.prep_type('Cash', 'C')
            category_in = self.prep_category(cattype='in')

            asset = self.prep_asset_item(
                company=company,
                product=self.prep_asset_product(name='Product 1'))
            self.assertEqual(asset.symbol, 'usd/u')

            Asset.write(*[
                [asset],
                {
                    'rates': [('create', [{
                        'date': date(2022, 5, 1),
                        'rate': Decimal('10.0'),
                        }, {
                        'date': date(2022, 5, 2),
                        'rate': Decimal('12.5'),
                        }])],
                }])
            self.assertEqual(
                asset.rec_name, 'Product 1 | 12.5000 usd/u | 05/02/2022')

            (usd, euro) = self.prep_2nd_currency(company)
            self.assertEqual(company.currency.rec_name, 'Euro')

            BType.write(*[
                [type_depot],
                {
                    'feature': 'asset',
                }])

            books = Book.create([{
                'name': 'L0-Euro-None',
                'btype': None,
                'company': company.id,
                'currency': euro.id,
                'number_sequ': self.prep_sequence().id,
                'start_date': date(2022, 5, 1),
                'childs': [('create', [{
                    'name': 'L1-Euro-Cash',
                    'btype': type_cash.id,
                    'company': company.id,
                    'currency': euro.id,
                    'number_sequ': self.prep_sequence().id,
                    'start_date': date(2022, 5, 1),
                    'lines': [('create', [{
                        'date': date(2022, 5, 1),
                        'description': 'Cat In',
                        'category': category_in.id,
                        'bookingtype': 'in',
                        'amount': Decimal('15.0'),
                        }])],
                    }, {
                    'name': 'L1-USD-Cash',
                    'btype': type_cash.id,
                    'company': company.id,
                    'currency': usd.id,
                    'number_sequ': self.prep_sequence().id,
                    'start_date': date(2022, 5, 1),
                    'lines': [('create', [{
                        'date': date(2022, 5, 1),
                        'description': 'Cat In',
                        'category': category_in.id,
                        'bookingtype': 'in',
                        'amount': Decimal('15.0'),  # 14.29 €
                        }])],
                    }, {
                    'name': 'L1-Euro-Depot',
                    'btype': type_depot.id,
                    'company': company.id,
                    'currency': euro.id,
                    'number_sequ': self.prep_sequence().id,
                    'start_date': date(2022, 5, 1),
                    'asset': asset.id,
                    'quantity_uom': asset.uom.id,
                    'lines': [('create', [{
                        'date': date(2022, 5, 1),
                        'description': 'Cat In',
                        'category': category_in.id,
                        'bookingtype': 'in',
                        'amount': Decimal('15.0'),
                        'quantity': Decimal('1.0'),
                        }])],
                    }, {
                    'name': 'L1-USD-Depot',
                    'btype': type_depot.id,
                    'company': company.id,
                    'currency': usd.id,
                    'number_sequ': self.prep_sequence().id,
                    'start_date': date(2022, 5, 1),
                    'asset': asset.id,
                    'quantity_uom': asset.uom.id,
                    'lines': [('create', [{
                        'date': date(2022, 5, 1),
                        'description': 'Cat In',
                        'category': category_in.id,
                        'bookingtype': 'in',
                        'amount': Decimal('15.0'),  # 14.29 €
                        'quantity': Decimal('1.0'),
                        }])],
                    }])],
                }])
            self.assertEqual(len(books), 1)
            self.assertEqual(books[0].rec_name, 'L0-Euro-None')
            self.assertEqual(books[0].balance, Decimal('58.57'))
            self.assertEqual(books[0].balance_ref, Decimal('58.57'))
            # balance of asset-books: 29,286 €
            # value of asset-books: 11.9€ + 12.5USD/1.05 = 23.8€
            self.assertEqual(books[0].current_value, Decimal('23.8'))
            self.assertEqual(books[0].current_value_ref, Decimal('23.8'))
            self.assertEqual(books[0].diff_amount, Decimal('-5.49'))
            self.assertEqual(books[0].diff_percent, Decimal('-18.74'))

            # searcher
            self.assertEqual(Book.search_count([
                ('current_value', '=', Decimal('23.8'))]), 1)
            self.assertEqual(Book.search_count([
                ('current_value_ref', '=', Decimal('23.8'))]), 1)
            self.assertEqual(Book.search_count([
                ('diff_amount', '=', Decimal('-5.49'))]), 1)
            self.assertEqual(Book.search_count([
                ('diff_percent', '=', Decimal('-18.74'))]), 1)
            self.assertEqual(Book.search_count([
                ('quantity', '=', Decimal('1.0'))]), 2)
            self.assertEqual(Book.search_count([
                ('quantity_all', '=', Decimal('1.0'))]), 2)
            self.assertEqual(Book.search_count([
                ('current_rate', '=', Decimal('11.9'))]), 1)
            self.assertEqual(Book.search_count([
                ('purchase_amount', '=', Decimal('15.0'))]), 2)

            self.assertEqual(len(books[0].childs), 4)

            self.assertEqual(
                books[0].childs[0].rec_name,
                'L0-Euro-None/L1-Euro-Cash | 15.00 € | Open')
            self.assertEqual(books[0].childs[0].current_value, None)
            self.assertEqual(books[0].childs[0].current_value_ref, None)
            self.assertEqual(books[0].childs[0].diff_amount, None)
            self.assertEqual(books[0].childs[0].diff_percent, None)

            self.assertEqual(
                books[0].childs[1].rec_name,
                'L0-Euro-None/L1-Euro-Depot | 15.00 € | Open | 1.0000 u')
            self.assertEqual(
                books[0].childs[1].asset.rec_name,
                'Product 1 | 12.5000 usd/u | 05/02/2022')
            self.assertEqual(
                books[0].childs[1].current_value, Decimal('11.9'))
            self.assertEqual(
                books[0].childs[1].current_value_ref, Decimal('11.9'))
            self.assertEqual(
                books[0].childs[1].diff_amount, Decimal('-3.1'))
            self.assertEqual(
                books[0].childs[1].diff_percent, Decimal('-20.67'))

            self.assertEqual(
                books[0].childs[2].rec_name,
                'L0-Euro-None/L1-USD-Cash | 15.00 usd | Open')
            self.assertEqual(books[0].childs[2].current_value, None)
            self.assertEqual(books[0].childs[2].current_value_ref, None)
            self.assertEqual(books[0].childs[2].diff_amount, None)
            self.assertEqual(books[0].childs[2].diff_percent, None)

            self.assertEqual(
                books[0].childs[3].rec_name,
                'L0-Euro-None/L1-USD-Depot | 15.00 usd | Open | 1.0000 u')
            self.assertEqual(
                books[0].childs[3].asset.rec_name,
                'Product 1 | 12.5000 usd/u | 05/02/2022')
            self.assertEqual(
                books[0].childs[3].current_value, Decimal('12.5'))
            self.assertEqual(
                books[0].childs[3].current_value_ref, Decimal('11.9'))
            self.assertEqual(
                books[0].childs[3].diff_amount, Decimal('-2.5'))
            self.assertEqual(
                books[0].childs[3].diff_percent, Decimal('-16.67'))

    @with_transaction()
    def test_assetbook_create_line(self):
        """ create cashbook, add line
        """
        pool = Pool()
        Book = pool.get('cashbook.book')
        Line = pool.get('cashbook.line')
        BType = pool.get('cashbook.type')
        Asset = pool.get('investment.asset')

        company = self.prep_company()
        with Transaction().set_context({'company': company.id}):
            types = self.prep_type()
            BType.write(*[
                [types],
                {
                    'feature': 'asset',
                }])
            category = self.prep_category(cattype='in')

            party = self.prep_party()
            asset = self.prep_asset_item(
                company=company,
                product=self.prep_asset_product(name='Product 1'))

            Asset.write(*[
                [asset],
                {
                    'rates': [('create', [{
                        'date': date(2022, 5, 1),
                        'rate': Decimal('2.5'),
                        }, {
                        'date': date(2022, 5, 2),
                        'rate': Decimal('2.8'),
                        }])],
                }])
            self.assertEqual(
                asset.rec_name, 'Product 1 | 2.8000 usd/u | 05/02/2022')

            (usd, euro) = self.prep_2nd_currency(company)
            self.assertEqual(company.currency.rec_name, 'Euro')
            self.assertEqual(asset.symbol, 'usd/u')

            book, = Book.create([{
                'start_date': date(2022, 4, 1),
                'name': 'Book 1',
                'btype': types.id,
                'company': company.id,
                'currency': euro.id,
                'number_sequ': self.prep_sequence().id,
                'asset': asset.id,
                'quantity_uom': asset.uom.id,
                'quantity_digits': 3,
                'lines': [('create', [{
                        'date': date(2022, 5, 1),
                        'description': 'Text 1',
                        'category': category.id,
                        'bookingtype': 'in',
                        'amount': Decimal('2.5'),
                        'party': party.id,
                        'quantity': Decimal('1.453'),
                        }, {
                        'date': date(2022, 5, 10),
                        'description': 'Text 2',
                        'category': category.id,
                        'bookingtype': 'in',
                        'amount': Decimal('4.0'),
                        'party': party.id,
                        'quantity': Decimal('3.3'),
                        }],
                    )],
                }])

            self.assertEqual(book.name, 'Book 1')
            self.assertEqual(book.rec_name, 'Book 1 | 6.50 € | Open | 4.753 u')
            self.assertEqual(book.state, 'open')
            self.assertEqual(book.feature, 'asset')
            self.assertEqual(book.quantity_digits, 3)
            self.assertEqual(book.balance_all, Decimal('6.5'))
            self.assertEqual(len(book.lines), 2)

            self.assertEqual(book.lines[0].amount, Decimal('2.5'))
            self.assertEqual(book.lines[0].quantity, Decimal('1.453'))
            self.assertEqual(book.lines[0].quantity_credit, Decimal('1.453'))
            self.assertEqual(book.lines[0].quantity_debit, Decimal('0.0'))
            self.assertEqual(book.lines[0].quantity_digits, 3)
            self.assertEqual(book.lines[0].quantity_uom.symbol, 'u')
            self.assertEqual(book.lines[0].current_value, Decimal('3.88'))
            self.assertEqual(book.lines[0].diff_amount, Decimal('1.38'))
            self.assertEqual(book.lines[0].diff_percent, Decimal('55.18'))

            self.assertEqual(book.lines[1].amount, Decimal('4.0'))
            self.assertEqual(book.lines[1].quantity, Decimal('3.3'))
            self.assertEqual(book.lines[1].quantity_credit, Decimal('3.3'))
            self.assertEqual(book.lines[1].quantity_debit, Decimal('0.0'))
            self.assertEqual(book.lines[1].quantity_digits, 3)
            self.assertEqual(book.lines[1].quantity_uom.symbol, 'u')

            self.assertEqual(book.symbol, '€/u')
            self.assertEqual(
                book.asset.rec_name,
                'Product 1 | 2.8000 usd/u | 05/02/2022')

            # wf --> check
            Line.wfcheck(book.lines)
            self.prep_valstore_run_worker()

            # check quantities at cashbook
            with Transaction().set_context({
                    'date': date(2022, 5, 5)}):
                book2, = Book.browse([book])
                self.assertEqual(book.asset.rate, Decimal('2.8'))   # usd
                self.assertEqual(book2.quantity, Decimal('1.453'))
                self.assertEqual(book2.quantity_all, Decimal('4.753'))
                # 2.8 / 1.05 * 1.453 = 3.87466
                self.assertEqual(book2.current_value, Decimal('3.87'))
                self.assertEqual(book2.current_value_ref, Decimal('3.87'))

            with Transaction().set_context({
                    'date': date(2022, 5, 12)}):
                book2, = Book.browse([book])
                self.assertEqual(book2.quantity, Decimal('4.753'))
                self.assertEqual(book2.quantity_all, Decimal('4.753'))
                # 2.8 / 1.05 * 4.753 = 12.67466
                self.assertEqual(book2.current_value, Decimal('12.67'))
                self.assertEqual(book2.current_value_ref, Decimal('12.67'))

    @with_transaction()
    def test_assetbook_check_uom_and_currency_convert(self):
        """ asset in US$/Ounce, cashbook in EUR/Gram
        """
        pool = Pool()
        Book = pool.get('cashbook.book')
        BType = pool.get('cashbook.type')
        Asset = pool.get('investment.asset')
        ProdTempl = pool.get('product.template')
        Uom = pool.get('product.uom')

        company = self.prep_company()
        with Transaction().set_context({'company': company.id}):
            types = self.prep_type()
            BType.write(*[
                [types],
                {
                    'feature': 'asset',
                }])
            category = self.prep_category(cattype='in')

            party = self.prep_party()
            asset = self.prep_asset_item(
                company=company,
                product=self.prep_asset_product(name='Product 1'))

            # set product to ounce
            ounce, = Uom.search([('symbol', '=', 'oz')])
            gram, = Uom.search([('symbol', '=', 'g')])

            ProdTempl.write(*[
                [asset.product.template],
                {
                    'default_uom': ounce.id,
                    'name': 'Aurum',
                }])

            Asset.write(*[
                [asset],
                {
                    'uom': ounce.id,
                    'rates': [('create', [{
                        'date': date(2022, 5, 1),
                        'rate': Decimal('1750.0'),
                        }, ])],
                }])
            self.assertEqual(
                asset.rec_name,
                'Aurum | 1,750.0000 usd/oz | 05/01/2022')

            (usd, euro) = self.prep_2nd_currency(company)

            usd.rates[0].date = date(2022, 5, 1)
            usd.rates[0].save()
            self.assertEqual(len(usd.rates), 1)
            self.assertEqual(usd.rates[0].date, date(2022, 5, 1))

            euro.rates[0].date = date(2022, 5, 1)
            euro.rates[0].save()
            self.assertEqual(len(euro.rates), 1)
            self.assertEqual(euro.rates[0].date, date(2022, 5, 1))

            self.assertEqual(company.currency.rec_name, 'Euro')
            self.assertEqual(asset.symbol, 'usd/oz')

            book, = Book.create([{
                'start_date': date(2022, 4, 1),
                'name': 'Aurum-Storage',
                'btype': types.id,
                'company': company.id,
                'currency': euro.id,
                'number_sequ': self.prep_sequence().id,
                'asset': asset.id,
                'quantity_uom': gram.id,
                'quantity_digits': 3,
                'lines': [('create', [{
                        'date': date(2022, 5, 1),
                        'description': 'store some metal',
                        'category': category.id,
                        'bookingtype': 'in',
                        'amount': Decimal('1250.0'),
                        'party': party.id,
                        'quantity': Decimal('20.0'),
                        }],
                    )],
                }])

            self.assertEqual(
                book.rec_name,
                'Aurum-Storage | 1,250.00 € | Open | 20.000 g')
            self.assertEqual(book.balance_all, Decimal('1250.0'))
            self.assertEqual(len(book.lines), 1)

            self.assertEqual(book.lines[0].amount, Decimal('1250.0'))
            self.assertEqual(book.lines[0].quantity, Decimal('20.0'))
            self.assertEqual(book.lines[0].quantity_uom.symbol, 'g')

            self.assertEqual(book.symbol, '€/g')
            self.assertEqual(
                book.asset.rec_name,
                'Aurum | 1,750.0000 usd/oz | 05/01/2022')

            # check quantities at cashbook
            with Transaction().set_context({
                    'date': date(2022, 5, 1)}):
                book2, = Book.browse([book])
                self.assertEqual(book.asset.rate, Decimal('1750.0'))   # usd
                self.assertEqual(book2.quantity, Decimal('20.0'))
                self.assertEqual(book2.quantity_all, Decimal('20.0'))
                # usd --> eur: 1750 US$ / 1.05 = 1666.666 €
                # 1 ounce --> 20 gram: 1666.666 € * 20 / 28.3495 = 1175.7996 €
                # better we use 'Troy Ounce': 1 oz.tr. = 31.1034768 gram
                self.assertEqual(book2.current_value, Decimal('1175.80'))
                self.assertEqual(book2.current_value_ref, Decimal('1175.80'))
                self.assertEqual(book2.diff_amount, Decimal('-74.20'))
                self.assertEqual(book2.diff_percent, Decimal('-5.94'))
                self.assertEqual(book2.current_rate, Decimal('58.79'))

    @with_transaction()
    def test_assetbook_check_uom_and_currency_convert2(self):
        """ asset in US$/Ounce, cashbook in CHF/Gram,
            company-currency EUR
        """
        pool = Pool()
        Book = pool.get('cashbook.book')
        BType = pool.get('cashbook.type')
        Asset = pool.get('investment.asset')
        ProdTempl = pool.get('product.template')
        Uom = pool.get('product.uom')
        Currency = pool.get('currency.currency')

        company = self.prep_company()
        with Transaction().set_context({'company': company.id}):
            types = self.prep_type()
            BType.write(*[
                [types],
                {
                    'feature': 'asset',
                }])
            category = self.prep_category(cattype='in')

            party = self.prep_party()
            asset = self.prep_asset_item(
                company=company,
                product=self.prep_asset_product(name='Product 1'))

            # set product to ounce
            ounce, = Uom.search([('symbol', '=', 'oz')])
            gram, = Uom.search([('symbol', '=', 'g')])

            ProdTempl.write(*[
                [asset.product.template],
                {
                    'default_uom': ounce.id,
                    'name': 'Aurum',
                }])

            Asset.write(*[
                [asset],
                {
                    'uom': ounce.id,
                    'rates': [('create', [{
                        'date': date(2022, 5, 1),
                        'rate': Decimal('1750.0'),
                        }, ])],
                }])
            self.assertEqual(
                asset.rec_name,
                'Aurum | 1,750.0000 usd/oz | 05/01/2022')

            (usd, euro) = self.prep_2nd_currency(company)
            usd.rates[0].date = date(2022, 5, 1)
            usd.rates[0].save()
            self.assertEqual(len(usd.rates), 1)
            self.assertEqual(usd.rates[0].date, date(2022, 5, 1))

            euro.rates[0].date = date(2022, 5, 1)
            euro.rates[0].save()
            self.assertEqual(len(euro.rates), 1)
            self.assertEqual(euro.rates[0].date, date(2022, 5, 1))

            self.assertEqual(company.currency.rec_name, 'Euro')
            self.assertEqual(asset.symbol, 'usd/oz')
            chf, = Currency.create([{
                'name': 'Swiss Franc',
                'code': 'CHF',
                'numeric_code': '756',
                'symbol': 'CHF',
                'rounding': Decimal('0.01'),
                'digits': 2,
                'rates': [('create', [{
                    'date': date(2022, 5, 1),
                    'rate': Decimal('0.95'),
                    }])],
                }])

            book, = Book.create([{
                'start_date': date(2022, 4, 1),
                'name': 'Aurum-Storage',
                'btype': types.id,
                'company': company.id,
                'currency': chf.id,
                'number_sequ': self.prep_sequence().id,
                'asset': asset.id,
                'quantity_uom': gram.id,
                'quantity_digits': 3,
                'lines': [('create', [{
                        'date': date(2022, 5, 1),
                        'description': 'store some metal',
                        'category': category.id,
                        'bookingtype': 'in',
                        'amount': Decimal('1250.0'),
                        'party': party.id,
                        'quantity': Decimal('20.0'),
                        }],
                    )],
                }])

            self.assertEqual(
                book.rec_name,
                'Aurum-Storage | 1,250.00 CHF | Open | 20.000 g')
            self.assertEqual(book.balance_all, Decimal('1250.0'))
            self.assertEqual(len(book.lines), 1)

            self.assertEqual(book.lines[0].amount, Decimal('1250.0'))
            self.assertEqual(book.lines[0].quantity, Decimal('20.0'))
            self.assertEqual(book.lines[0].quantity_uom.symbol, 'g')

            self.assertEqual(book.symbol, 'CHF/g')
            self.assertEqual(
                book.asset.rec_name,
                'Aurum | 1,750.0000 usd/oz | 05/01/2022')

            # check quantities at cashbook
            with Transaction().set_context({
                    'date': date(2022, 5, 1)}):
                book2, = Book.browse([book])
                self.assertEqual(book.asset.rate, Decimal('1750.0'))   # usd
                self.assertEqual(book2.quantity, Decimal('20.0'))
                self.assertEqual(book2.quantity_all, Decimal('20.0'))
                # usd --> chf: 1750 US$ * 0.95 / 1.05 = 1583.333 €
                # 1 ounce --> 20 gram:
                #   1583.333 CHF * 20 / 28.3495 = 1117.0097 CHF
                self.assertEqual(
                    book2.current_value, Decimal('1117.01'))   # CHF
                self.assertEqual(
                    book2.current_value_ref, Decimal('1175.80'))   # EUR
                self.assertEqual(book2.diff_amount, Decimal('-132.99'))
                self.assertEqual(book2.diff_percent, Decimal('-10.64'))
                self.assertEqual(book2.current_rate, Decimal('55.85'))

    @with_transaction()
    def test_assetbook_book_uom(self):
        """ check default auf uom
        """
        pool = Pool()
        Book = pool.get('cashbook.book')
        BType = pool.get('cashbook.type')

        company = self.prep_company()
        with Transaction().set_context({'company': company.id}):
            types = self.prep_type()
            BType.write(*[
                [types],
                {
                    'feature': 'asset',
                    'name': 'Asset',
                    'short': 'A',
                }])

            asset = self.prep_asset_item(
                company=company,
                product=self.prep_asset_product(name='Product 1'))
            self.assertEqual(asset.symbol, 'usd/u')

            book = Book(asset=asset, quantity_uom=None)
            self.assertEqual(book.quantity_uom, None)
            book.on_change_asset()
            self.assertEqual(book.quantity_uom.rec_name, 'Unit')

    @with_transaction()
    def test_assetbook_quantity_digits(self):
        """ check selection of quantity-digits
        """
        pool = Pool()
        Book = pool.get('cashbook.book')
        BType = pool.get('cashbook.type')

        company = self.prep_company()
        with Transaction().set_context({'company': company.id}):
            category = self.prep_category(cattype='in')
            type_depot = self.prep_type('Depot', 'D')
            type_cash = self.prep_type('Cash', 'C')
            BType.write(*[
                [type_depot],
                {
                    'feature': 'asset',
                    'name': 'Asset',
                    'short': 'A',
                }])

            asset = self.prep_asset_item(
                company=company,
                product=self.prep_asset_product(name='Product 1'))
            self.assertEqual(asset.symbol, 'usd/u')

            books = Book.create([{
                'name': 'Book 1',
                'btype': type_depot.id,
                'company': company.id,
                'currency': company.currency.id,
                'number_sequ': self.prep_sequence().id,
                'asset': asset.id,
                'quantity_uom': asset.uom.id,
                'quantity_digits': 3,
                'start_date': date(2022, 5, 1),
                }, {
                'name': 'Book 2',
                'btype': type_cash.id,
                'company': company.id,
                'currency': company.currency.id,
                'number_sequ': self.prep_sequence().id,
                'start_date': date(2022, 5, 1),
                }])
            self.assertEqual(
                books[0].rec_name, 'Book 1 | 0.00 usd | Open | 0.000 u')
            self.assertEqual(
                books[1].rec_name, 'Book 2 | 0.00 usd | Open')

            Book.write(*[
                [books[0]],
                {
                    'lines': [('create', [{
                        'bookingtype': 'in',
                        'date': date(2022, 5, 1),
                        'category': category.id,
                        'amount': Decimal('1.0'),
                        'quantity': Decimal('1.0'),
                        }])],
                }])
            self.assertEqual(
                books[0].lines[0].rec_name,
                '05/01/2022|Rev|1.00 usd|- [Cat1]|1.000 u')
            self.assertEqual(books[0].lines[0].quantity_digits, 3)

            Book.write(*[
                [books[1]],
                {
                    'lines': [('create', [{
                        'bookingtype': 'in',
                        'date': date(2022, 5, 1),
                        'category': category.id,
                        'amount': Decimal('1.0'),
                        }])],
                }])
            self.assertEqual(
                books[1].lines[0].rec_name,
                '05/01/2022|Rev|1.00 usd|- [Cat1]')
            self.assertEqual(books[1].lines[0].quantity_digits, 0)

            Book.write(*[
                [books[1]],
                {
                    'lines': [('create', [{
                        'bookingtype': 'mvin',
                        'date': date(2022, 5, 1),
                        'amount': Decimal('1.0'),
                        'quantity': Decimal('1.0'),
                        'booktransf': books[0].id,
                        }])],
                }])
            self.assertEqual(
                books[1].lines[1].rec_name,
                '05/01/2022|from|1.00 usd|- [Book 1 | ' +
                '1.00 usd | Open | 1.000 u]')
            self.assertEqual(books[1].lines[1].quantity_digits, 3)

    @with_transaction()
    def test_assetbook_book_with_asset(self):
        """ create cashbook, set 'btype' to asset
        """
        pool = Pool()
        Book = pool.get('cashbook.book')
        BType = pool.get('cashbook.type')

        company = self.prep_company()
        with Transaction().set_context({'company': company.id}):
            types = self.prep_type()
            BType.write(*[
                [types],
                {
                    'feature': 'asset',
                    'name': 'Asset',
                    'short': 'A',
                }])

            asset = self.prep_asset_item(
                company=company,
                product=self.prep_asset_product(name='Product 1'))
            self.assertEqual(asset.symbol, 'usd/u')

            book, = Book.create([{
                'name': 'Book 1',
                'btype': types.id,
                'company': company.id,
                'currency': company.currency.id,
                'number_sequ': self.prep_sequence().id,
                'asset': asset.id,
                'quantity_uom': asset.uom.id,
                }])

            self.assertEqual(book.name, 'Book 1')
            self.assertEqual(
                book.rec_name, 'Book 1 | 0.00 usd | Open | 0.0000 u')
            self.assertEqual(book.btype.rec_name, 'A - Asset')
            self.assertEqual(book.state, 'open')
            self.assertEqual(book.feature, 'asset')
            self.assertEqual(book.asset.rec_name, 'Product 1 | - usd/u | -')
            self.assertEqual(book.quantity_uom.rec_name, 'Unit')

            self.assertRaisesRegex(
                UserError,
                'A value is required for field "Asset" in "Cashbook".',
                Book.write,
                *[
                    [book],
                    {
                        'asset': None,
                    }
                ])

    @with_transaction()
    def test_assetbook_check_sign_mismatch(self):
        """ create cashbook + line, bookingtype 'in',
            check detection of sign mismatch between quantity and amount
        """
        pool = Pool()
        Book = pool.get('cashbook.book')
        BType = pool.get('cashbook.type')

        company = self.prep_company()
        with Transaction().set_context({'company': company.id}):
            type_depot = self.prep_type('Depot', 'D')
            BType.write(*[
                [type_depot],
                {
                    'feature': 'asset',
                }])

            category_in = self.prep_category(cattype='in')
            self.prep_party()

            asset = self.prep_asset_item(
                company=company,
                product=self.prep_asset_product(name='Product 1'))
            self.assertEqual(asset.symbol, 'usd/u')

            book, = Book.create([{
                'name': 'Asset-Book',
                'btype': type_depot.id,
                'asset': asset.id,
                'quantity_uom': asset.uom.id,
                'company': company.id,
                'currency': company.currency.id,
                'number_sequ': self.prep_sequence().id,
                'start_date': date(2022, 5, 1),
                'lines': [('create', [{
                        'date': date(2022, 5, 1),
                        'description': 'buy some',
                        'category': category_in.id,
                        'bookingtype': 'in',
                        'amount': Decimal('1.0'),
                        'quantity': Decimal('1.5'),
                    }])],
                }])

            self.assertEqual(
                book.rec_name,
                'Asset-Book | 1.00 usd | Open | 1.5000 u')
            self.assertEqual(len(book.lines), 1)
            self.assertEqual(book.lines[0].amount, Decimal('1.0'))
            self.assertEqual(book.lines[0].credit, Decimal('1.0'))
            self.assertEqual(book.lines[0].debit, Decimal('0.0'))
            self.assertEqual(book.lines[0].quantity, Decimal('1.5'))
            self.assertEqual(book.lines[0].quantity_credit, Decimal('1.5'))
            self.assertEqual(book.lines[0].quantity_debit, Decimal('0.0'))

            self.assertRaisesRegex(
                UserError,
                "Quantity and Amount must with same sign for line " +
                "05/01/2022|Rev|1.00 usd|buy some [Cat1].",
                Book.write,
                *[
                    [book],
                    {
                        'lines': [('write', [book.lines[0]], {
                            'quantity': Decimal('-1.5'),
                        })],
                    }
                ])

    @with_transaction()
    def test_assetbook_check_mvout(self):
        """ create cashbook + line, bookingtype 'mvout'
            transfer from cash to depot (buy asset, pay from cash)
        """
        pool = Pool()
        Book = pool.get('cashbook.book')
        Line = pool.get('cashbook.line')
        BType = pool.get('cashbook.type')

        company = self.prep_company()
        with Transaction().set_context({'company': company.id}):
            type_cash = self.prep_type()
            type_depot = self.prep_type('Depot', 'D')
            BType.write(*[
                [type_depot],
                {
                    'feature': 'asset',
                }])

            self.prep_category(cattype='in')
            category_out = self.prep_category(
                name='Out Category', cattype='out')
            self.prep_party()

            asset = self.prep_asset_item(
                company=company,
                product=self.prep_asset_product(name='Product 1'))
            self.assertEqual(asset.symbol, 'usd/u')

            book2, = Book.create([{
                'name': 'Asset-Book',
                'btype': type_depot.id,
                'asset': asset.id,
                'quantity_uom': asset.uom.id,
                'company': company.id,
                'currency': company.currency.id,
                'number_sequ': self.prep_sequence().id,
                'start_date': date(2022, 5, 1),
                }])
            self.assertEqual(book2.show_performance, True)

            book, = Book.create([{
                'name': 'Book 1',
                'btype': type_cash.id,
                'company': company.id,
                'currency': company.currency.id,
                'number_sequ': self.prep_sequence().id,
                'start_date': date(2022, 5, 1),
                'lines': [('create', [{
                        'date': date(2022, 5, 1),
                        'description': 'Transfer Out',
                        'category': category_out.id,
                        'bookingtype': 'mvout',
                        'amount': Decimal('1.0'),
                        'booktransf': book2.id,
                        'quantity': Decimal('1.5'),
                    }])],
                }])
            self.assertEqual(book.show_performance, False)
            self.assertEqual(book.rec_name, 'Book 1 | -1.00 usd | Open')
            self.assertEqual(len(book.lines), 1)
            self.assertEqual(book.lines[0].quantity, Decimal('1.5'))
            self.assertEqual(book.lines[0].quantity_credit, None)
            self.assertEqual(book.lines[0].quantity_debit, None)
            self.assertEqual(book.lines[0].feature, 'gen')
            self.assertEqual(book.lines[0].booktransf_feature, 'asset')
            self.assertEqual(len(book2.lines), 0)
            self.assertEqual(
                book.lines[0].rec_name,
                '05/01/2022|to|-1.00 usd|Transfer Out [Asset-Book' +
                ' | 0.00 usd | Open | 0.0000 u]')
            self.assertEqual(len(book.lines[0].references), 0)

            # update quantity
            Book.write(*[
                [book],
                {
                    'lines': [
                        ('write',
                            [book.lines[0]], {'quantity': Decimal('2.5')})],
                }])
            self.assertEqual(book.lines[0].quantity, Decimal('2.5'))
            self.assertEqual(book.lines[0].quantity_credit, None)
            self.assertEqual(book.lines[0].quantity_debit, None)

            # check counterpart
            self.assertEqual(
                book.lines[0].booktransf.rec_name,
                'Asset-Book | 0.00 usd | Open | 0.0000 u')
            self.assertEqual(book.lines[0].booktransf.btype.feature, 'asset')
            self.assertEqual(book.lines[0].booktransf_feature, 'asset')

            # set line to 'checked', this creates the counterpart
            Line.wfcheck(list(book.lines))
            self.prep_valstore_run_worker()

            self.assertEqual(book.rec_name, 'Book 1 | -1.00 usd | Open')
            self.assertEqual(len(book.lines), 1)
            self.assertEqual(
                book.lines[0].rec_name,
                '05/01/2022|to|-1.00 usd|Transfer Out [Asset-Book | ' +
                '1.00 usd | Open | 2.5000 u]')
            self.assertEqual(book.lines[0].state, 'check')
            self.assertEqual(book.lines[0].bookingtype, 'mvout')
            self.assertEqual(book.lines[0].feature, 'gen')
            self.assertEqual(book.lines[0].amount, Decimal('1.0'))
            self.assertEqual(book.lines[0].credit, Decimal('0.0'))
            self.assertEqual(book.lines[0].debit, Decimal('1.0'))
            self.assertEqual(book.lines[0].quantity, Decimal('2.5'))
            self.assertEqual(
                book.lines[0].quantity_credit, None)   # feature != asset
            # --> no quantity-credit/debit
            self.assertEqual(
                book.lines[0].quantity_debit, None)
            self.assertEqual(book.lines[0].quantity_2nd_uom, None)
            self.assertEqual(book.lines[0].factor_2nd_uom, None)
            self.assertEqual(book.lines[0].quantity2nd, None)
            self.assertEqual(book.lines[0].quantity2nd_digits, 4)
            self.assertEqual(len(book.lines[0].references), 1)
            self.assertEqual(book.lines[0].reference, None)
            self.assertEqual(book.lines[0].references[0].id, book2.lines[0].id)

            self.assertEqual(
                book2.rec_name,
                'Asset-Book | 1.00 usd | Open | 2.5000 u')
            self.assertEqual(len(book2.lines), 1)
            self.assertEqual(
                book2.lines[0].rec_name,
                '05/01/2022|from|1.00 usd|Transfer Out [Book 1 | ' +
                '-1.00 usd | Open]|2.5000 u')
            self.assertEqual(book2.lines[0].state, 'check')
            self.assertEqual(book2.lines[0].bookingtype, 'mvin')
            self.assertEqual(book2.lines[0].feature, 'asset')
            self.assertEqual(book2.lines[0].amount, Decimal('1.0'))
            self.assertEqual(book2.lines[0].credit, Decimal('1.0'))
            self.assertEqual(book2.lines[0].debit, Decimal('0.0'))
            self.assertEqual(book2.lines[0].quantity, Decimal('2.5'))
            self.assertEqual(
                book2.lines[0].quantity_credit,
                Decimal('2.5'))    # feature=asset
            self.assertEqual(
                book2.lines[0].quantity_debit,
                Decimal('0.0'))     # needs quantity-credit/debit
            self.assertEqual(book2.lines[0].quantity_2nd_uom, None)
            self.assertEqual(book2.lines[0].factor_2nd_uom, None)
            self.assertEqual(book2.lines[0].quantity2nd, None)
            self.assertEqual(book2.lines[0].quantity2nd_digits, 4)
            self.assertEqual(book2.lines[0].asset_rate, Decimal('0.4'))
            self.assertEqual(
                book2.lines[0].reference.rec_name,
                '05/01/2022|to|-1.00 usd|Transfer Out [Asset-Book | ' +
                '1.00 usd | Open | 2.5000 u]')
            self.assertEqual(len(book2.lines[0].references), 0)

            l1 = list(book.lines)
            l1.append(Line(
                bookingtype='mvout',
                amount=Decimal('2.5'),
                quantity=Decimal('2.5'),
                booktransf=book2,
                ))
            book.lines = l1
            book.lines[-1].on_change_quantity()

    @with_transaction()
    def test_assetbook_check_mvout_zero_quantity(self):
        """ create cashbook + line, bookingtype 'mvout'
            transfer from asset-book to cash-book - zero quantity,
            to book gain/loss
        """
        pool = Pool()
        Book = pool.get('cashbook.book')
        Line = pool.get('cashbook.line')
        BType = pool.get('cashbook.type')

        company = self.prep_company()
        with Transaction().set_context({'company': company.id}):
            type_cash = self.prep_type()
            type_depot = self.prep_type('Depot', 'D')
            BType.write(*[
                [type_depot],
                {
                    'feature': 'asset',
                }])

            category_out = self.prep_category(
                name='Out Category', cattype='out')
            self.prep_party()

            asset = self.prep_asset_item(
                company=company,
                product=self.prep_asset_product(name='Product 1'))
            self.assertEqual(asset.symbol, 'usd/u')

            book1, = Book.create([{
                'name': 'Asset-Book',
                'btype': type_depot.id,
                'asset': asset.id,
                'quantity_uom': asset.uom.id,
                'company': company.id,
                'currency': company.currency.id,
                'number_sequ': self.prep_sequence().id,
                'start_date': date(2022, 5, 1),
                }])

            book2, = Book.create([{
                'name': 'Cash-Book',
                'btype': type_cash.id,
                'company': company.id,
                'currency': company.currency.id,
                'number_sequ': self.prep_sequence().id,
                'start_date': date(2022, 5, 1),
                }])

            Book.write(*[
                [book1],
                {
                    'lines': [('create', [{
                        'date': date(2022, 5, 1),
                        'description': 'loss at sell',
                        'category': category_out.id,
                        'bookingtype': 'mvout',
                        'amount': Decimal('10.0'),
                        'booktransf': book2.id,
                        'quantity': Decimal('0.0'),
                    }])],
                },
                ])
            self.assertEqual(
                book1.rec_name,
                'Asset-Book | -10.00 usd | Open | 0.0000 u')
            self.assertEqual(len(book1.lines), 1)
            self.assertEqual(
                book1.lines[0].rec_name,
                '05/01/2022|to|-10.00 usd|loss at sell [Cash-Book | ' +
                '0.00 usd | Open]|0.0000 u')
            self.assertEqual(book2.rec_name, 'Cash-Book | 0.00 usd | Open')
            self.assertEqual(len(book2.lines), 0)

            Line.wfcheck(list(book1.lines))
            self.prep_valstore_run_worker()

            self.assertEqual(
                book1.rec_name,
                'Asset-Book | -10.00 usd | Open | 0.0000 u')
            self.assertEqual(len(book1.lines), 1)
            self.assertEqual(
                book1.lines[0].rec_name,
                '05/01/2022|to|-10.00 usd|loss at sell [Cash-Book | ' +
                '10.00 usd | Open]|0.0000 u')
            self.assertEqual(book2.rec_name, 'Cash-Book | 10.00 usd | Open')
            self.assertEqual(len(book2.lines), 1)
            self.assertEqual(
                book2.lines[0].rec_name,
                '05/01/2022|from|10.00 usd|loss at sell [Asset-Book | ' +
                '-10.00 usd | Open | 0.0000 u]')

    @with_transaction()
    def test_assetbook_check_mvin(self):
        """ create cashbook + line, bookingtype 'mvin'
            transfer from depot to cash (sell asset, transfer to cash)
        """
        pool = Pool()
        Book = pool.get('cashbook.book')
        Line = pool.get('cashbook.line')
        BType = pool.get('cashbook.type')

        company = self.prep_company()
        with Transaction().set_context({'company': company.id}):
            type_cash = self.prep_type()
            type_depot = self.prep_type('Depot', 'D')
            BType.write(*[
                [type_depot],
                {
                    'feature': 'asset',
                }])

            self.prep_category(cattype='in')
            category_out = self.prep_category(
                name='Out Category', cattype='out')
            self.prep_party()

            asset = self.prep_asset_item(
                company=company,
                product=self.prep_asset_product(name='Product 1'))
            self.assertEqual(asset.symbol, 'usd/u')

            book2, = Book.create([{
                'name': 'Asset-Book',
                'btype': type_depot.id,
                'asset': asset.id,
                'quantity_uom': asset.uom.id,
                'company': company.id,
                'currency': company.currency.id,
                'number_sequ': self.prep_sequence().id,
                'start_date': date(2022, 5, 1),
                }])

            book, = Book.create([{
                'name': 'Book 1',
                'btype': type_cash.id,
                'company': company.id,
                'currency': company.currency.id,
                'number_sequ': self.prep_sequence().id,
                'start_date': date(2022, 5, 1),
                'lines': [('create', [{
                        'date': date(2022, 5, 1),
                        'description': 'Transfer In',
                        'category': category_out.id,
                        'bookingtype': 'mvin',
                        'amount': Decimal('1.0'),
                        'booktransf': book2.id,
                        'quantity': Decimal('1.5'),
                    }])],
                }])
            self.assertEqual(book.rec_name, 'Book 1 | 1.00 usd | Open')
            self.assertEqual(len(book.lines), 1)
            self.assertEqual(book.lines[0].quantity, Decimal('1.5'))
            self.assertEqual(book.lines[0].quantity_credit, None)
            self.assertEqual(book.lines[0].quantity_debit, None)
            self.assertEqual(book.lines[0].feature, 'gen')
            self.assertEqual(book.lines[0].booktransf_feature, 'asset')
            self.assertEqual(book.lines[0].splitline_has_quantity, False)
            self.assertEqual(len(book2.lines), 0)
            self.assertEqual(
                book.lines[0].rec_name,
                '05/01/2022|from|1.00 usd|Transfer In [Asset-Book | ' +
                '0.00 usd | Open | 0.0000 u]')
            self.assertEqual(len(book.lines[0].references), 0)

            # check counterpart
            self.assertEqual(
                book.lines[0].booktransf.rec_name,
                'Asset-Book | 0.00 usd | Open | 0.0000 u')
            self.assertEqual(book.lines[0].booktransf.btype.feature, 'asset')
            self.assertEqual(book.lines[0].booktransf_feature, 'asset')

            # set line to 'checked', this creates the counterpart
            Line.wfcheck(list(book.lines))
            self.prep_valstore_run_worker()

            self.assertEqual(book.rec_name, 'Book 1 | 1.00 usd | Open')
            self.assertEqual(len(book.lines), 1)
            self.assertEqual(
                book.lines[0].rec_name,
                '05/01/2022|from|1.00 usd|Transfer In [Asset-Book | ' +
                '-1.00 usd | Open | -1.5000 u]')
            self.assertEqual(book.lines[0].state, 'check')
            self.assertEqual(book.lines[0].bookingtype, 'mvin')
            self.assertEqual(book.lines[0].feature, 'gen')
            self.assertEqual(book.lines[0].amount, Decimal('1.0'))
            self.assertEqual(book.lines[0].credit, Decimal('1.0'))
            self.assertEqual(book.lines[0].debit, Decimal('0.0'))
            self.assertEqual(book.lines[0].quantity, Decimal('1.5'))
            self.assertEqual(
                book.lines[0].quantity_credit, None)   # feature != asset
            self.assertEqual(
                book.lines[0].quantity_debit,
                None)    # --> no quantity-credit/debit
            self.assertEqual(book.lines[0].quantity_2nd_uom, None)
            self.assertEqual(book.lines[0].factor_2nd_uom, None)
            self.assertEqual(book.lines[0].quantity2nd, None)
            self.assertEqual(book.lines[0].quantity2nd_digits, 4)
            self.assertEqual(len(book.lines[0].references), 1)
            self.assertEqual(book.lines[0].reference, None)
            self.assertEqual(book.lines[0].references[0].id, book2.lines[0].id)

            self.assertEqual(
                book2.rec_name,
                'Asset-Book | -1.00 usd | Open | -1.5000 u')
            self.assertEqual(len(book2.lines), 1)
            self.assertEqual(
                book2.lines[0].rec_name,
                '05/01/2022|to|-1.00 usd|Transfer In [Book 1 | ' +
                '1.00 usd | Open]|-1.5000 u')
            self.assertEqual(book2.lines[0].state, 'check')
            self.assertEqual(book2.lines[0].bookingtype, 'mvout')
            self.assertEqual(book2.lines[0].feature, 'asset')
            self.assertEqual(book2.lines[0].amount, Decimal('1.0'))
            self.assertEqual(book2.lines[0].credit, Decimal('0.0'))
            self.assertEqual(book2.lines[0].debit, Decimal('1.0'))
            self.assertEqual(book2.lines[0].quantity, Decimal('1.5'))
            self.assertEqual(
                book2.lines[0].quantity_credit,
                Decimal('0.0'))    # feature=asset
            self.assertEqual(
                book2.lines[0].quantity_debit,
                Decimal('1.5'))     # needs quantity-credit/debit
            self.assertEqual(book2.lines[0].quantity_2nd_uom, None)
            self.assertEqual(book2.lines[0].factor_2nd_uom, None)
            self.assertEqual(book2.lines[0].quantity2nd, None)
            self.assertEqual(book2.lines[0].quantity2nd_digits, 4)
            self.assertEqual(book2.lines[0].asset_rate, Decimal('0.6667'))
            self.assertEqual(
                book2.lines[0].reference.rec_name,
                '05/01/2022|from|1.00 usd|Transfer In [Asset-Book | ' +
                '-1.00 usd | Open | -1.5000 u]')
            self.assertEqual(len(book2.lines[0].references), 0)

    @with_transaction()
    def test_assetbook_check_mvin_two_assetbooks(self):
        """ create cashbook + line, bookingtype 'mvin'
            transfer from depot to depot, equal uom on both cashbooks
        """
        pool = Pool()
        Book = pool.get('cashbook.book')
        Line = pool.get('cashbook.line')
        BType = pool.get('cashbook.type')

        company = self.prep_company()
        with Transaction().set_context({'company': company.id}):
            self.prep_type()
            type_depot = self.prep_type('Depot', 'D')
            BType.write(*[
                [type_depot],
                {
                    'feature': 'asset',
                }])

            self.prep_category(cattype='in')
            category_out = self.prep_category(
                name='Out Category', cattype='out')
            self.prep_party()

            asset = self.prep_asset_item(
                company=company,
                product=self.prep_asset_product(name='Product 1'))
            self.assertEqual(asset.symbol, 'usd/u')

            book2, = Book.create([{
                'name': 'Asset-Book 1',
                'btype': type_depot.id,
                'asset': asset.id,
                'quantity_uom': asset.uom.id,
                'company': company.id,
                'currency': company.currency.id,
                'number_sequ': self.prep_sequence().id,
                'start_date': date(2022, 5, 1),
                }])

            book, = Book.create([{
                'name': 'Asset-Book 2',
                'btype': type_depot.id,
                'asset': asset.id,
                'quantity_uom': asset.uom.id,
                'company': company.id,
                'currency': company.currency.id,
                'number_sequ': self.prep_sequence().id,
                'start_date': date(2022, 5, 1),
                'lines': [('create', [{
                        'date': date(2022, 5, 1),
                        'description': 'Transfer In',
                        'category': category_out.id,
                        'bookingtype': 'mvin',
                        'amount': Decimal('1.0'),
                        'booktransf': book2.id,
                        'quantity': Decimal('1.5'),
                    }])],
                }])
            self.assertEqual(
                book.rec_name,
                'Asset-Book 2 | 1.00 usd | Open | 1.5000 u')
            self.assertEqual(len(book.lines), 1)
            self.assertEqual(book.lines[0].amount, Decimal('1.0'))
            self.assertEqual(book.lines[0].credit, Decimal('1.0'))
            self.assertEqual(book.lines[0].debit, Decimal('0.0'))
            self.assertEqual(book.lines[0].quantity, Decimal('1.5'))
            self.assertEqual(book.lines[0].quantity_credit, Decimal('1.5'))
            self.assertEqual(book.lines[0].quantity_debit, Decimal('0.0'))
            self.assertEqual(book.lines[0].feature, 'asset')
            self.assertEqual(book.lines[0].booktransf_feature, 'asset')
            self.assertEqual(len(book2.lines), 0)
            self.assertEqual(
                book.lines[0].rec_name,
                '05/01/2022|from|1.00 usd|Transfer In [Asset-Book 1 | ' +
                '0.00 usd | Open | 0.0000 u]|1.5000 u')
            self.assertEqual(len(book.lines[0].references), 0)

            # check counterpart
            self.assertEqual(
                book.lines[0].booktransf.rec_name,
                'Asset-Book 1 | 0.00 usd | Open | 0.0000 u')
            self.assertEqual(book.lines[0].booktransf.btype.feature, 'asset')
            self.assertEqual(book.lines[0].booktransf_feature, 'asset')

            # set line to 'checked', this creates the counterpart
            Line.wfcheck(list(book.lines))
            self.prep_valstore_run_worker()

            self.assertEqual(
                book.rec_name,
                'Asset-Book 2 | 1.00 usd | Open | 1.5000 u')
            self.assertEqual(len(book.lines), 1)
            self.assertEqual(
                book.lines[0].rec_name,
                '05/01/2022|from|1.00 usd|Transfer In [Asset-Book 1 | ' +
                '-1.00 usd | Open | -1.5000 u]|1.5000 u')
            self.assertEqual(book.lines[0].state, 'check')
            self.assertEqual(book.lines[0].bookingtype, 'mvin')
            self.assertEqual(book.lines[0].feature, 'asset')
            self.assertEqual(book.lines[0].amount, Decimal('1.0'))
            self.assertEqual(book.lines[0].credit, Decimal('1.0'))
            self.assertEqual(book.lines[0].debit, Decimal('0.0'))
            self.assertEqual(book.lines[0].quantity, Decimal('1.5'))
            self.assertEqual(book.lines[0].quantity_credit, Decimal('1.5'))
            self.assertEqual(book.lines[0].quantity_debit, Decimal('0.0'))
            self.assertEqual(book.lines[0].quantity_2nd_uom, None)
            self.assertEqual(book.lines[0].factor_2nd_uom, None)
            self.assertEqual(book.lines[0].quantity2nd, None)
            self.assertEqual(book.lines[0].quantity2nd_digits, 4)
            self.assertEqual(len(book.lines[0].references), 1)
            self.assertEqual(book.lines[0].reference, None)
            self.assertEqual(book.lines[0].references[0].id, book2.lines[0].id)

            self.assertEqual(
                book2.rec_name,
                'Asset-Book 1 | -1.00 usd | Open | -1.5000 u')
            self.assertEqual(len(book2.lines), 1)
            self.assertEqual(
                book2.lines[0].rec_name,
                '05/01/2022|to|-1.00 usd|Transfer In [Asset-Book 2 | ' +
                '1.00 usd | Open | 1.5000 u]|-1.5000 u')
            self.assertEqual(book2.lines[0].state, 'check')
            self.assertEqual(book2.lines[0].bookingtype, 'mvout')
            self.assertEqual(book2.lines[0].feature, 'asset')
            self.assertEqual(book2.lines[0].amount, Decimal('1.0'))
            self.assertEqual(book2.lines[0].credit, Decimal('0.0'))
            self.assertEqual(book2.lines[0].debit, Decimal('1.0'))
            self.assertEqual(book2.lines[0].quantity, Decimal('1.5'))
            self.assertEqual(book2.lines[0].quantity_credit, Decimal('0.0'))
            self.assertEqual(book2.lines[0].quantity_debit, Decimal('1.5'))
            self.assertEqual(book2.lines[0].quantity_2nd_uom, None)
            self.assertEqual(book2.lines[0].factor_2nd_uom, None)
            self.assertEqual(book2.lines[0].quantity2nd, None)
            self.assertEqual(book2.lines[0].quantity2nd_digits, 4)
            self.assertEqual(book2.lines[0].asset_rate, Decimal('0.6667'))
            self.assertEqual(
                book2.lines[0].reference.rec_name,
                '05/01/2022|from|1.00 usd|Transfer In [Asset-Book 1 | ' +
                '-1.00 usd | Open | -1.5000 u]|1.5000 u')
            self.assertEqual(len(book2.lines[0].references), 0)

    @with_transaction()
    def test_assetbook_check_mvin_two_assetbooks_diff_uom_equal_uomcat(self):
        """ create cashbook + line, bookingtype 'mvin'
            transfer from depot to depot,
            different uom (equal uom-category) on both cashbooks
        """
        pool = Pool()
        Book = pool.get('cashbook.book')
        Line = pool.get('cashbook.line')
        BType = pool.get('cashbook.type')
        UOM = pool.get('product.uom')
        ProdTempl = pool.get('product.template')
        Asset = pool.get('investment.asset')

        company = self.prep_company()
        with Transaction().set_context({'company': company.id}):
            self.prep_type()
            type_depot = self.prep_type('Depot', 'D')
            BType.write(*[
                [type_depot],
                {
                    'feature': 'asset',
                }])

            self.prep_category(cattype='in')
            category_out = self.prep_category(
                name='Out Category', cattype='out')
            self.prep_party()

            asset1 = self.prep_asset_item(
                company=company,
                product=self.prep_asset_product(name='Product 1'))
            asset2 = self.prep_asset_item(
                company=company,
                product=self.prep_asset_product(name='Product 2'))

            uom_grams = UOM.search([('symbol', '=', 'g')])[0]
            uom_ounce = UOM.search([('symbol', '=', 'oz')])[0]
            ProdTempl.write(*[
                [asset1.product.template],
                {
                    'default_uom': uom_grams.id,
                },
                [asset2.product.template],
                {
                    'default_uom': uom_ounce.id,
                },
                ])

            Asset.write(*[
                [asset1],
                {
                    'uom': uom_grams.id,
                },
                [asset2],
                {
                    'uom': uom_ounce.id,
                },
                ])
            self.assertEqual(asset1.symbol, 'usd/g')
            self.assertEqual(asset2.symbol, 'usd/oz')

            book2, = Book.create([{
                'name': 'Asset-Book 1',
                'btype': type_depot.id,
                'asset': asset1.id,
                'quantity_uom': asset1.uom.id,
                'company': company.id,
                'currency': company.currency.id,
                'number_sequ': self.prep_sequence().id,
                'start_date': date(2022, 5, 1),
                }])

            book, = Book.create([{
                'name': 'Asset-Book 2',
                'btype': type_depot.id,
                'asset': asset2.id,
                'quantity_uom': asset2.uom.id,
                'company': company.id,
                'currency': company.currency.id,
                'number_sequ': self.prep_sequence().id,
                'start_date': date(2022, 5, 1),
                'lines': [('create', [{
                        'date': date(2022, 5, 1),
                        'description': 'Transfer In',
                        'category': category_out.id,
                        'bookingtype': 'mvin',
                        'amount': Decimal('1.0'),
                        'booktransf': book2.id,
                        'quantity': Decimal('1.5'),
                    }])],
                }])
            self.assertEqual(
                book.rec_name,
                'Asset-Book 2 | 1.00 usd | Open | 1.5000 oz')
            self.assertEqual(len(book.lines), 1)
            self.assertEqual(book.lines[0].amount, Decimal('1.0'))
            self.assertEqual(book.lines[0].credit, Decimal('1.0'))
            self.assertEqual(book.lines[0].debit, Decimal('0.0'))
            self.assertEqual(book.lines[0].quantity, Decimal('1.5'))
            self.assertEqual(book.lines[0].quantity_credit, Decimal('1.5'))
            self.assertEqual(book.lines[0].quantity_debit, Decimal('0.0'))
            self.assertEqual(book.lines[0].quantity_uom.symbol, 'oz')
            self.assertEqual(book.lines[0].quantity_uom.factor, 0.028349523125)
            self.assertEqual(book.lines[0].quantity2nd.symbol, 'g')
            self.assertEqual(book.lines[0].quantity2nd.factor, 0.001)
            self.assertEqual(
                book.lines[0].quantity_2nd_uom,
                Decimal('42.5243'))    # 1.5 oz --> g
            self.assertEqual(
                book.lines[0].factor_2nd_uom,
                Decimal('28.349533333333'))
            self.assertEqual(book.lines[0].quantity2nd_digits, 4)
            self.assertEqual(book.lines[0].feature, 'asset')
            self.assertEqual(len(book2.lines), 0)
            self.assertEqual(
                book.lines[0].rec_name,
                '05/01/2022|from|1.00 usd|Transfer In [Asset-Book 1 | ' +
                '0.00 usd | Open | 0.0000 g]|1.5000 oz')
            self.assertEqual(len(book.lines[0].references), 0)

            # check counterpart
            self.assertEqual(
                book.lines[0].booktransf.rec_name,
                'Asset-Book 1 | 0.00 usd | Open | 0.0000 g')
            self.assertEqual(book.lines[0].booktransf.btype.feature, 'asset')
            self.assertEqual(book.lines[0].booktransf_feature, 'asset')

            # set line to 'checked', this creates the counterpart
            Line.wfcheck(list(book.lines))
            self.prep_valstore_run_worker()

            self.assertEqual(
                book.rec_name,
                'Asset-Book 2 | 1.00 usd | Open | 1.5000 oz')
            self.assertEqual(len(book.lines), 1)
            self.assertEqual(
                book.lines[0].rec_name,
                '05/01/2022|from|1.00 usd|Transfer In [Asset-Book 1 | ' +
                '-1.00 usd | Open | -42.5243 g]|1.5000 oz')
            self.assertEqual(book.lines[0].state, 'check')
            self.assertEqual(book.lines[0].bookingtype, 'mvin')
            self.assertEqual(book.lines[0].feature, 'asset')
            self.assertEqual(book.lines[0].amount, Decimal('1.0'))
            self.assertEqual(book.lines[0].credit, Decimal('1.0'))
            self.assertEqual(book.lines[0].debit, Decimal('0.0'))
            self.assertEqual(book.lines[0].quantity, Decimal('1.5'))
            self.assertEqual(book.lines[0].quantity_credit, Decimal('1.5'))
            self.assertEqual(book.lines[0].quantity_debit, Decimal('0.0'))
            self.assertEqual(book.lines[0].quantity_2nd_uom, Decimal('42.5243'))
            self.assertEqual(
                book.lines[0].factor_2nd_uom,
                Decimal('28.349533333333'))
            self.assertEqual(book.lines[0].quantity2nd.symbol, 'g')
            self.assertEqual(book.lines[0].quantity2nd.factor, 0.001)
            self.assertEqual(book.lines[0].quantity2nd_digits, 4)
            self.assertEqual(len(book.lines[0].references), 1)
            self.assertEqual(book.lines[0].reference, None)
            self.assertEqual(book.lines[0].references[0].id, book2.lines[0].id)

            self.assertEqual(
                book2.rec_name,
                'Asset-Book 1 | -1.00 usd | Open | -42.5243 g')
            self.assertEqual(len(book2.lines), 1)
            self.assertEqual(
                book2.lines[0].rec_name,
                '05/01/2022|to|-1.00 usd|Transfer In [Asset-Book 2 | ' +
                '1.00 usd | Open | 1.5000 oz]|-42.5243 g')
            self.assertEqual(book2.lines[0].state, 'check')
            self.assertEqual(book2.lines[0].bookingtype, 'mvout')
            self.assertEqual(book2.lines[0].feature, 'asset')
            self.assertEqual(book2.lines[0].amount, Decimal('1.0'))
            self.assertEqual(book2.lines[0].credit, Decimal('0.0'))
            self.assertEqual(book2.lines[0].debit, Decimal('1.0'))
            self.assertEqual(book2.lines[0].quantity, Decimal('42.5243'))
            self.assertEqual(book2.lines[0].quantity_credit, Decimal('0.0'))
            self.assertEqual(book2.lines[0].quantity_debit, Decimal('42.5243'))
            self.assertEqual(book2.lines[0].quantity_2nd_uom, Decimal('1.5'))
            self.assertEqual(
                book2.lines[0].factor_2nd_uom,
                Decimal('0.035273949248'))
            self.assertEqual(book2.lines[0].quantity2nd.symbol, 'oz')
            self.assertEqual(book2.lines[0].quantity2nd.factor, 0.028349523125)
            self.assertEqual(book2.lines[0].quantity2nd_digits, 4)
            self.assertEqual(book2.lines[0].asset_rate, Decimal('0.0235'))
            self.assertEqual(
                book2.lines[0].reference.rec_name,
                '05/01/2022|from|1.00 usd|Transfer In [Asset-Book 1 | ' +
                '-1.00 usd | Open | -42.5243 g]|1.5000 oz')
            self.assertEqual(len(book2.lines[0].references), 0)

    @with_transaction()
    def test_assetbook_check_mvin_two_assetbooks_diff_uom_diff_uomcat(self):
        """ create cashbook + line, bookingtype 'mvin'
            transfer from depot to depot,
            different uom (different uom-category) on both cashbooks
        """
        pool = Pool()
        Book = pool.get('cashbook.book')
        BType = pool.get('cashbook.type')
        UOM = pool.get('product.uom')
        ProdTempl = pool.get('product.template')
        Asset = pool.get('investment.asset')

        company = self.prep_company()
        with Transaction().set_context({'company': company.id}):
            self.prep_type()
            type_depot = self.prep_type('Depot', 'D')
            BType.write(*[
                [type_depot],
                {
                    'feature': 'asset',
                }])

            self.prep_category(cattype='in')
            category_out = self.prep_category(
                name='Out Category', cattype='out')
            self.prep_party()

            asset1 = self.prep_asset_item(
                company=company,
                product=self.prep_asset_product(name='Product 1'))
            asset2 = self.prep_asset_item(
                company=company,
                product=self.prep_asset_product(name='Product 2'))

            uom_grams = UOM.search([('symbol', '=', 'g')])[0]
            uom_min = UOM.search([('symbol', '=', 'min')])[0]
            ProdTempl.write(*[
                [asset1.product.template],
                {
                    'default_uom': uom_grams.id,
                },
                [asset2.product.template],
                {
                    'default_uom': uom_min.id,
                },
                ])

            Asset.write(*[
                [asset1],
                {
                    'uom': uom_grams.id,
                },
                [asset2],
                {
                    'uom': uom_min.id,
                },
                ])
            self.assertEqual(asset1.symbol, 'usd/g')
            self.assertEqual(asset2.symbol, 'usd/min')

            book2, = Book.create([{
                'name': 'Asset-Book 1',
                'btype': type_depot.id,
                'asset': asset1.id,
                'quantity_uom': asset1.uom.id,
                'company': company.id,
                'currency': company.currency.id,
                'number_sequ': self.prep_sequence().id,
                'start_date': date(2022, 5, 1),
                }])

            book, = Book.create([{
                'name': 'Asset-Book 2',
                'btype': type_depot.id,
                'asset': asset2.id,
                'quantity_uom': asset2.uom.id,
                'company': company.id,
                'currency': company.currency.id,
                'number_sequ': self.prep_sequence().id,
                'start_date': date(2022, 5, 1),
                }])

            self.assertRaisesRegex(
                UserError,
                r'Cannot transfer quantities between cashbooks with ' +
                r'different unit-categories \(Time != Weight\).',
                Book.write,
                *[
                    [book],
                    {
                        'lines': [('create', [{
                                'date': date(2022, 5, 1),
                                'description': 'Transfer In',
                                'category': category_out.id,
                                'bookingtype': 'mvin',
                                'amount': Decimal('1.0'),
                                'booktransf': book2.id,
                                'quantity': Decimal('1.5'),
                            }])],
                    },
                ])

    @with_transaction()
    def test_assetbook_split_in_category(self):
        """ splitbooking incoming with asset
        """
        pool = Pool()
        Book = pool.get('cashbook.book')
        BType = pool.get('cashbook.type')

        company = self.prep_company()
        with Transaction().set_context({'company': company.id}):
            types = self.prep_type()
            BType.write(*[
                [types],
                {
                    'feature': 'asset',
                }])
            category = self.prep_category(cattype='in')

            self.prep_party()
            asset = self.prep_asset_item(
                company=company,
                product=self.prep_asset_product(name='Product 1'))
            self.assertEqual(asset.symbol, 'usd/u')

            book, = Book.create([{
                'start_date': date(2022, 4, 1),
                'name': 'Book 1',
                'btype': types.id,
                'company': company.id,
                'currency': company.currency.id,
                'number_sequ': self.prep_sequence().id,
                'asset': asset.id,
                'quantity_uom': asset.uom.id,
                'quantity_digits': 2,
                }])

            Book.write(*[
                [book],
                {
                    'lines': [('create', [{
                        'bookingtype': 'spin',
                        'date': date(2022, 5, 1),
                        'splitlines': [('create', [{
                            'amount': Decimal('5.0'),
                            'splittype': 'cat',
                            'description': 'from category',
                            'category': category.id,
                            'quantity': Decimal('1.5'),
                            }, {
                            'amount': Decimal('6.0'),
                            'splittype': 'cat',
                            'description': 'from category',
                            'category': category.id,
                            'quantity': Decimal('2.5'),
                            }])],
                        }])],
                }])

            self.assertEqual(
                book.rec_name, 'Book 1 | 11.00 usd | Open | 4.00 u')
            self.assertEqual(book.balance_all, Decimal('11.0'))
            self.assertEqual(len(book.lines), 1)

            self.assertEqual(book.lines[0].amount, Decimal('11.0'))
            self.assertEqual(book.lines[0].quantity, Decimal('4.0'))
            self.assertEqual(book.lines[0].quantity_uom.symbol, 'u')
            self.assertEqual(book.lines[0].splitline_has_quantity, False)
            self.assertEqual(
                book.lines[0].rec_name,
                '05/01/2022|Rev/Sp|11.00 usd|- [-]|4.00 u')

            self.assertEqual(len(book.lines[0].splitlines), 2)
            self.assertEqual(book.lines[0].splitlines[0].splittype, 'cat')
            self.assertEqual(book.lines[0].splitlines[0].amount, Decimal('5.0'))
            self.assertEqual(
                book.lines[0].splitlines[0].quantity, Decimal('1.5'))
            self.assertEqual(book.lines[0].splitlines[1].splittype, 'cat')
            self.assertEqual(book.lines[0].splitlines[1].amount, Decimal('6.0'))
            self.assertEqual(
                book.lines[0].splitlines[1].quantity, Decimal('2.5'))

    @with_transaction()
    def test_assetbook_split_in_category_and_assetbook(self):
        """ splitbooking incoming to asset-cahbook,
            from category and asset-cashbook
        """
        pool = Pool()
        Book = pool.get('cashbook.book')
        Line = pool.get('cashbook.line')
        BType = pool.get('cashbook.type')

        company = self.prep_company()
        with Transaction().set_context({'company': company.id}):
            types = self.prep_type()
            BType.write(*[
                [types],
                {
                    'feature': 'asset',
                }])
            category = self.prep_category(cattype='in')

            self.prep_party()
            asset = self.prep_asset_item(
                company=company,
                product=self.prep_asset_product(name='Product 1'))
            self.assertEqual(asset.symbol, 'usd/u')

            books = Book.create([{
                'start_date': date(2022, 4, 1),
                'name': 'Book 1',
                'btype': types.id,
                'company': company.id,
                'currency': company.currency.id,
                'number_sequ': self.prep_sequence().id,
                'asset': asset.id,
                'quantity_uom': asset.uom.id,
                'quantity_digits': 2,
                }, {
                'start_date': date(2022, 4, 1),
                'name': 'Book 2',
                'btype': types.id,
                'company': company.id,
                'currency': company.currency.id,
                'number_sequ': self.prep_sequence().id,
                'asset': asset.id,
                'quantity_uom': asset.uom.id,
                'quantity_digits': 2,
                }])

            Book.write(*[
                [books[0]],
                {
                    'lines': [('create', [{
                        'bookingtype': 'spin',
                        'date': date(2022, 5, 1),
                        'splitlines': [('create', [{
                            'amount': Decimal('5.0'),
                            'splittype': 'cat',
                            'description': 'from category',
                            'category': category.id,
                            'quantity': Decimal('1.5'),
                            }, {
                            'amount': Decimal('6.0'),
                            'splittype': 'tr',
                            'description': 'from cashbook',
                            'booktransf': books[1].id,
                            'quantity': Decimal('2.5'),
                            }])],
                        }])],
                }])

            self.assertEqual(
                books[0].rec_name,
                'Book 1 | 11.00 usd | Open | 4.00 u')
            self.assertEqual(books[0].balance_all, Decimal('11.0'))
            self.assertEqual(len(books[0].lines), 1)

            self.assertEqual(books[0].lines[0].amount, Decimal('11.0'))
            self.assertEqual(books[0].lines[0].quantity, Decimal('4.0'))
            self.assertEqual(books[0].lines[0].quantity_uom.symbol, 'u')
            self.assertEqual(books[0].lines[0].splitline_has_quantity, True)
            self.assertEqual(
                books[0].lines[0].rec_name,
                '05/01/2022|Rev/Sp|11.00 usd|- [-]|4.00 u')

            self.assertEqual(len(books[0].lines[0].splitlines), 2)
            self.assertEqual(books[0].lines[0].splitlines[0].splittype, 'cat')
            self.assertEqual(
                books[0].lines[0].splitlines[0].amount, Decimal('5.0'))
            self.assertEqual(
                books[0].lines[0].splitlines[0].quantity,
                Decimal('1.5'))
            self.assertEqual(
                books[0].lines[0].splitlines[0].category.rec_name,
                'Cat1')
            self.assertEqual(books[0].lines[0].splitlines[0].booktransf, None)
            self.assertEqual(books[0].lines[0].splitlines[1].splittype, 'tr')
            self.assertEqual(
                books[0].lines[0].splitlines[1].amount, Decimal('6.0'))
            self.assertEqual(
                books[0].lines[0].splitlines[1].quantity,
                Decimal('2.5'))
            self.assertEqual(
                books[0].lines[0].splitlines[1].booktransf.rec_name,
                'Book 2 | 0.00 usd | Open | 0.00 u')
            self.assertEqual(len(books[0].lines[0].references), 0)
            self.assertEqual(books[0].lines[0].reference, None)

            self.assertEqual(
                books[1].rec_name, 'Book 2 | 0.00 usd | Open | 0.00 u')
            self.assertEqual(books[1].balance_all, Decimal('0.0'))
            self.assertEqual(len(books[1].lines), 0)

            Line.wfcheck([books[0].lines[0]])
            self.prep_valstore_run_worker()

            self.assertEqual(
                books[0].rec_name,
                'Book 1 | 11.00 usd | Open | 4.00 u')
            self.assertEqual(books[0].balance_all, Decimal('11.0'))
            self.assertEqual(len(books[0].lines), 1)

            self.assertEqual(books[0].lines[0].amount, Decimal('11.0'))
            self.assertEqual(books[0].lines[0].quantity, Decimal('4.0'))
            self.assertEqual(books[0].lines[0].quantity_uom.symbol, 'u')
            self.assertEqual(books[0].lines[0].splitline_has_quantity, True)
            self.assertEqual(
                books[0].lines[0].rec_name,
                '05/01/2022|Rev/Sp|11.00 usd|- [-]|4.00 u')

            self.assertEqual(len(books[0].lines[0].splitlines), 2)
            self.assertEqual(books[0].lines[0].splitlines[0].splittype, 'cat')
            self.assertEqual(
                books[0].lines[0].splitlines[0].amount, Decimal('5.0'))
            self.assertEqual(
                books[0].lines[0].splitlines[0].quantity,
                Decimal('1.5'))
            self.assertEqual(
                books[0].lines[0].splitlines[0].category.rec_name,
                'Cat1')
            self.assertEqual(books[0].lines[0].splitlines[0].booktransf, None)
            self.assertEqual(books[0].lines[0].splitlines[1].splittype, 'tr')
            self.assertEqual(
                books[0].lines[0].splitlines[1].amount, Decimal('6.0'))
            self.assertEqual(
                books[0].lines[0].splitlines[1].quantity,
                Decimal('2.5'))
            self.assertEqual(
                books[0].lines[0].splitlines[1].booktransf.rec_name,
                'Book 2 | -6.00 usd | Open | -2.50 u')
            self.assertEqual(len(books[0].lines[0].references), 1)
            self.assertEqual(
                books[0].lines[0].references[0].rec_name,
                '05/01/2022|to|-6.00 usd|from cashbook [Book 1 | 11.00 usd' +
                ' | Open | 4.00 u]|-2.50 u')
            self.assertEqual(books[0].lines[0].reference, None)

            self.assertEqual(
                books[1].rec_name,
                'Book 2 | -6.00 usd | Open | -2.50 u')
            self.assertEqual(books[1].balance_all, Decimal('-6.0'))
            self.assertEqual(len(books[1].lines), 1)
            self.assertEqual(
                books[1].lines[0].rec_name,
                '05/01/2022|to|-6.00 usd|from cashbook [Book 1 | 11.00 usd' +
                ' | Open | 4.00 u]|-2.50 u')

    @with_transaction()
    def test_assetbook_split_in_category_and_assetbook_zero_quantity(self):
        """ splitbooking incoming to asset-cahbook,
            from category and asset-cashbook, zero qunatity to book
            gain/loss of a sell from asset-cashbook
        """
        pool = Pool()
        Book = pool.get('cashbook.book')
        Line = pool.get('cashbook.line')
        BType = pool.get('cashbook.type')

        company = self.prep_company()
        with Transaction().set_context({'company': company.id}):
            types = self.prep_type()
            BType.write(*[
                [types],
                {
                    'feature': 'asset',
                }])
            category = self.prep_category(cattype='in')

            self.prep_party()
            asset = self.prep_asset_item(
                company=company,
                product=self.prep_asset_product(name='Product 1'))
            self.assertEqual(asset.symbol, 'usd/u')

            books = Book.create([{
                'start_date': date(2022, 4, 1),
                'name': 'Book 1',
                'btype': types.id,
                'company': company.id,
                'currency': company.currency.id,
                'number_sequ': self.prep_sequence().id,
                'asset': asset.id,
                'quantity_uom': asset.uom.id,
                'quantity_digits': 2,
                }, {
                'start_date': date(2022, 4, 1),
                'name': 'Book 2',
                'btype': types.id,
                'company': company.id,
                'currency': company.currency.id,
                'number_sequ': self.prep_sequence().id,
                'asset': asset.id,
                'quantity_uom': asset.uom.id,
                'quantity_digits': 2,
                }])

            Book.write(*[
                [books[0]],
                {
                    'lines': [('create', [{
                        'bookingtype': 'spin',
                        'date': date(2022, 5, 1),
                        'splitlines': [('create', [{
                            'amount': Decimal('5.0'),
                            'splittype': 'cat',
                            'description': 'gain on sell',
                            'category': category.id,
                            'quantity': Decimal('0.0'),
                            }, {
                            'amount': Decimal('6.0'),
                            'splittype': 'tr',
                            'description': 'transfer zero quantity',
                            'booktransf': books[1].id,
                            'quantity': Decimal('0.0'),
                            }])],
                        }])],
                }])

            self.assertEqual(
                books[0].rec_name,
                'Book 1 | 11.00 usd | Open | 0.00 u')
            self.assertEqual(books[0].balance_all, Decimal('11.0'))
            self.assertEqual(len(books[0].lines), 1)

            self.assertEqual(
                books[0].lines[0].rec_name,
                '05/01/2022|Rev/Sp|11.00 usd|- [-]|0.00 u')
            self.assertEqual(books[0].lines[0].splitline_has_quantity, True)

            self.assertEqual(len(books[0].lines[0].splitlines), 2)
            self.assertEqual(
                books[0].lines[0].splitlines[0].rec_name,
                'Rev/Sp|5.00 usd|gain on sell [Cat1]|0.00 u')
            self.assertEqual(books[0].lines[0].splitlines[0].booktransf, None)
            self.assertEqual(
                books[0].lines[0].splitlines[1].rec_name,
                'Rev/Sp|6.00 usd|transfer zero quantity [Book 2 | 0.00 usd' +
                ' | Open | 0.00 u]|0.00 u')
            self.assertEqual(
                books[0].lines[0].splitlines[1].booktransf.rec_name,
                'Book 2 | 0.00 usd | Open | 0.00 u')
            self.assertEqual(len(books[0].lines[0].references), 0)
            self.assertEqual(books[0].lines[0].reference, None)

            self.assertEqual(
                books[1].rec_name, 'Book 2 | 0.00 usd | Open | 0.00 u')
            self.assertEqual(books[1].balance_all, Decimal('0.0'))
            self.assertEqual(len(books[1].lines), 0)

            Line.wfcheck([books[0].lines[0]])
            self.prep_valstore_run_worker()

            self.assertEqual(
                books[0].rec_name,
                'Book 1 | 11.00 usd | Open | 0.00 u')
            self.assertEqual(books[0].balance_all, Decimal('11.0'))
            self.assertEqual(len(books[0].lines), 1)

            self.assertEqual(
                books[0].lines[0].rec_name,
                '05/01/2022|Rev/Sp|11.00 usd|- [-]|0.00 u')
            self.assertEqual(books[0].lines[0].splitline_has_quantity, True)

            self.assertEqual(len(books[0].lines[0].splitlines), 2)
            self.assertEqual(
                books[0].lines[0].splitlines[0].rec_name,
                'Rev/Sp|5.00 usd|gain on sell [Cat1]|0.00 u')
            self.assertEqual(books[0].lines[0].splitlines[0].booktransf, None)
            self.assertEqual(
                books[0].lines[0].splitlines[1].rec_name,
                'Rev/Sp|6.00 usd|transfer zero quantity [Book 2 | -6.00 usd' +
                ' | Open | 0.00 u]|0.00 u')
            self.assertEqual(
                books[0].lines[0].splitlines[1].booktransf.rec_name,
                'Book 2 | -6.00 usd | Open | 0.00 u')
            self.assertEqual(len(books[0].lines[0].references), 1)
            self.assertEqual(
                books[0].lines[0].references[0].rec_name,
                '05/01/2022|to|-6.00 usd|transfer zero quantity [Book 1 | ' +
                '11.00 usd | Open | 0.00 u]|0.00 u')
            self.assertEqual(books[0].lines[0].reference, None)

            self.assertEqual(
                books[1].rec_name,
                'Book 2 | -6.00 usd | Open | 0.00 u')
            self.assertEqual(books[1].balance_all, Decimal('-6.0'))
            self.assertEqual(len(books[1].lines), 1)
            self.assertEqual(
                books[1].lines[0].rec_name,
                '05/01/2022|to|-6.00 usd|transfer zero quantity [Book 1 | ' +
                '11.00 usd | Open | 0.00 u]|0.00 u')

    @with_transaction()
    def test_assetbook_split_in_catergory_asset_diff_unit(self):
        """ splitbooking incoming to asset-cahbook,
            from category and asset-cashbook with different
            unit
        """
        pool = Pool()
        Book = pool.get('cashbook.book')
        Line = pool.get('cashbook.line')
        BType = pool.get('cashbook.type')
        Asset = pool.get('investment.asset')
        ProdTempl = pool.get('product.template')
        Uom = pool.get('product.uom')

        company = self.prep_company()
        with Transaction().set_context({'company': company.id}):
            types = self.prep_type()
            BType.write(*[
                [types],
                {
                    'feature': 'asset',
                }])
            category = self.prep_category(cattype='in')

            self.prep_party()
            asset = self.prep_asset_item(
                company=company,
                product=self.prep_asset_product(name='Product 1'))

            # set product to ounce
            ounce, = Uom.search([('symbol', '=', 'oz')])
            gram, = Uom.search([('symbol', '=', 'g')])

            ProdTempl.write(*[
                [asset.product.template],
                {
                    'default_uom': ounce.id,
                    'name': 'Aurum',
                }])

            Asset.write(*[
                [asset],
                {
                    'uom': ounce.id,
                    'rates': [('create', [{
                        'date': date(2022, 5, 1),
                        'rate': Decimal('1750.0'),
                        }, ])],
                }])
            self.assertEqual(
                asset.rec_name,
                'Aurum | 1,750.0000 usd/oz | 05/01/2022')

            (usd, euro) = self.prep_2nd_currency(company)
            self.assertEqual(company.currency.rec_name, 'Euro')
            self.assertEqual(asset.symbol, 'usd/oz')

            books = Book.create([{
                'start_date': date(2022, 4, 1),
                'name': 'Book ounce|usd',
                'btype': types.id,
                'company': company.id,
                'currency': usd.id,
                'number_sequ': self.prep_sequence().id,
                'asset': asset.id,
                'quantity_uom': ounce.id,
                'quantity_digits': 3,
                }, {
                'start_date': date(2022, 4, 1),
                'name': 'Book gram|euro',
                'btype': types.id,
                'company': company.id,
                'currency': euro.id,
                'number_sequ': self.prep_sequence().id,
                'asset': asset.id,
                'quantity_uom': gram.id,
                'quantity_digits': 3,
                }])
            self.assertEqual(
                books[0].rec_name,
                'Book ounce|usd | 0.00 usd | Open | 0.000 oz')
            self.assertEqual(books[0].balance_all, Decimal('0.0'))
            self.assertEqual(len(books[0].lines), 0)
            self.assertEqual(
                books[1].rec_name,
                'Book gram|euro | 0.00 € | Open | 0.000 g')
            self.assertEqual(books[1].balance_all, Decimal('0.0'))
            self.assertEqual(len(books[1].lines), 0)

            Book.write(*[
                [books[0]],
                {
                    'lines': [('create', [{
                        'bookingtype': 'spin',
                        'date': date(2022, 5, 1),
                        'splitlines': [('create', [{
                            'amount': Decimal('5.0'),
                            'splittype': 'cat',
                            'description': 'from category',
                            'category': category.id,
                            'quantity': Decimal('1.5'),
                            }, {
                            'amount': Decimal('6.0'),
                            'splittype': 'tr',
                            'description': 'from cashbook',
                            'booktransf': books[1].id,
                            'quantity': Decimal('2.5'),
                            }])],
                        }])],
                }])

            self.assertEqual(
                books[0].rec_name,
                'Book ounce|usd | 11.00 usd | Open | 4.000 oz')
            self.assertEqual(books[0].balance_all, Decimal('11.0'))
            self.assertEqual(len(books[0].lines), 1)
            self.assertEqual(
                books[0].lines[0].rec_name,
                '05/01/2022|Rev/Sp|11.00 usd|- [-]|4.000 oz')
            self.assertEqual(len(books[0].lines[0].splitlines), 2)
            self.assertEqual(
                books[0].lines[0].splitlines[0].rec_name,
                'Rev/Sp|5.00 usd|from category [Cat1]|1.500 oz')
            self.assertEqual(
                books[0].lines[0].splitlines[1].rec_name,
                'Rev/Sp|6.00 usd|from cashbook [Book gram|euro | 0.00 € | ' +
                'Open | 0.000 g]|2.500 oz')
            self.assertEqual(
                books[0].lines[0].splitlines[1].quantity,
                Decimal('2.5'))
            self.assertEqual(
                books[0].lines[0].splitlines[1].quantity_2nd_uom,
                Decimal('70.874'))

            self.assertEqual(
                books[1].rec_name,
                'Book gram|euro | 0.00 € | Open | 0.000 g')
            self.assertEqual(books[1].balance_all, Decimal('0.0'))
            self.assertEqual(len(books[1].lines), 0)

            Line.wfcheck([books[0].lines[0]])
            self.prep_valstore_run_worker()

            self.assertEqual(
                books[0].rec_name,
                'Book ounce|usd | 11.00 usd | Open | 4.000 oz')
            self.assertEqual(books[0].balance_all, Decimal('11.0'))
            self.assertEqual(len(books[0].lines), 1)
            self.assertEqual(
                books[0].lines[0].rec_name,
                '05/01/2022|Rev/Sp|11.00 usd|- [-]|4.000 oz')
            self.assertEqual(len(books[0].lines[0].splitlines), 2)
            self.assertEqual(
                books[0].lines[0].splitlines[0].rec_name,
                'Rev/Sp|5.00 usd|from category [Cat1]|1.500 oz')
            self.assertEqual(
                books[0].lines[0].splitlines[1].rec_name,
                'Rev/Sp|6.00 usd|from cashbook [Book gram|euro | -5.71 € | ' +
                'Open | -70.874 g]|2.500 oz')

            self.assertEqual(
                books[1].rec_name,
                'Book gram|euro | -5.71 € | Open | -70.874 g')
            self.assertEqual(books[1].balance_all, Decimal('-5.71'))
            self.assertEqual(len(books[1].lines), 1)
            self.assertEqual(
                books[1].lines[0].rec_name,
                '05/01/2022|to|-5.71 €|from cashbook [Book ounce|usd | ' +
                '11.00 usd | Open | 4.000 oz]|-70.874 g')

    @with_transaction()
    def test_assetbook_split_in_catergory_asset_diff_unit_diff_cat(self):
        """ splitbooking incoming to asset-cahbook,
            from category and asset-cashbook with different
            unit and different uom-category
        """
        pool = Pool()
        Book = pool.get('cashbook.book')
        BType = pool.get('cashbook.type')
        Asset = pool.get('investment.asset')
        ProdTempl = pool.get('product.template')
        Uom = pool.get('product.uom')

        company = self.prep_company()
        with Transaction().set_context({'company': company.id}):
            types = self.prep_type()
            BType.write(*[
                [types],
                {
                    'feature': 'asset',
                }])
            category = self.prep_category(cattype='in')

            self.prep_party()
            asset1 = self.prep_asset_item(
                company=company,
                product=self.prep_asset_product(name='Product 1'))
            asset2 = self.prep_asset_item(
                company=company,
                product=self.prep_asset_product(name='Product Liter'))

            # set product to ounce
            ounce, = Uom.search([('symbol', '=', 'oz')])
            liter, = Uom.search([('symbol', '=', 'l')])

            ProdTempl.write(*[
                [asset1.product.template],
                {
                    'default_uom': ounce.id,
                    'name': 'Aurum',
                },
                [asset2.product.template],
                {
                    'default_uom': liter.id,
                    'name': 'Liquid',
                },
                ])

            Asset.write(*[
                [asset1],
                {
                    'uom': ounce.id,
                    'rates': [('create', [{
                        'date': date(2022, 5, 1),
                        'rate': Decimal('1750.0'),
                        }, ])],
                },
                [asset2],
                {
                    'uom': liter.id,
                    'rates': [('create', [{
                        'date': date(2022, 5, 1),
                        'rate': Decimal('10.0'),
                        }, ])],
                },
                ])
            self.assertEqual(
                asset1.rec_name,
                'Aurum | 1,750.0000 usd/oz | 05/01/2022')
            self.assertEqual(
                asset2.rec_name, 'Liquid | 10.0000 usd/l | 05/01/2022')

            (usd, euro) = self.prep_2nd_currency(company)
            self.assertEqual(company.currency.rec_name, 'Euro')
            self.assertEqual(asset1.symbol, 'usd/oz')
            self.assertEqual(asset2.symbol, 'usd/l')

            books = Book.create([{
                'start_date': date(2022, 4, 1),
                'name': 'Book ounce|usd',
                'btype': types.id,
                'company': company.id,
                'currency': usd.id,
                'number_sequ': self.prep_sequence().id,
                'asset': asset1.id,
                'quantity_uom': ounce.id,
                'quantity_digits': 3,
                }, {
                'start_date': date(2022, 4, 1),
                'name': 'Book liter|euro',
                'btype': types.id,
                'company': company.id,
                'currency': euro.id,
                'number_sequ': self.prep_sequence().id,
                'asset': asset2.id,
                'quantity_uom': liter.id,
                'quantity_digits': 3,
                }])
            self.assertEqual(
                books[0].rec_name,
                'Book ounce|usd | 0.00 usd | Open | 0.000 oz')
            self.assertEqual(books[0].balance_all, Decimal('0.0'))
            self.assertEqual(len(books[0].lines), 0)
            self.assertEqual(
                books[1].rec_name,
                'Book liter|euro | 0.00 € | Open | 0.000 l')
            self.assertEqual(books[1].balance_all, Decimal('0.0'))
            self.assertEqual(len(books[1].lines), 0)

            self.assertRaisesRegex(
                UserError,
                r"Cannot transfer quantities between cashbooks with " +
                r"different unit-categories \(Weight != Volume\).",
                Book.write,
                *[
                    [books[0]],
                    {
                        'lines': [('create', [{
                            'bookingtype': 'spin',
                            'date': date(2022, 5, 1),
                            'splitlines': [('create', [{
                                'amount': Decimal('5.0'),
                                'splittype': 'cat',
                                'description': 'from category',
                                'category': category.id,
                                'quantity': Decimal('1.5'),
                                }, {
                                'amount': Decimal('6.0'),
                                'splittype': 'tr',
                                'description': 'from cashbook',
                                'booktransf': books[1].id,
                                'quantity': Decimal('2.5'),
                                }])],
                            }])],
                    },
                ])

    @with_transaction()
    def test_assetbook_split_out_category(self):
        """ splitbooking outgoing with asset
        """
        pool = Pool()
        Book = pool.get('cashbook.book')
        BType = pool.get('cashbook.type')

        company = self.prep_company()
        with Transaction().set_context({'company': company.id}):
            types = self.prep_type()
            BType.write(*[
                [types],
                {
                    'feature': 'asset',
                }])
            category = self.prep_category(cattype='out')

            self.prep_party()
            asset = self.prep_asset_item(
                company=company,
                product=self.prep_asset_product(name='Product 1'))
            self.assertEqual(asset.symbol, 'usd/u')

            book, = Book.create([{
                'start_date': date(2022, 4, 1),
                'name': 'Book 1',
                'btype': types.id,
                'company': company.id,
                'currency': company.currency.id,
                'number_sequ': self.prep_sequence().id,
                'asset': asset.id,
                'quantity_uom': asset.uom.id,
                'quantity_digits': 2,
                }])

            Book.write(*[
                [book],
                {
                    'lines': [('create', [{
                        'bookingtype': 'spout',
                        'date': date(2022, 5, 1),
                        'splitlines': [('create', [{
                            'amount': Decimal('5.0'),
                            'splittype': 'cat',
                            'description': 'to category',
                            'category': category.id,
                            'quantity': Decimal('1.5'),
                            }, {
                            'amount': Decimal('6.0'),
                            'splittype': 'cat',
                            'description': 'to category',
                            'category': category.id,
                            'quantity': Decimal('2.5'),
                            }])],
                        }])],
                }])

            self.assertEqual(
                book.rec_name, 'Book 1 | -11.00 usd | Open | -4.00 u')
            self.assertEqual(book.balance_all, Decimal('-11.0'))
            self.assertEqual(len(book.lines), 1)
            self.assertEqual(book.lines[0].splitline_has_quantity, False)
            self.assertEqual(
                book.lines[0].rec_name,
                '05/01/2022|Exp/Sp|-11.00 usd|- [-]|-4.00 u')

            self.assertEqual(len(book.lines[0].splitlines), 2)
            self.assertEqual(
                book.lines[0].splitlines[0].rec_name,
                'Exp/Sp|5.00 usd|to category [Cat1]|1.50 u')
            self.assertEqual(
                book.lines[0].splitlines[1].rec_name,
                'Exp/Sp|6.00 usd|to category [Cat1]|2.50 u')

    @with_transaction()
    def test_assetbook_split_out_category_and_assetbook(self):
        """ splitbooking outgoing,
            from asset-cashbook to asset-cashbook and to category
        """
        pool = Pool()
        Book = pool.get('cashbook.book')
        Line = pool.get('cashbook.line')
        BType = pool.get('cashbook.type')

        company = self.prep_company()
        with Transaction().set_context({'company': company.id}):
            types = self.prep_type()
            BType.write(*[
                [types],
                {
                    'feature': 'asset',
                }])
            category = self.prep_category(cattype='out')

            self.prep_party()
            asset = self.prep_asset_item(
                company=company,
                product=self.prep_asset_product(name='Product 1'))
            self.assertEqual(asset.symbol, 'usd/u')

            books = Book.create([{
                'start_date': date(2022, 4, 1),
                'name': 'Book 1',
                'btype': types.id,
                'company': company.id,
                'currency': company.currency.id,
                'number_sequ': self.prep_sequence().id,
                'asset': asset.id,
                'quantity_uom': asset.uom.id,
                'quantity_digits': 2,
                }, {
                'start_date': date(2022, 4, 1),
                'name': 'Book 2',
                'btype': types.id,
                'company': company.id,
                'currency': company.currency.id,
                'number_sequ': self.prep_sequence().id,
                'asset': asset.id,
                'quantity_uom': asset.uom.id,
                'quantity_digits': 2,
                }])

            Book.write(*[
                [books[0]],
                {
                    'lines': [('create', [{
                        'bookingtype': 'spout',
                        'date': date(2022, 5, 1),
                        'splitlines': [('create', [{
                            'amount': Decimal('5.0'),
                            'splittype': 'cat',
                            'description': 'to category',
                            'category': category.id,
                            'quantity': Decimal('1.5'),
                            }, {
                            'amount': Decimal('6.0'),
                            'splittype': 'tr',
                            'description': 'to cashbook',
                            'booktransf': books[1].id,
                            'quantity': Decimal('2.5'),
                            }])],
                        }])],
                }])

            self.assertEqual(
                books[0].rec_name,
                'Book 1 | -11.00 usd | Open | -4.00 u')
            self.assertEqual(books[0].balance_all, Decimal('-11.0'))

            self.assertEqual(len(books[0].lines), 1)
            self.assertEqual(
                books[0].lines[0].rec_name,
                '05/01/2022|Exp/Sp|-11.00 usd|- [-]|-4.00 u')
            self.assertEqual(books[0].lines[0].splitline_has_quantity, True)

            self.assertEqual(len(books[0].lines[0].splitlines), 2)
            self.assertEqual(
                books[0].lines[0].splitlines[0].rec_name,
                'Exp/Sp|5.00 usd|to category [Cat1]|1.50 u')
            self.assertEqual(
                books[0].lines[0].splitlines[1].rec_name,
                'Exp/Sp|6.00 usd|to cashbook [Book 2 | 0.00 usd | Open ' +
                '| 0.00 u]|2.50 u')

            self.assertEqual(len(books[0].lines[0].references), 0)
            self.assertEqual(books[0].lines[0].reference, None)

            self.assertEqual(
                books[1].rec_name, 'Book 2 | 0.00 usd | Open | 0.00 u')
            self.assertEqual(books[1].balance_all, Decimal('0.0'))
            self.assertEqual(len(books[1].lines), 0)

            Line.wfcheck([books[0].lines[0]])
            self.prep_valstore_run_worker()

            self.assertEqual(
                books[0].rec_name,
                'Book 1 | -11.00 usd | Open | -4.00 u')
            self.assertEqual(books[0].balance_all, Decimal('-11.0'))
            self.assertEqual(len(books[0].lines), 1)

            self.assertEqual(
                books[0].lines[0].rec_name,
                '05/01/2022|Exp/Sp|-11.00 usd|- [-]|-4.00 u')
            self.assertEqual(books[0].lines[0].splitline_has_quantity, True)

            self.assertEqual(len(books[0].lines[0].splitlines), 2)
            self.assertEqual(
                books[0].lines[0].splitlines[0].rec_name,
                'Exp/Sp|5.00 usd|to category [Cat1]|1.50 u')
            self.assertEqual(
                books[0].lines[0].splitlines[1].rec_name,
                'Exp/Sp|6.00 usd|to cashbook [Book 2 | 6.00 usd | Open' +
                ' | 2.50 u]|2.50 u')
            self.assertEqual(
                books[0].lines[0].splitlines[1].amount, Decimal('6.0'))
            self.assertEqual(
                books[0].lines[0].splitlines[1].amount_2nd_currency,
                None)
            self.assertEqual(
                books[0].lines[0].splitlines[1].quantity,
                Decimal('2.5'))
            self.assertEqual(books[0].lines[0].splitlines[1].quantity2nd, None)
            self.assertEqual(
                books[0].lines[0].splitlines[1].booktransf.rec_name,
                'Book 2 | 6.00 usd | Open | 2.50 u')
            self.assertEqual(len(books[0].lines[0].references), 1)
            self.assertEqual(
                books[0].lines[0].references[0].rec_name,
                '05/01/2022|from|6.00 usd|to cashbook [Book 1 | -11.00 usd' +
                ' | Open | -4.00 u]|2.50 u')
            self.assertEqual(books[0].lines[0].reference, None)

            self.assertEqual(
                books[1].rec_name, 'Book 2 | 6.00 usd | Open | 2.50 u')
            self.assertEqual(books[1].balance_all, Decimal('6.0'))
            self.assertEqual(len(books[1].lines), 1)
            self.assertEqual(
                books[1].lines[0].rec_name,
                '05/01/2022|from|6.00 usd|to cashbook [Book 1 | -11.00 usd' +
                ' | Open | -4.00 u]|2.50 u')

    @with_transaction()
    def test_assetbook_split_out_category_and_assetbook2(self):
        """ splitbooking outgoing,
            from cashbook to asset-cahbook and to category
        """
        pool = Pool()
        Book = pool.get('cashbook.book')
        Line = pool.get('cashbook.line')
        BType = pool.get('cashbook.type')

        company = self.prep_company()
        with Transaction().set_context({'company': company.id}):
            types_asset = self.prep_type()
            BType.write(*[
                [types_asset],
                {
                    'feature': 'asset',
                    'name': 'Asset',
                    'short': 'as',
                }])
            types_cash = self.prep_type()
            self.assertEqual(types_cash.rec_name, 'CAS - Cash')
            self.assertEqual(types_asset.rec_name, 'as - Asset')
            category = self.prep_category(cattype='out')

            self.prep_party()
            asset = self.prep_asset_item(
                company=company,
                product=self.prep_asset_product(name='Product 1'))
            self.assertEqual(asset.symbol, 'usd/u')

            books = Book.create([{
                'start_date': date(2022, 4, 1),
                'name': 'Book Cash',
                'btype': types_cash.id,
                'company': company.id,
                'currency': company.currency.id,
                'number_sequ': self.prep_sequence().id,
                }, {
                'start_date': date(2022, 4, 1),
                'name': 'Book Asset',
                'btype': types_asset.id,
                'company': company.id,
                'currency': company.currency.id,
                'number_sequ': self.prep_sequence().id,
                'asset': asset.id,
                'quantity_uom': asset.uom.id,
                'quantity_digits': 2,
                }])

            Book.write(*[
                [books[0]],
                {
                    'lines': [('create', [{
                        'bookingtype': 'spout',
                        'date': date(2022, 5, 1),
                        'splitlines': [('create', [{
                            'amount': Decimal('5.0'),
                            'splittype': 'cat',
                            'description': 'to category',
                            'category': category.id,
                            }, {
                            'amount': Decimal('6.0'),
                            'splittype': 'tr',
                            'description': 'to cashbook',
                            'booktransf': books[1].id,
                            'quantity': Decimal('2.5'),
                            }])],
                        }])],
                }])

            self.assertEqual(books[0].rec_name, 'Book Cash | -11.00 usd | Open')
            self.assertEqual(books[0].balance_all, Decimal('-11.0'))

            self.assertEqual(len(books[0].lines), 1)
            self.assertEqual(
                books[0].lines[0].rec_name,
                '05/01/2022|Exp/Sp|-11.00 usd|- [-]')
            self.assertEqual(books[0].lines[0].quantity, Decimal('2.5'))
            self.assertEqual(books[0].lines[0].quantity_credit, None)
            self.assertEqual(books[0].lines[0].quantity_debit, None)
            self.assertEqual(books[0].lines[0].quantity_2nd_uom, None)
            self.assertEqual(books[0].lines[0].splitline_has_quantity, True)

            self.assertEqual(len(books[0].lines[0].splitlines), 2)
            self.assertEqual(
                books[0].lines[0].splitlines[0].rec_name,
                'Exp/Sp|5.00 usd|to category [Cat1]')
            self.assertEqual(books[0].lines[0].splitlines[0].quantity, None)
            self.assertEqual(
                books[0].lines[0].splitlines[0].quantity_2nd_uom, None)
            self.assertEqual(
                books[0].lines[0].splitlines[1].rec_name,
                'Exp/Sp|6.00 usd|to cashbook [Book Asset | 0.00 usd | ' +
                'Open | 0.00 u]')
            self.assertEqual(
                books[0].lines[0].splitlines[1].quantity,
                Decimal('2.5'))
            self.assertEqual(
                books[0].lines[0].splitlines[1].quantity_2nd_uom, None)

            self.assertEqual(len(books[0].lines[0].references), 0)
            self.assertEqual(books[0].lines[0].reference, None)

            self.assertEqual(
                books[1].rec_name,
                'Book Asset | 0.00 usd | Open | 0.00 u')
            self.assertEqual(books[1].balance_all, Decimal('0.0'))
            self.assertEqual(len(books[1].lines), 0)

            Line.wfcheck([books[0].lines[0]])
            self.prep_valstore_run_worker()

            self.assertEqual(books[0].rec_name, 'Book Cash | -11.00 usd | Open')
            self.assertEqual(books[0].balance_all, Decimal('-11.0'))
            self.assertEqual(len(books[0].lines), 1)

            self.assertEqual(
                books[0].lines[0].rec_name,
                '05/01/2022|Exp/Sp|-11.00 usd|- [-]')
            self.assertEqual(books[0].lines[0].splitline_has_quantity, True)
            self.assertEqual(books[0].lines[0].quantity, Decimal('2.5'))
            self.assertEqual(books[0].lines[0].quantity_credit, None)
            self.assertEqual(books[0].lines[0].quantity_debit, None)
            self.assertEqual(books[0].lines[0].quantity_2nd_uom, None)

            self.assertEqual(len(books[0].lines[0].splitlines), 2)
            self.assertEqual(
                books[0].lines[0].splitlines[0].rec_name,
                'Exp/Sp|5.00 usd|to category [Cat1]')
            self.assertEqual(
                books[0].lines[0].splitlines[1].rec_name,
                'Exp/Sp|6.00 usd|to cashbook [Book Asset | 6.00 usd' +
                ' | Open | 2.50 u]')
            self.assertEqual(
                books[0].lines[0].splitlines[1].amount, Decimal('6.0'))
            self.assertEqual(
                books[0].lines[0].splitlines[1].amount_2nd_currency,
                None)
            self.assertEqual(
                books[0].lines[0].splitlines[1].quantity,
                Decimal('2.5'))
            self.assertEqual(books[0].lines[0].splitlines[1].quantity2nd, None)
            self.assertEqual(
                books[0].lines[0].splitlines[1].booktransf.rec_name,
                'Book Asset | 6.00 usd | Open | 2.50 u')
            self.assertEqual(len(books[0].lines[0].references), 1)
            self.assertEqual(
                books[0].lines[0].references[0].rec_name,
                '05/01/2022|from|6.00 usd|to cashbook [Book Cash | ' +
                '-11.00 usd | Open]|2.50 u')
            self.assertEqual(books[0].lines[0].reference, None)

            self.assertEqual(
                books[1].rec_name,
                'Book Asset | 6.00 usd | Open | 2.50 u')
            self.assertEqual(books[1].balance_all, Decimal('6.0'))
            self.assertEqual(len(books[1].lines), 1)
            self.assertEqual(
                books[1].lines[0].rec_name,
                '05/01/2022|from|6.00 usd|to cashbook [Book Cash | ' +
                '-11.00 usd | Open]|2.50 u')

    @with_transaction()
    def test_assetbook_split_out_catergory_asset_diff_unit(self):
        """ splitbooking outgoing to asset-cahbook,
            to category and asset-cashbook with different
            unit
        """
        pool = Pool()
        Book = pool.get('cashbook.book')
        Line = pool.get('cashbook.line')
        BType = pool.get('cashbook.type')
        Asset = pool.get('investment.asset')
        ProdTempl = pool.get('product.template')
        Uom = pool.get('product.uom')

        company = self.prep_company()
        with Transaction().set_context({'company': company.id}):
            types = self.prep_type()
            BType.write(*[
                [types],
                {
                    'feature': 'asset',
                }])
            category = self.prep_category(cattype='out')

            self.prep_party()
            asset = self.prep_asset_item(
                company=company,
                product=self.prep_asset_product(name='Product 1'))

            # set product to ounce
            ounce, = Uom.search([('symbol', '=', 'oz')])
            gram, = Uom.search([('symbol', '=', 'g')])

            ProdTempl.write(*[
                [asset.product.template],
                {
                    'default_uom': ounce.id,
                    'name': 'Aurum',
                }])

            Asset.write(*[
                [asset],
                {
                    'uom': ounce.id,
                    'rates': [('create', [{
                        'date': date(2022, 5, 1),
                        'rate': Decimal('1750.0'),
                        }, ])],
                }])
            self.assertEqual(
                asset.rec_name,
                'Aurum | 1,750.0000 usd/oz | 05/01/2022')

            (usd, euro) = self.prep_2nd_currency(company)
            self.assertEqual(company.currency.rec_name, 'Euro')
            self.assertEqual(asset.symbol, 'usd/oz')

            books = Book.create([{
                'start_date': date(2022, 4, 1),
                'name': 'Book ounce|usd',
                'btype': types.id,
                'company': company.id,
                'currency': usd.id,
                'number_sequ': self.prep_sequence().id,
                'asset': asset.id,
                'quantity_uom': ounce.id,
                'quantity_digits': 3,
                }, {
                'start_date': date(2022, 4, 1),
                'name': 'Book gram|euro',
                'btype': types.id,
                'company': company.id,
                'currency': euro.id,
                'number_sequ': self.prep_sequence().id,
                'asset': asset.id,
                'quantity_uom': gram.id,
                'quantity_digits': 3,
                }])
            self.assertEqual(
                books[0].rec_name,
                'Book ounce|usd | 0.00 usd | Open | 0.000 oz')
            self.assertEqual(books[0].balance_all, Decimal('0.0'))
            self.assertEqual(len(books[0].lines), 0)
            self.assertEqual(
                books[1].rec_name,
                'Book gram|euro | 0.00 € | Open | 0.000 g')
            self.assertEqual(books[1].balance_all, Decimal('0.0'))
            self.assertEqual(len(books[1].lines), 0)

            Book.write(*[
                [books[0]],
                {
                    'lines': [('create', [{
                        'bookingtype': 'spout',
                        'date': date(2022, 5, 1),
                        'splitlines': [('create', [{
                            'amount': Decimal('5.0'),
                            'splittype': 'cat',
                            'description': 'to category',
                            'category': category.id,
                            'quantity': Decimal('1.5'),
                            }, {
                            'amount': Decimal('6.0'),
                            'splittype': 'tr',
                            'description': 'to cashbook',
                            'booktransf': books[1].id,
                            'quantity': Decimal('2.5'),
                            }])],
                        }])],
                }])

            self.assertEqual(
                books[0].rec_name,
                'Book ounce|usd | -11.00 usd | Open | -4.000 oz')
            self.assertEqual(books[0].balance_all, Decimal('-11.0'))
            self.assertEqual(len(books[0].lines), 1)
            self.assertEqual(
                books[0].lines[0].rec_name,
                '05/01/2022|Exp/Sp|-11.00 usd|- [-]|-4.000 oz')
            self.assertEqual(len(books[0].lines[0].splitlines), 2)
            self.assertEqual(
                books[0].lines[0].splitlines[0].rec_name,
                'Exp/Sp|5.00 usd|to category [Cat1]|1.500 oz')
            self.assertEqual(
                books[0].lines[0].splitlines[1].rec_name,
                'Exp/Sp|6.00 usd|to cashbook [Book gram|euro | 0.00 € | ' +
                'Open | 0.000 g]|2.500 oz')
            self.assertEqual(
                books[0].lines[0].splitlines[1].quantity,
                Decimal('2.5'))
            self.assertEqual(
                books[0].lines[0].splitlines[1].quantity_2nd_uom,
                Decimal('70.874'))

            self.assertEqual(
                books[1].rec_name,
                'Book gram|euro | 0.00 € | Open | 0.000 g')
            self.assertEqual(books[1].balance_all, Decimal('0.0'))
            self.assertEqual(len(books[1].lines), 0)

            Line.wfcheck([books[0].lines[0]])
            self.prep_valstore_run_worker()

            self.assertEqual(
                books[0].rec_name,
                'Book ounce|usd | -11.00 usd | Open | -4.000 oz')
            self.assertEqual(books[0].balance_all, Decimal('-11.0'))
            self.assertEqual(len(books[0].lines), 1)
            self.assertEqual(
                books[0].lines[0].rec_name,
                '05/01/2022|Exp/Sp|-11.00 usd|- [-]|-4.000 oz')
            self.assertEqual(len(books[0].lines[0].splitlines), 2)
            self.assertEqual(
                books[0].lines[0].splitlines[0].rec_name,
                'Exp/Sp|5.00 usd|to category [Cat1]|1.500 oz')
            self.assertEqual(
                books[0].lines[0].splitlines[1].rec_name,
                'Exp/Sp|6.00 usd|to cashbook [Book gram|euro | 5.71 € | ' +
                'Open | 70.874 g]|2.500 oz')

            self.assertEqual(
                books[1].rec_name,
                'Book gram|euro | 5.71 € | Open | 70.874 g')
            self.assertEqual(books[1].balance_all, Decimal('5.71'))
            self.assertEqual(len(books[1].lines), 1)
            self.assertEqual(
                books[1].lines[0].rec_name,
                '05/01/2022|from|5.71 €|to cashbook [Book ounce|usd | ' +
                '-11.00 usd | Open | -4.000 oz]|70.874 g')

    @with_transaction()
    def test_assetbook_split_out_catergory_asset_diff_unit_diff_cat(self):
        """ splitbooking outgoing to asset-cahbook,
            to category and asset-cashbook with different
            unit and different uom-category
        """
        pool = Pool()
        Book = pool.get('cashbook.book')
        BType = pool.get('cashbook.type')
        Asset = pool.get('investment.asset')
        ProdTempl = pool.get('product.template')
        Uom = pool.get('product.uom')

        company = self.prep_company()
        with Transaction().set_context({'company': company.id}):
            types = self.prep_type()
            BType.write(*[
                [types],
                {
                    'feature': 'asset',
                }])
            category = self.prep_category(cattype='out')

            self.prep_party()
            asset1 = self.prep_asset_item(
                company=company,
                product=self.prep_asset_product(name='Product 1'))
            asset2 = self.prep_asset_item(
                company=company,
                product=self.prep_asset_product(name='Product Liter'))

            # set product to ounce
            ounce, = Uom.search([('symbol', '=', 'oz')])
            liter, = Uom.search([('symbol', '=', 'l')])

            ProdTempl.write(*[
                [asset1.product.template],
                {
                    'default_uom': ounce.id,
                    'name': 'Aurum',
                },
                [asset2.product.template],
                {
                    'default_uom': liter.id,
                    'name': 'Liquid',
                },
                ])

            Asset.write(*[
                [asset1],
                {
                    'uom': ounce.id,
                    'rates': [('create', [{
                        'date': date(2022, 5, 1),
                        'rate': Decimal('1750.0'),
                        }, ])],
                },
                [asset2],
                {
                    'uom': liter.id,
                    'rates': [('create', [{
                        'date': date(2022, 5, 1),
                        'rate': Decimal('10.0'),
                        }, ])],
                },
                ])
            self.assertEqual(
                asset1.rec_name,
                'Aurum | 1,750.0000 usd/oz | 05/01/2022')
            self.assertEqual(
                asset2.rec_name,
                'Liquid | 10.0000 usd/l | 05/01/2022')

            (usd, euro) = self.prep_2nd_currency(company)
            self.assertEqual(company.currency.rec_name, 'Euro')
            self.assertEqual(asset1.symbol, 'usd/oz')
            self.assertEqual(asset2.symbol, 'usd/l')

            books = Book.create([{
                'start_date': date(2022, 4, 1),
                'name': 'Book ounce|usd',
                'btype': types.id,
                'company': company.id,
                'currency': usd.id,
                'number_sequ': self.prep_sequence().id,
                'asset': asset1.id,
                'quantity_uom': ounce.id,
                'quantity_digits': 3,
                }, {
                'start_date': date(2022, 4, 1),
                'name': 'Book liter|euro',
                'btype': types.id,
                'company': company.id,
                'currency': euro.id,
                'number_sequ': self.prep_sequence().id,
                'asset': asset2.id,
                'quantity_uom': liter.id,
                'quantity_digits': 3,
                }])
            self.assertEqual(
                books[0].rec_name,
                'Book ounce|usd | 0.00 usd | Open | 0.000 oz')
            self.assertEqual(books[0].balance_all, Decimal('0.0'))
            self.assertEqual(len(books[0].lines), 0)
            self.assertEqual(
                books[1].rec_name,
                'Book liter|euro | 0.00 € | Open | 0.000 l')
            self.assertEqual(books[1].balance_all, Decimal('0.0'))
            self.assertEqual(len(books[1].lines), 0)

            self.assertRaisesRegex(
                UserError,
                r"Cannot transfer quantities between cashbooks with " +
                r"different unit-categories \(Weight != Volume\).",
                Book.write,
                *[
                    [books[0]],
                    {
                        'lines': [('create', [{
                            'bookingtype': 'spout',
                            'date': date(2022, 5, 1),
                            'splitlines': [('create', [{
                                'amount': Decimal('5.0'),
                                'splittype': 'cat',
                                'description': 'from category',
                                'category': category.id,
                                'quantity': Decimal('1.5'),
                                }, {
                                'amount': Decimal('6.0'),
                                'splittype': 'tr',
                                'description': 'from cashbook',
                                'booktransf': books[1].id,
                                'quantity': Decimal('2.5'),
                                }])],
                            }])],
                    },
                ])

    # TODO:
    # in/out-splitbuchung

# end CbInvTestCase
