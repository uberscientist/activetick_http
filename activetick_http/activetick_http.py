from quote_fields import quote_definitions, quote_dtypes
from io import StringIO
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from requests import Session

# TODO look into read_csv use_cols option for speedups

class ActiveTick:
    def __init__(self, host='127.0.0.1', port=5000):

        # Active tick HTTP proxy config
        self.host = host
        self.port = port
        self.r = Session()

        self._date_fmt = '%Y%m%d%H%M%S'

    def _format_symbols(self, symbols):
        """
        symbols - string (returns unchanged) or list of symbols to concat with + symbols (string, list)
        Formats list of symbols for ActiveTick URL
        :param symbols:
        :return:
        String
        """
        if not isinstance(symbols, str):
            symbols = '+'.join(symbols)
        return symbols

    def _date_parser(self, date_format):
        """
        Date parser function factory for pandas csv parsing of ActiveTick data
        :param date_format:
        Format used for parsing date (string)
        :return:
        (list of datetimes)
        """
        def date_parser(dates):
            return [ datetime.strptime(date, date_format) for date in dates ]
        return date_parser

    def quoteData(self, symbols, quoteFields):
        """
        symbols - Symbol (or iterable of multiple symbols) for contracts, ie SPY, AAPL--130308C00440000 (string, iter)
        quote_fields - List of all fields of interest (string, list)

        # Example:
        # look to quoteFields.py for the lookup table used and available fields

        atClient.quoteData('SPY', ['LastPrice' , 'BidSize', 'AskSize'])

        # returns pandas DataFrame with columns named

        :return:
        pandas.DataFrame() indexed on the symbol column with columns with requested quoteFields
        with extra status meta data regarding the request and symbols, to just get a DataFrame
        with the requested fields quoteData('SPY', fields)[fields]
        """
        print('quotefield:', quoteFields)
        names = ['symbol', 'symbol_status']
        def __name_fmt(names, field):
            names += ["{f}_field_id".format(f=field),
                      "{f}_status".format(f=field),
                      "{f}_datatype".format(f=field),
                      "{f}".format(f=field)]
            return names

        if not isinstance(quoteFields, str):

            # Create column names from quoteFields
            for field in quoteFields:
                names = __name_fmt(names, field)

            # TODO: Declare specific dtypes for each column in names
            # Translate from human readable quoteFields to IDs
            quoteFields = map(lambda field: quote_definitions[field], quoteFields)
            quoteFields = '+'.join(quoteFields)
        else:

            # Only one quoteField as string
            names = __name_fmt(names, quoteFields)
            quoteFields = quote_definitions[quoteFields]

        url = "http://{host}:{port}/quoteData?symbol={symbols}&field={quoteFields}".format(
            host=self.host,
            port=self.port,
            symbols=self._format_symbols(symbols),
            quoteFields=quoteFields
        )

        # GET request is made and the CSV is read into a Pandas DataFrame
        df = pd.read_csv(url, header=None, names=names, index_col='symbol')
        return df

    def quoteStream(self, symbols):
        """
        symbols - string or iter of symbols

        # Example
        # res is an instance of requests iter_lines()
        res = at.quoteStream('SPY')
        for quote in res:
            print(quote)

        :return:
        returns lazy iterator see requests iter_lines() that can be looped over to access streaming data
        """
        # TODO: Start, pause, stop quote stream

        def __tickParse(tick):
            tick = tick.decode('utf-8')
            if tick[0] is 'Q':
                names = ['type', 'symbol', 'cond', 'bid_ex', 'ask_ex', 'bid', 'ask', 'bidz', 'askz', 'datetime']
                dtype = {'type': object,
                         'symbol': object,
                         'cond': np.uint8,
                         'bid_ex': object,
                         'ask_ex': object,
                         'bid': np.float32,
                         'ask': np.float32,
                         'bidz': np.uint32,
                         'askz': np.uint32,
                         'datetime': object}
            else:
                names = ['type', 'symbol', 'flags', 'cond1', 'cond2', 'cond3', 'cond4', 'last_ex', 'last', 'lastz',
                         'datetime']
                dtype = {
                    'type': object,
                    'symbol': object,
                    'flags': object,
                    'cond1': np.int8,
                    'cond2': np.int8,
                    'cond3': np.int8,
                    'cond4': np.int8,
                    'last_ex': object,
                    'last': np.float32,
                    'lastz': np.uint32
                }
            date_format = '%Y%m%d%H%M%S%f'
            parse_date = self._date_parser(date_format)

            return pd.read_csv(StringIO(tick), names=names, index_col='type', dtype=dtype,
                               parse_dates=['datetime'], date_parser=parse_date)

        res = self.r.get('http://{host}:{port}/quoteStream?symbol={symbols}'.format(
            host=self.host,
            port=self.port,
            symbols=self._format_symbols(symbols)
        ), stream=True)
        lines = map(__tickParse, res.iter_lines())
        first_line = next(lines)
        return lines

    def barData(self, symbol, historyType='I', intradayMinutes=60,
                beginTime=datetime(datetime.now().year, datetime.now().month, 1), endTime=datetime.now()):
        """
        :param symbol:
         Takes only one symbol, string
        :param historyType:
         Takes 'I', 'D' or 'W' as a string (Intraday 0, Daily 1 or Weekly 0)
        :param intradayMinutes:
         If historyType is 'I' select a bar size: 0 to 60 minutes (int)
        :param beginTime:
         Beginning date for query (datetime)
        :param endTime:
         Ending date for query (datetime)
        :return:
         Pandas DataFrame OHLCV indexed on the datetime
        """
        history_lookup = {
            'I': 0,
            'D': 1,
            'W': 2
        }

        def __getIntradayMinutesAttr():
            # Returns URL segment for intraday minutes if needed
            if historyType is not 'I':
                attr_str = ''
            else:
                attr_str = 'intradayMinutes={intradayMinutes}&'.format(intradayMinutes=str(intradayMinutes))
            return attr_str

        url = 'http://{host}:{port}/barData?symbol={symbol}&historyType={historyType}' \
              '&{intradayMintuesAttr}beginTime={beginTime}&endTime={endTime}'.format(
            host = self.host,
            port = self.port,
            symbol = symbol,
            historyType = history_lookup[historyType],
            intradayMintuesAttr = __getIntradayMinutesAttr(),
            beginTime = datetime.strftime(beginTime, format=self._date_fmt),
            endTime = datetime.strftime(endTime, format=self._date_fmt))

        dtypes = {'datetime': object,
                  'open': np.float32,
                  'high': np.float32,
                  'low': np.float32,
                  'close': np.float32,
                  'volume': np.uint32}

        df = pd.read_csv(url, header=None, names=['datetime', 'open', 'high', 'low', 'close', 'volume'],
                         index_col='datetime', parse_dates=['datetime'], dtype=dtypes)
        return df

    def tickData(self, symbol, trades=False, quotes=True,
                 beginTime=datetime.now() - timedelta(minutes=15), endTime=datetime.now()):
        """
        Gets tick level data in between a time range, limited to returnedin 100,000 quotes/trades at a time
        :param symbol:
        String, ticker for symbol in ActiveTick format
        :param trades:
        Boolean, whether to return trade ticks
        :param quotes:
        Boolean whether to return quote ticks
        :param beginTime:
        datetime beginning of date range
        :param endTime:
        datetime end of date range
        :return:
        """

        url = 'http://{host}:{port}/tickData?symbol={symbol}&trades={trades}' \
              '&quotes={quotes}&beginTime={beginTime}&endTime={endTime}'

        url = url.format(
            host=self.host,
            port=self.port,
            symbol=symbol,
            trades=1,
            quotes=1,
            beginTime=datetime.strftime(beginTime, format=self._date_fmt),
            endTime=datetime.strftime(endTime, format=self._date_fmt)
        )

        q_names = ['type',
                   'bid',
                   'ask',
                   'bidz',
                   'askz',
                   'bidx',
                   'askx',
                   'cond']

        t_names = ['type',
                   'last',
                   'lastz',
                   'lastx',
                   'cond1',
                   'cond2',
                   'cond3',
                   'cond4']

        tick_date_fmt = '%Y%m%d%H%M%S%f'
        date_parser = self._date_parser(tick_date_fmt)

        df = pd.read_csv(url, header=None,
                         engine='c',
                         index_col=1,
                         parse_dates=[1],
                         date_parser=date_parser)

        df.index.name = 'datetime'

        trades_df = df[df[0] == 'T'].copy()
        trades_df.columns = t_names

        trades_df.loc[:, 'last'] = trades_df.loc[:, 'last'].astype(np.float32)
        trades_df.loc[:, 'lastz'] = trades_df.loc[:, 'lastz'].astype(np.uint32)
        trades_df.loc[:, ['cond1','cond2','cond3','cond4']] = trades_df.loc[:, ['cond1',
                                                                                'cond2',
                                                                                'cond3',
                                                                                'cond4']].astype(np.uint8)

        quotes_df = df[df[0] == 'Q'].copy()
        quotes_df.columns = q_names

        quotes_df.loc[:, ['bid', 'ask']] = quotes_df.loc[:, ['bid', 'ask']].astype(np.float32)
        quotes_df.loc[:, ['bidz', 'askz']] = quotes_df.loc[:, ['bidz', 'askz']].astype(np.uint32)
        quotes_df.loc[:, 'cond'] = quotes_df.loc[:, 'cond'].astype(np.uint8)

        if trades and quotes:
            df = trades_df.append(quotes_df).sort_index(axis=0)
        elif trades and not quotes:
            df = trades_df
        elif quotes and not trades:
            df = quotes_df
        else:
            df = pd.DataFrame()
        return df

    def optionChain(self, symbol):
        """
        Returns unnamed pandas dataframe of option symbols currently listed for underlying symbol
        :param symbol:
        String, ticker symbol for underlying
        :return:
        Raw unnamed dataframe from ActiveTick
        """
        url = 'http://{host}:{port}/optionChain?symbol={symbol}'.format(
            host=self.host,
            port=self.port,
            symbol=symbol)
        df = pd.read_csv(url)
        return df

if __name__ == '__main__':
    print('ActiveTick Python Module, attaches to ActiveTick HTTP Proxy, returns Pandas DataFrames.')
    # TODO Write/Run tests
