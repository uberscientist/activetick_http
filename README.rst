===============
activetick_http
===============
Python module that connects to ActiveTick HTTP proxy and supplies Pandas DataFrames.
Requires requests for the quoteStream, and redis for caching.

Currently unstable, may end up changing the methods from camelCase to pep8 snake_case.

tests run using ``pytest``

===========
How to use:
===========
Run the
HTTP proxy supplied by ActiveTick_
and instantiate ActiveTick, the defaults are shown with a Redis cache enabled::

    from activetick_http import ActiveTick

    # Import the StrictRedis client to enable local persistent caching
    from redis import StrictRedis

    # ActiveTick initialized with Redis caching enabled (requires Redis)
    at = ActiveTick(host='127.0.0.1', port=5000, cache=StrictRedis(host='127.0.0.1'))

From the ActiveTick instance we have access to all the functionality provided by the HTTP proxy with the following \
methods:

.. _ActiveTick: http://www.activetick.com/activetick/contents/PersonalServicesDataAPIDownload.aspx

=========
quoteData
=========
``quoteData(symbols, fields)``

Returns instantaneous quote information (fields) on symbols
check `quote_fields.py` for available options.::

    fields = ['LastPrice', 'BidPrice', 'AskPrice']
    df = at.quoteData(('SPY', 'TLT', 'TVIX'), fields)
    print(df[fields].head())

+------+-------------+------------+------------+
|      |   LastPrice |   BidPrice |   AskPrice |
+======+=============+============+============+
| SPY  |      216.3  |     216.46 |     216.55 |
+------+-------------+------------+------------+
| TLT  |      137.51 |     137.02 |     137.5  |
+------+-------------+------------+------------+
| TVIX |       18.15 |      18.2  |      18.25 |
+------+-------------+------------+------------+

===========
quoteStream
===========
``quoteStream(symbols)``

Returns a live updated quote stream iterator::

    stream = at.quoteStream(('NUGT','DUST'))
    for tick in stream:
        print(tick)

TODO: example df

=======
barData
=======
``barData(symbol, historyType='I', intradayMinutes=60, beginTime=datetime, endTime=datetime)``

Returns OHLCV data for singular symbol::

    df = at.barData('INTC', historyType='I', beginTime=datetime(datetime.now().year, 9, 27))
    print(df.head())

+---------------------+--------+--------+-------+---------+-------------+
|                     |   open |   high |   low |   close |      volume |
+=====================+========+========+=======+=========+=============+
| 2016-09-28 09:00:00 | 37.52  |  37.52 | 37.25 |  37.395 | 1.79294e+06 |
+---------------------+--------+--------+-------+---------+-------------+
| 2016-09-28 10:00:00 | 37.4   |  37.46 | 37.27 |  37.31  | 1.59818e+06 |
+---------------------+--------+--------+-------+---------+-------------+
| 2016-09-28 11:00:00 | 37.31  |  37.32 | 37.15 |  37.28  | 1.32702e+06 |
+---------------------+--------+--------+-------+---------+-------------+
| 2016-09-28 12:00:00 | 37.28  |  37.32 | 37.2  |  37.27  | 2.39398e+06 |
+---------------------+--------+--------+-------+---------+-------------+
| 2016-09-28 13:00:00 | 37.275 |  37.39 | 37.22 |  37.37  | 1.23249e+06 |
+---------------------+--------+--------+-------+---------+-------------+

========
tickData
========
``tickData(symbol, trades=False, quotes=True, beginTime=datetime, endTime=dateime)``
Returns historical tick level quote and trade data for a symbol::

    df = at.tickData('GDX', trades=True, quotes=False)
    print(df.head())

+----------------------------+--------+--------+---------+---------+---------+---------+---------+---------+
|                            | type   |   last |   lastz | lastx   |   cond1 |   cond2 |   cond3 |   cond4 |
+============================+========+========+=========+=========+=========+=========+=========+=========+
| 2016-09-28 09:30:00.091000 | T      |  26.27 |   52073 | P       |       0 |       0 |      17 |       0 |
+----------------------------+--------+--------+---------+---------+---------+---------+---------+---------+
| 2016-09-28 09:30:00.091000 | T      |  26.27 |   52073 | P       |      16 |       0 |       0 |       0 |
+----------------------------+--------+--------+---------+---------+---------+---------+---------+---------+
| 2016-09-28 09:30:00.182000 | T      |  26.25 |     211 | T       |       0 |      12 |       0 |       0 |
+----------------------------+--------+--------+---------+---------+---------+---------+---------+---------+
| 2016-09-28 09:30:00.184000 | T      |  26.25 |      89 | T       |      37 |      12 |      14 |       0 |
+----------------------------+--------+--------+---------+---------+---------+---------+---------+---------+
| 2016-09-28 09:30:00.185000 | T      |  26.25 |     500 | T       |       0 |      12 |      14 |       0 |
+----------------------------+--------+--------+---------+---------+---------+---------+---------+---------+

===========
optionChain
===========
``optionChain(symbol)``

Returns the symbols making up the optionchain for the underlying::

    df = at.optionChain('SPY')
    print(df.head())

+----+------------------------------+
|    |                              |
+====+==============================+
|  0 | OPTION:SPY---161014P00186000 |
+----+------------------------------+
|  1 | OPTION:SPY---161012C00197000 |
+----+------------------------------+
|  2 | OPTION:SPY---161014C00187000 |
+----+------------------------------+
|  3 | OPTION:SPY---161014P00192000 |
+----+------------------------------+
|  4 | OPTION:SPY---161012P00193000 |
+----+------------------------------+
