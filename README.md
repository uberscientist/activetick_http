activetick_http
=================
Python module that connects to ActiveTick HTTP proxy and supplies Pandas DataFrames.
Requires requests for the quoteStream, and redis for caching.

tests written using `pytest`

How to use:
--------------
Run the
[HTTP proxy supplied by ActiveTick](http://www.activetick.com/activetick/contents/PersonalServicesDataAPIDownload.aspx)
 and instantiate ActiveTick, the defaults are shown with a Redis cache enabled:

```python
from activetick_http import ActiveTick

# Import the StrictRedis client to enable local persistent caching
from redis import StrictRedis

# ActiveTick initialized with Redis caching enabled (requires Redis)
at = ActiveTick(host='127.0.0.1', port=5000, cache=StrictRedis(host='127.0.0.1'))
```

From the ActiveTick instance we have access to all the functionality provided by the HTTP proxy with the following
 methods:

quoteData(*symbols, fields*)
-----------
Returns instantaneous quote information (fields) on symbols
check `quote_fields.py` for availiable options.

```python
fields = ['LastPrice', 'BidPrice', 'AskPrice']
df = at.quoteData(('SPY', 'TLT', 'TVIX'), fields)
print(df[fields])
```
|      |   LastPrice |   BidPrice |   AskPrice |
|:-----|------------:|-----------:|-----------:|
| SPY  |      216.64 |     216.6  |     216.62 |
| TLT  |      138.4  |     138.25 |     138.44 |
| TVIX |       17.49 |      17.48 |      17.51 |

quoteStream(*symbols*)
------------
Returns a live updated quote stream iterator

```python
stream = at.quoteStream(('NUGT','DUST'))
for tick in stream:
    print(tick)
```
|    | symbol   |   cond | bid_ex   | ask_ex   |   bid |   ask |   bidz |   askz | datetime                   |
|:---|:---------|-------:|:---------|:---------|------:|------:|-------:|-------:|:---------------------------|
| Q  | DUST     |      0 | P        | P        | 32.15 | 32.18 |      1 |      5 | 2016-09-28 14:16:32.758000 |

|    | symbol   |   flags |   cond1 |   cond2 |   cond3 |   cond4 | last_ex   |   last |   lastz | datetime                   |
|:---|:---------|--------:|--------:|--------:|--------:|--------:|:----------|-------:|--------:|:---------------------------|
| T  | NUGT     |       3 |       0 |      14 |       0 |       0 | P         |  19.86 |     101 | 2016-09-28 14:16:33.518000 |               |

barData(*symbol, historyType='I', intradayMinutes=60, beginTime=datetime, endTime=datetime*)
----------
Returns OHLCV data for singular symbol

```python
intc_hourly = at.barData('INTC', historyType='I', beginTime=datetime(datetime.now().year, 9, 27))
print(intc_hourly)
```

|                     |   open |   high |    low |   close |           volume |
|:--------------------|-------:|-------:|-------:|--------:|-----------------:|
| 2016-09-27 09:00:00 | 36.9   | 36.97  | 36.63  | 36.965  |      2.49561e+06 |
| 2016-09-27 10:00:00 | 36.965 | 37.05  | 36.735 | 36.765  |      2.54651e+06 |
| 2016-09-27 11:00:00 | 36.77  | 36.95  | 36.76  | 36.935  |      2.27909e+06 |
| 2016-09-27 12:00:00 | 36.936 | 37.98  | 36.89  | 36.995  |      2.67261e+06 |
| 2016-09-27 13:00:00 | 36.995 | 37.1   | 36.94  | 37.06   |      1.48077e+06 |
| 2016-09-27 14:00:00 | 37.065 | 37.105 | 37     | 37.055  |      1.70914e+06 |
| 2016-09-27 15:00:00 | 37.055 | 37.22  | 37.04  | 37.185  |      4.27286e+06 |
| 2016-09-27 16:00:00 | 37.185 | 37.185 | 37.18  | 37.18   |      1.31793e+06 |
| 2016-09-28 09:00:00 | 37.52  | 37.52  | 37.25  | 37.395  |      1.79294e+06 |
| 2016-09-28 10:00:00 | 37.4   | 37.46  | 37.27  | 37.31   |      1.59818e+06 |
| 2016-09-28 11:00:00 | 37.31  | 37.32  | 37.22  | 37.2263 | 488536           |

tickData(*symbol, trades=False, quotes=True, beginTime=datetime, endTime=dateime*)
--------
Returns historical tick level quote and trade data for a symbol

```python
df = at.tickData('TWTR', trades=True, quotes=True)
print(df)
```

|                            |    ask | askx   |   askz |   bid | bidx   |   bidz |   cond |   cond1 |   cond2 |   cond3 |   cond4 |     last | lastx   |   lastz | type   |
|:---------------------------|-------:|:-------|-------:|------:|:-------|-------:|-------:|--------:|--------:|--------:|--------:|---------:|:--------|--------:|:-------|
| 2016-09-28 12:40:57.033000 | nan    | nan    |    nan | nan   | nan    |    nan |    nan |       0 |       0 |       0 |       0 |  22.905  | D       |     100 | T      |
| 2016-09-28 12:40:57.039000 | nan    | nan    |    nan | nan   | nan    |    nan |    nan |       0 |       0 |       0 |       0 |  22.9044 | D       |     100 | T      |
| 2016-09-28 12:40:57.057000 | nan    | nan    |    nan | nan   | nan    |    nan |    nan |       0 |       0 |       0 |       0 |  22.9044 | D       |     800 | T      |
| 2016-09-28 12:40:57.090000 | nan    | nan    |    nan | nan   | nan    |    nan |    nan |       0 |       0 |       0 |       0 |  22.905  | D       |     700 | T      |
| 2016-09-28 12:40:57.290000 | nan    | nan    |    nan | nan   | nan    |    nan |    nan |       0 |       0 |       0 |       0 |  22.905  | K       |     100 | T      |
| 2016-09-28 12:40:57.490000 |  22.91 | N      |     35 |  22.9 | N      |     14 |      0 |     nan |     nan |     nan |     nan | nan      | nan     |     nan | Q      |
| 2016-09-28 12:40:57.491000 |  22.91 | N      |     34 |  22.9 | N      |     14 |      0 |     nan |     nan |     nan |     nan | nan      | nan     |     nan | Q      |
| 2016-09-28 12:40:57.501000 |  22.91 | N      |     32 |  22.9 | N      |     15 |      0 |     nan |     nan |     nan |     nan | nan      | nan     |     nan | Q      |
| 2016-09-28 12:40:57.501000 |  22.91 | N      |     32 |  22.9 | N      |     14 |      0 |     nan |     nan |     nan |     nan | nan      | nan     |     nan | Q      |
| 2016-09-28 12:40:57.501000 | nan    | nan    |    nan | nan   | nan    |    nan |    nan |       0 |       0 |       0 |       0 |  22.9    | P       |     100 | T      |

optionChain(*symbol*)
----------
Returns the symbols making up the optionchain for the underlying

```python
df = at.optionChain('SPXW')
print(df)
```

|-|-|
|-----:|:-----------------------------|
|    0 | OPTION:SPXW--161230P02215000 |
|    1 | OPTION:SPXW--161111C02315000 |
|    2 | OPTION:SPXW--161130P02265000 |
|    3 | OPTION:SPXW--161230C02135000 |
|    4 | OPTION:SPXW--161130C02055000 |
|    5 | OPTION:SPXW--161230P02205000 |
|    6 | OPTION:SPXW--161130P02045000 |
|    7 | OPTION:SPXW--161130C02265000 |
|    8 | OPTION:SPXW--161230P02135000 |
|    9 | OPTION:SPXW--161230C02205000 |
|   10 | OPTION:SPXW--161230C02165000 |
|  ... | ...                          |
