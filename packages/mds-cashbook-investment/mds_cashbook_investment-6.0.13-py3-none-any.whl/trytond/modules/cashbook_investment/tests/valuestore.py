# -*- coding: utf-8 -*-
# This file is part of the cashbook-module from m-ds for Tryton.
# The COPYRIGHT file at the top level of this repository contains the
# full copyright notices and license terms.

from trytond.tests.test_tryton import with_transaction
from trytond.pool import Pool
from trytond.transaction import Transaction
from datetime import date
from decimal import Decimal


class ValueStoreTestCase(object):
    """ test update of cashbooks on update of asset
    """
    @with_transaction()
    def test_valstore_update_asset_rate(self):
        """ update rate of asset, should update cashbook
        """
        pool = Pool()
        Book = pool.get('cashbook.book')
        BType = pool.get('cashbook.type')
        Asset = pool.get('investment.asset')
        Queue = pool.get('ir.queue')
        ValStore = pool.get('cashbook.values')

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

            self.assertEqual(Queue.search_count([]), 0)

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
                    'quantity': Decimal('1.5'),
                    }])],
                }])

            # run worker
            self.assertEqual(
                ValStore.search_count([]),
                len(Book.valuestore_fields()))
            self.prep_valstore_run_worker()

            self.assertEqual(book.name, 'Book 1')
            self.assertEqual(book.rec_name, 'Book 1 | 2.50 € | Open | 1.500 u')
            self.assertEqual(len(book.lines), 1)
            self.assertEqual(
                book.lines[0].rec_name,
                '05/01/2022|Rev|2.50 €|Text 1 [Cat1]|1.500 u')

            values = ValStore.search([
                ('cashbook', '=', book.id)], order=[('field_name', 'ASC')])
            self.assertEqual(len(values), len(Book.valuestore_fields()))

            self.assertEqual(
                values[0].rec_name,
                '[Book 1 | 2.50 € | Open | 1.500 u]|balance|2.50|2')
            self.assertEqual(
                values[1].rec_name,
                '[Book 1 | 2.50 € | Open | 1.500 u]|balance_all|2.50|2')
            self.assertEqual(
                values[2].rec_name,
                '[Book 1 | 2.50 € | Open | 1.500 u]|balance_ref|2.50|2')
            self.assertEqual(
                values[3].rec_name,
                '[Book 1 | 2.50 € | Open | 1.500 u]|current_rate|2.67|2')
            self.assertEqual(
                values[4].rec_name,
                '[Book 1 | 2.50 € | Open | 1.500 u]|current_value|4.00|2')
            self.assertEqual(
                values[5].rec_name,
                '[Book 1 | 2.50 € | Open | 1.500 u]|current_value_ref|4.00|2')
            self.assertEqual(
                values[6].rec_name,
                '[Book 1 | 2.50 € | Open | 1.500 u]|diff_amount|1.50|2')
            self.assertEqual(
                values[7].rec_name,
                '[Book 1 | 2.50 € | Open | 1.500 u]|diff_percent|60.00|2')
            self.assertEqual(
                values[8].rec_name,
                '[Book 1 | 2.50 € | Open | 1.500 u]|purchase_amount|2.50|2')
            self.assertEqual(
                values[9].rec_name,
                '[Book 1 | 2.50 € | Open | 1.500 u]|quantity|1.500|3')
            self.assertEqual(
                values[10].rec_name,
                '[Book 1 | 2.50 € | Open | 1.500 u]|quantity_all|1.500|3')
            self.assertEqual(
                values[11].rec_name,
                '[Book 1 | 2.50 € | Open | 1.500 u]|yield_balance|4.00|2')
            self.assertEqual(
                values[12].rec_name,
                '[Book 1 | 2.50 € | Open | 1.500 u]|yield_dividend_12m|0.00|2')
            self.assertEqual(
                values[13].rec_name,
                '[Book 1 | 2.50 € | Open | 1.500 u]|yield_dividend_total|0.00|2')
            self.assertEqual(
                values[14].rec_name,
                '[Book 1 | 2.50 € | Open | 1.500 u]|yield_fee_12m|0.00|2')
            self.assertEqual(
                values[15].rec_name,
                '[Book 1 | 2.50 € | Open | 1.500 u]|yield_fee_total|0.00|2')
            self.assertEqual(
                values[16].rec_name,
                '[Book 1 | 2.50 € | Open | 1.500 u]|yield_sales|2.50|2')
            self.assertEqual(
                values[17].rec_name,
                '[Book 1 | 2.50 € | Open | 1.500 u]|yield_sales_12m|0.00|2')

            # add rate
            Asset.write(*[
                [asset],
                {
                    'rates': [('create', [{
                        'date': date(2022, 5, 10),
                        'rate': Decimal('3.0'),
                        }])],
                }])
            self.assertEqual(
                asset.rec_name, 'Product 1 | 3.0000 usd/u | 05/10/2022')

            # run worker
            self.prep_valstore_run_worker()

            values = ValStore.search([
                ('cashbook', '=', book.id)], order=[('field_name', 'ASC')])
            self.assertEqual(len(values), len(Book.valuestore_fields()))

            self.assertEqual(
                values[0].rec_name,
                '[Book 1 | 2.50 € | Open | 1.500 u]|balance|2.50|2')
            self.assertEqual(
                values[1].rec_name,
                '[Book 1 | 2.50 € | Open | 1.500 u]|balance_all|2.50|2')
            self.assertEqual(
                values[2].rec_name,
                '[Book 1 | 2.50 € | Open | 1.500 u]|balance_ref|2.50|2')
            self.assertEqual(
                values[3].rec_name,
                '[Book 1 | 2.50 € | Open | 1.500 u]|current_rate|2.86|2')
            self.assertEqual(
                values[4].rec_name,
                '[Book 1 | 2.50 € | Open | 1.500 u]|current_value|4.29|2')
            self.assertEqual(
                values[5].rec_name,
                '[Book 1 | 2.50 € | Open | 1.500 u]|current_value_ref|4.29|2')
            self.assertEqual(
                values[6].rec_name,
                '[Book 1 | 2.50 € | Open | 1.500 u]|diff_amount|1.79|2')
            self.assertEqual(
                values[7].rec_name,
                '[Book 1 | 2.50 € | Open | 1.500 u]|diff_percent|71.60|2')
            self.assertEqual(
                values[8].rec_name,
                '[Book 1 | 2.50 € | Open | 1.500 u]|purchase_amount|2.50|2')
            self.assertEqual(
                values[9].rec_name,
                '[Book 1 | 2.50 € | Open | 1.500 u]|quantity|1.500|3')
            self.assertEqual(
                values[10].rec_name,
                '[Book 1 | 2.50 € | Open | 1.500 u]|quantity_all|1.500|3')
            self.assertEqual(
                values[11].rec_name,
                '[Book 1 | 2.50 € | Open | 1.500 u]|yield_balance|4.29|2')
            self.assertEqual(
                values[12].rec_name,
                '[Book 1 | 2.50 € | Open | 1.500 u]|yield_dividend_12m|0.00|2')
            self.assertEqual(
                values[13].rec_name,
                '[Book 1 | 2.50 € | Open | 1.500 u]|yield_dividend_total|0.00|2')
            self.assertEqual(
                values[14].rec_name,
                '[Book 1 | 2.50 € | Open | 1.500 u]|yield_fee_12m|0.00|2')
            self.assertEqual(
                values[15].rec_name,
                '[Book 1 | 2.50 € | Open | 1.500 u]|yield_fee_total|0.00|2')
            self.assertEqual(
                values[16].rec_name,
                '[Book 1 | 2.50 € | Open | 1.500 u]|yield_sales|2.50|2')
            self.assertEqual(
                values[17].rec_name,
                '[Book 1 | 2.50 € | Open | 1.500 u]|yield_sales_12m|0.00|2')

            # update rate
            self.assertEqual(asset.rates[0].rate, Decimal('3.0'))
            self.assertEqual(asset.rates[0].date, date(2022, 5, 10))
            Asset.write(*[
                [asset],
                {
                    'rates': [('write', [asset.rates[0]], {
                        'rate': Decimal('3.5'),
                        })],
                }])
            self.assertEqual(
                asset.rec_name, 'Product 1 | 3.5000 usd/u | 05/10/2022')

            # run worker
            self.prep_valstore_run_worker()

            values = ValStore.search([
                ('cashbook', '=', book.id)], order=[('field_name', 'ASC')])
            self.assertEqual(len(values), len(Book.valuestore_fields()))

            self.assertEqual(
                values[0].rec_name,
                '[Book 1 | 2.50 € | Open | 1.500 u]|balance|2.50|2')
            self.assertEqual(
                values[1].rec_name,
                '[Book 1 | 2.50 € | Open | 1.500 u]|balance_all|2.50|2')
            self.assertEqual(
                values[2].rec_name,
                '[Book 1 | 2.50 € | Open | 1.500 u]|balance_ref|2.50|2')
            self.assertEqual(
                values[3].rec_name,
                '[Book 1 | 2.50 € | Open | 1.500 u]|current_rate|3.33|2')
            self.assertEqual(
                values[4].rec_name,
                '[Book 1 | 2.50 € | Open | 1.500 u]|current_value|5.00|2')
            self.assertEqual(
                values[5].rec_name,
                '[Book 1 | 2.50 € | Open | 1.500 u]|current_value_ref|5.00|2')
            self.assertEqual(
                values[6].rec_name,
                '[Book 1 | 2.50 € | Open | 1.500 u]|diff_amount|2.50|2')
            self.assertEqual(
                values[7].rec_name,
                '[Book 1 | 2.50 € | Open | 1.500 u]|diff_percent|100.00|2')
            self.assertEqual(
                values[8].rec_name,
                '[Book 1 | 2.50 € | Open | 1.500 u]|purchase_amount|2.50|2')
            self.assertEqual(
                values[9].rec_name,
                '[Book 1 | 2.50 € | Open | 1.500 u]|quantity|1.500|3')
            self.assertEqual(
                values[10].rec_name,
                '[Book 1 | 2.50 € | Open | 1.500 u]|quantity_all|1.500|3')
            self.assertEqual(
                values[11].rec_name,
                '[Book 1 | 2.50 € | Open | 1.500 u]|yield_balance|5.00|2')
            self.assertEqual(
                values[12].rec_name,
                '[Book 1 | 2.50 € | Open | 1.500 u]|yield_dividend_12m|0.00|2')
            self.assertEqual(
                values[13].rec_name,
                '[Book 1 | 2.50 € | Open | 1.500 u]|yield_dividend_total|0.00|2')
            self.assertEqual(
                values[14].rec_name,
                '[Book 1 | 2.50 € | Open | 1.500 u]|yield_fee_12m|0.00|2')
            self.assertEqual(
                values[15].rec_name,
                '[Book 1 | 2.50 € | Open | 1.500 u]|yield_fee_total|0.00|2')
            self.assertEqual(
                values[16].rec_name,
                '[Book 1 | 2.50 € | Open | 1.500 u]|yield_sales|2.50|2')
            self.assertEqual(
                values[17].rec_name,
                '[Book 1 | 2.50 € | Open | 1.500 u]|yield_sales_12m|0.00|2')

            # delete rate
            self.assertEqual(asset.rates[0].rate, Decimal('3.5'))
            self.assertEqual(asset.rates[0].date, date(2022, 5, 10))
            Asset.write(*[
                [asset],
                {
                    'rates': [('delete', [asset.rates[0].id])],
                }])
            self.assertEqual(
                asset.rec_name, 'Product 1 | 2.8000 usd/u | 05/02/2022')

            # run worker
            self.prep_valstore_run_worker()

            values = ValStore.search([
                ('cashbook', '=', book.id)], order=[('field_name', 'ASC')])
            self.assertEqual(len(values), len(Book.valuestore_fields()))

            self.assertEqual(
                values[0].rec_name,
                '[Book 1 | 2.50 € | Open | 1.500 u]|balance|2.50|2')
            self.assertEqual(
                values[1].rec_name,
                '[Book 1 | 2.50 € | Open | 1.500 u]|balance_all|2.50|2')
            self.assertEqual(
                values[2].rec_name,
                '[Book 1 | 2.50 € | Open | 1.500 u]|balance_ref|2.50|2')
            self.assertEqual(
                values[3].rec_name,
                '[Book 1 | 2.50 € | Open | 1.500 u]|current_rate|2.67|2')
            self.assertEqual(
                values[4].rec_name,
                '[Book 1 | 2.50 € | Open | 1.500 u]|current_value|4.00|2')
            self.assertEqual(
                values[5].rec_name,
                '[Book 1 | 2.50 € | Open | 1.500 u]|current_value_ref|4.00|2')
            self.assertEqual(
                values[6].rec_name,
                '[Book 1 | 2.50 € | Open | 1.500 u]|diff_amount|1.50|2')
            self.assertEqual(
                values[7].rec_name,
                '[Book 1 | 2.50 € | Open | 1.500 u]|diff_percent|60.00|2')
            self.assertEqual(
                values[8].rec_name,
                '[Book 1 | 2.50 € | Open | 1.500 u]|purchase_amount|2.50|2')
            self.assertEqual(
                values[9].rec_name,
                '[Book 1 | 2.50 € | Open | 1.500 u]|quantity|1.500|3')
            self.assertEqual(
                values[10].rec_name,
                '[Book 1 | 2.50 € | Open | 1.500 u]|quantity_all|1.500|3')
            self.assertEqual(
                values[11].rec_name,
                '[Book 1 | 2.50 € | Open | 1.500 u]|yield_balance|4.00|2')
            self.assertEqual(
                values[12].rec_name,
                '[Book 1 | 2.50 € | Open | 1.500 u]|yield_dividend_12m|0.00|2')
            self.assertEqual(
                values[13].rec_name,
                '[Book 1 | 2.50 € | Open | 1.500 u]|yield_dividend_total|0.00|2')
            self.assertEqual(
                values[14].rec_name,
                '[Book 1 | 2.50 € | Open | 1.500 u]|yield_fee_12m|0.00|2')
            self.assertEqual(
                values[15].rec_name,
                '[Book 1 | 2.50 € | Open | 1.500 u]|yield_fee_total|0.00|2')
            self.assertEqual(
                values[16].rec_name,
                '[Book 1 | 2.50 € | Open | 1.500 u]|yield_sales|2.50|2')
            self.assertEqual(
                values[17].rec_name,
                '[Book 1 | 2.50 € | Open | 1.500 u]|yield_sales_12m|0.00|2')

# end ValueStoreTestCase
