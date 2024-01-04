mds-cashbook-investment
=======================
Tryton module to add investment accounts to cashbook.

Install
=======

pip install mds-cashbook-investment

Requires
========
- Tryton 6.0

How to
======

The module extends the cash accounts in mds-cashbook with
the ability to store quantities. You are free to choose the
unit of measurement. It uses the current price data
from the mds-investment module.
You can monitor trading fees, dividends and sales profits.

Changes
=======

*6.0.13 - 03.01.2024*

- fix: sorting/searcher of field yield-balance

*6.0.12 - 31.12.2023*

- remove caching
- add worker-based precalculation of cashbook-values

*6.0.11 - 06.12.2023*

- code optimized

*6.0.10 - 08.06.2023*

- code optimized

*6.0.9 - 19.04.2023*

- fix: line - exception if add split-lines

*6.0.8 - 17.04.2023*

- fix: line - selection of digits for quantity

*6.0.7 - 05.03.2023*

- updt: optimize queries for speed, optimize caching
- add: trytond.conf-settings

*6.0.6 - 27.02.2023*

- add: caching
- add: performance and yield info

*6.0.5 - 05.02.2023*

- fix: line rewrite values

*6.0.4 - 01.02.2023*

- fix: selection of quantity-uom/digits on line/spitline

*6.0.3 - 30.01.2023*

- add: performance-tab to line-form
- fix: digits of start/end-quantity in reconciliation

*6.0.2 - 28.01.2023*

- fix: transfer between cash-/asset-book with zero quantity
- add: view value/percent on chasbooks with btype=None

*6.0.1 - 21.01.2023*

- works

*6.0.0 - 20.12.2022*

- init
