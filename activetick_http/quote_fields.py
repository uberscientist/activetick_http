import numpy as np
"""
Definitions of Active Tick quoteField definitions
We remove the QuoteField prefix, so QuoteFieldSymbol becomes Symbol

This lookup tuple is for
activetick.py : quoteData
"""

DEFINITIONS = ["Symbol",
               "OpenPrice",
               "PreviousClosePrice",
               "ClosePrice",
               "LastPrice",
               "BidPrice",
               "AskPrice",
               "HighPrice",
               "LowPrice",
               "DayHighPrice",
               "DayLowPrice",
               "PreMarketOpenPrice",
               "ExtendedHoursLastPrice",
               "AfterMarketClosePrice",
               "BidExchange",
               "AskExchange",
               "LastExchange",
               "LastCondition",
               "QuoteCondition",
               "LastTradeDateTime",
               "LastQuoteDateTime",
               "DayHighDateTime",
               "DayLowDateTime",
               "LastSize",
               "BidSize",
               "AskSize",
               "Volume",
               "PreMarketVolume",
               "AfterMarketVolume",
               "TradeCount",
               "PreMarketTradeCount",
               "AfterMarketTradeCount",
               "FundamentalEquityName",
               "FundamentalEquityPrimaryExchange"]

DEF_DTYPES = {
    "Symbol": object,
    "OpenPrice": np.float32,
    "PreviousClosePrice": np.float32,
    "ClosePrice": np.float32,
    "LastPrice": np.float32,
    "BidPrice": np.float32,
    "AskPrice": np.float32,
    "HighPrice": np.float32,
    "LowPrice": np.float32,
    "DayHighPrice": np.float32,
    "DayLowPrice": np.float32,
    "PreMarketOpenPrice": np.float32,
    "ExtendedHoursLastPrice": np.float32,
    "AfterMarketClosePrice": np.float32,
    "BidExchange": np.uint16,
    "AskExchange": object,
    "LastExchange": object,
    "LastCondition": np.uint16,
    "QuoteCondition": np.uint16,
    "LastTradeDateTime": object,
    "LastQuoteDateTime": object,
    "DayHighDateTime": object,
    "DayLowDateTime": object,
    "LastSize": np.uint32,
    "BidSize": np.uint32,
    "AskSize": np.uint32,
    "Volume": np.uint32,
    "PreMarketVolume": np.uint32,
    "AfterMarketVolume": np.uint32,
    "TradeCount": np.uint32,
    "PreMarketTradeCount": np.uint32,
    "AfterMarketTradeCount": np.uint32,
    "FundamentalEquityName": object,
    "FundamentalEquityPrimaryExchange": object
}

quote_definitions = {DEFINITIONS[i]: str(i+1) for i in range(0, len(DEFINITIONS))}
quote_dtypes = DEF_DTYPES
