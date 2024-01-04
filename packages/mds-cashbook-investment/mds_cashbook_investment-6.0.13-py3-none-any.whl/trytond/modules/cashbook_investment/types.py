# -*- coding: utf-8 -*-
# This file is part of the cashbook-module from m-ds for Tryton.
# The COPYRIGHT file at the top level of this repository contains the
# full copyright notices and license terms.

from trytond.i18n import gettext
from trytond.pool import PoolMeta


class Type(metaclass=PoolMeta):
    __name__ = 'cashbook.type'

    @classmethod
    def get_sel_feature(cls):
        """ get feature-modes
        """
        l1 = super(Type, cls).get_sel_feature()
        l1.append(('asset', gettext('cashbook_investment.msg_btype_asset')))
        return l1

# end Type
