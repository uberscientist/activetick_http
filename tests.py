from redis import StrictRedis
from activetick_http import ActiveTick
from datetime import datetime
import numpy as np

from tabulate import tabulate

at = ActiveTick(cache=StrictRedis(host='127.0.0.1'))
class TestActiveTick():
    def test_quoteData(self):
        fields = ['LastPrice', 'BidPrice', 'AskPrice']
        df = at.quoteData(['SPY', 'TLT', 'TVIX'], fields)
        print('quoteData:\n', tabulate(df[fields], headers='keys', tablefmt='grid'))
        return True

    def test_quoteStream(self):
        print('\nquoteStream showing 3 ticks (timeout in 2 seconds for weekends tests):\n')
        stream = at.quoteStream(('SPY', 'VXX'), timeout=2)
        i = 0
        for tick in stream:
            if i < 3:
                i += 1
                print(tabulate(tick, headers='keys', tablefmt='grid'))
            else:

                # How to close the quoteStream
                at.stream_.connection.close()
                return True

    def test_barData(self):
        df = at.barData('INTC', historyType='I', beginTime=datetime(2016, 9, 28)).head()
        print('\nbarData:\n', tabulate(df.head(), headers='keys', tablefmt='grid'))
        return True

    def test_tickData(self):

        print('tickData:')
        beginTime = datetime(2016, 9, 28, 9, 30)
        endTime = datetime(2016, 9, 28, 9, 31)
        df = at.tickData('GDX', trades=True, quotes=False, beginTime=beginTime,
                          endTime=endTime).head()
        print('\nPlain date query:\n', tabulate(df.head(), headers='keys', tablefmt='grid'))

        # np.datetime64 begin and end type should work
        df = at.tickData('NUGT', trades=False, quotes=True, beginTime=np.datetime64(beginTime),
                         endTime=np.datetime64(endTime))
        print('\datetime64 query:\n', tabulate(df.head(), headers='keys', tablefmt='grid'))

        #Shouldn't crash if there's no data, AT returns a 0
        df = at.tickData('SPY',  trades=False, quotes=True, beginTime=datetime(2016, 9, 13, 9, 30),
                         endTime=datetime(2016, 9, 13, 9, 31))
        print('\nno data:\n', tabulate(df.head(), headers='keys', tablefmt='grid'))

    def test_optionChain(self):
        df = at.optionChain('SPY')
        print('\noptionChain:\n', tabulate(df.head(), headers=[''], tablefmt='grid'))
        return True
