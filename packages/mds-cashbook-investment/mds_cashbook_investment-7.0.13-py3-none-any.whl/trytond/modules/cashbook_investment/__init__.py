# -*- coding: utf-8 -*-
# This file is part of the cashbook-module from m-ds for Tryton.
# The COPYRIGHT file at the top level of this repository contains the
# full copyright notices and license terms.

from trytond.pool import Pool
from .types import Type
from .book import Book
from .reconciliation import Reconciliation
from .line import Line
from .splitline import SplitLine
from .assetsetting import AssetSetting
from .asset import AssetRate
from .valuestore import ValueStore


def register():
    Pool.register(
        AssetRate,
        Type,
        Book,
        Line,
        SplitLine,
        Reconciliation,
        AssetSetting,
        ValueStore,
        module='cashbook_investment', type_='model')
