# -*- coding: utf-8 -*-
# This file is part of the cashbook-module from m-ds for Tryton.
# The COPYRIGHT file at the top level of this repository contains the
# full copyright notices and license terms.


from trytond.modules.cashbook.tests.test_module import CashbookTestCase
from trytond.modules.investment.tests.test_module import InvestmentTestCase

from .yieldtest import YieldTestCase
from .book import CbInvTestCase
from .reconciliation import ReconTestCase
from .valuestore import ValueStoreTestCase


class CashbookInvestmentTestCase(
        ValueStoreTestCase,
        CashbookTestCase,
        InvestmentTestCase,
        CbInvTestCase,
        ReconTestCase,
        YieldTestCase):
    'Test cashbook-investment module'
    module = 'cashbook_investment'

# end CashbookInvestmentTestCase


del CashbookTestCase
del InvestmentTestCase
