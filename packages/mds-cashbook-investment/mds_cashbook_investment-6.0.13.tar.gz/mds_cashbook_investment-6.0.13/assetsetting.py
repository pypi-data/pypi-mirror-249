# -*- coding: utf-8 -*-
# This file is part of the cashbook-module from m-ds.de for Tryton.
# The COPYRIGHT file at the top level of this repository contains the
# full copyright notices and license terms.


from trytond.model import ModelSingleton, ModelView, ModelSQL, fields


class AssetSetting(ModelSingleton, ModelSQL, ModelView):
    'Asset setting'
    __name__ = 'cashbook.assetconf'

    fee_category = fields.Many2One(
        string='Fee category',
        model_name='cashbook.category', ondelete='RESTRICT',
        help='Category for fees when trading assets.')
    dividend_category = fields.Many2One(
        string='Dividend category',
        model_name='cashbook.category', ondelete='RESTRICT',
        help='Category for dividend paid out.')
    gainloss_book = fields.Many2One(
        string='Profit/Loss Cashbook',
        model_name='cashbook.book', ondelete='RESTRICT',
        help='Profit and loss on sale of assets are recorded in the cash book.')

# end AssetSetting
