# -*- coding: utf-8 -*-
# This file is part of the cashbook-module from m-ds for Tryton.
# The COPYRIGHT file at the top level of this repository contains the
# full copyright notices and license terms.


from trytond.pool import PoolMeta


class ValueStore(metaclass=PoolMeta):
    __name__ = 'cashbook.values'

    @classmethod
    def _maintenance_fields(cls):
        """ add fields to update job
        """
        result = super(ValueStore, cls)._maintenance_fields()
        result.extend([
            'quantity', 'current_value', 'current_value_ref',
            'diff_amount', 'diff_percent', 'current_rate',
            'purchase_amount', 'yield_fee_total', 'yield_dividend_total',
            'yield_sales', 'yield_fee_12m', 'yield_dividend_12m',
            'yield_sales_12m'])
        return result

# end ValueStore
