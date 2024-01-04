# -*- coding: utf-8 -*-
# This file is part of the cashbook-module from m-ds for Tryton.
# The COPYRIGHT file at the top level of this repository contains the
# full copyright notices and license terms.

from trytond.tests.test_tryton import with_transaction
from trytond.pool import Pool
from trytond.transaction import Transaction
from datetime import date
from decimal import Decimal


class ReconTestCase(object):
    """ test reconciliation
    """
    @with_transaction()
    def test_recon_set_start_quantity_by_cashbook(self):
        """ set start-quantity of reconciliation from cashbook-setting
        """
        pool = Pool()
        Book = pool.get('cashbook.book')
        Reconciliation = pool.get('cashbook.recon')
        BType = pool.get('cashbook.type')

        company = self.prep_company()
        with Transaction().set_context({'company': company.id}):
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

            book, = Book.create([{
                'name': 'Asset-Book',
                'btype': type_depot.id,
                'company': company.id,
                'currency': company.currency.id,
                'asset': asset.id,
                'quantity_uom': asset.uom.id,
                'start_date': date(2022, 5, 1),
                'number_sequ': self.prep_sequence().id,
                'reconciliations': [('create', [{
                        'date': date(2022, 5, 28),
                        'date_from': date(2022, 5, 1),
                        'date_to':  date(2022, 5, 31),
                    }])],
                }])
            self.assertEqual(book.name, 'Asset-Book')
            self.assertEqual(book.reconciliations[0].feature, 'asset')
            self.assertEqual(
                book.reconciliations[0].rec_name,
                '05/01/2022 - 05/31/2022 | 0.00 usd - 0.00 usd [0] ' +
                '| 0.0000 u - 0.0000 u')

            Reconciliation.wfcheck(list(book.reconciliations))
            self.assertEqual(
                book.reconciliations[0].rec_name,
                '05/01/2022 - 05/31/2022 | 0.00 usd - 0.00 usd [0] ' +
                '| 0.0000 u - 0.0000 u')

    @with_transaction()
    def test_recon_set_start_quantity_by_predecessor(self):
        """ set stat-quantity from end_amount of predecessor
        """
        pool = Pool()
        Book = pool.get('cashbook.book')
        Lines = pool.get('cashbook.line')
        Reconciliation = pool.get('cashbook.recon')
        BType = pool.get('cashbook.type')

        company = self.prep_company()
        with Transaction().set_context({'company': company.id}):
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

            category = self.prep_category(cattype='in')
            party = self.prep_party()
            book, = Book.create([{
                'name': 'Asset-Book',
                'btype': type_depot.id,
                'company': company.id,
                'currency': company.currency.id,
                'asset': asset.id,
                'quantity_uom': asset.uom.id,
                'quantity_digits': 3,
                'start_date': date(2022, 5, 1),
                'number_sequ': self.prep_sequence().id,
                'reconciliations': [('create', [{
                        'date': date(2022, 5, 28),
                        'date_from': date(2022, 5, 1),
                        'date_to':  date(2022, 5, 31),
                    }])],
                'lines': [('create', [{
                        'date': date(2022, 5, 5),
                        'bookingtype': 'in',
                        'category': category.id,
                        'description': 'Line 1',
                        'amount': Decimal('5.0'),
                        'quantity': Decimal('1.5'),
                        'party': party.id,
                    }, {
                        'date': date(2022, 5, 6),
                        'bookingtype': 'in',
                        'category': category.id,
                        'description': 'Line 2',
                        'party': party.id,
                        'amount': Decimal('7.0'),
                        'quantity': Decimal('2.5'),
                    },])],
                }])
            self.assertEqual(book.name, 'Asset-Book')
            self.assertEqual(len(book.reconciliations), 1)
            self.assertEqual(
                book.reconciliations[0].rec_name,
                '05/01/2022 - 05/31/2022 | 0.00 usd - 0.00 usd [0] | ' +
                '0.000 u - 0.000 u')
            self.assertEqual(len(book.reconciliations[0].lines), 0)

            Lines.wfcheck(list(book.lines))

            self.assertEqual(book.lines[0].quantity_balance, Decimal('1.5'))
            self.assertEqual(book.lines[1].quantity_balance, Decimal('4.0'))

            Reconciliation.wfcheck(list(book.reconciliations))

            self.assertEqual(book.lines[0].quantity_balance, Decimal('1.5'))
            self.assertEqual(book.lines[1].quantity_balance, Decimal('4.0'))

            self.assertEqual(book.reconciliations[0].state, 'check')
            self.assertEqual(
                book.reconciliations[0].rec_name,
                '05/01/2022 - 05/31/2022 | 0.00 usd - 12.00 usd [2] ' +
                '| 0.000 u - 4.000 u')
            Reconciliation.wfdone(list(book.reconciliations))
            self.assertEqual(book.reconciliations[0].state, 'done')

            recons = Reconciliation.create([{
                'cashbook': book.id,
                'date_from': date(2022, 5, 31),
                'date_to': date(2022, 6, 30),
                }])
            self.assertEqual(
                recons[0].rec_name,
                '05/31/2022 - 06/30/2022 | 0.00 usd - 0.00 usd [0] | ' +
                '0.000 u - 0.000 u')
            Reconciliation.wfcheck(recons)
            self.assertEqual(
                recons[0].rec_name,
                '05/31/2022 - 06/30/2022 | 12.00 usd - 12.00 usd [0] | ' +
                '4.000 u - 4.000 u')

# end ReconTestCase
