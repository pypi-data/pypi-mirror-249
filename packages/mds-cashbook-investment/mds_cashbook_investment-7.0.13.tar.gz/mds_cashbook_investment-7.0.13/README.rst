mds-cashbook-investment
=======================
Tryton module to add investment accounts to cashbook.

Install
=======

pip install mds-cashbook-investment

Requires
========
- Tryton 7.0

How to
======

The module extends the cash accounts in mds-cashbook with
the ability to store quantities. You are free to choose the
unit of measurement. It uses the current price data
from the mds-investment module.
You can monitor trading fees, dividends and sales profits.

Changes
=======

*7.0.13 - 03.01.2024*

- fix: sorting/searcher of field yield-balance

*7.0.12 - 31.12.2023*

- remove caching
- add worker-based precalculation of cashbook-values
- add columns to cashbook list/tree view

*7.0.11 - 06.12.2023*

- compatibility to Tryton 7.0
