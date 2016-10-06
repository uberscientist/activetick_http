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
        print('\nquoteStream:\n', 'No test.')
        return True
        stream = at.quoteStream(('NUGT', 'DUST'))
        for tick in stream:
            print(tick)

    def test_barData(self):
        df = at.barData('INTC', historyType='I', beginTime=datetime(2016, 9, 28)).head()
        print('\nbarData:\n', tabulate(df, headers='keys', tablefmt='grid'))
        return True

    def test_tickData(self):

        beginTime = datetime(2016, 9, 28, 9, 30)
        endTime = datetime(2016, 9, 28, 9, 31)
        # df = at.tickData('GDX', trades=True, quotes=False, beginTime=beginTime,
        #                  endTime=endTime).head()

        # np.datetime64 begin and end type should work
        df = at.tickData('NUGT', trades=False, quotes=True, beginTime=np.datetime64(beginTime),
                         endTime=np.datetime64(endTime))

        print('\ntickData:\n', tabulate(df, headers='keys', tablefmt='grid'))

    def test_optionChain(self):
        df = at.optionChain('SPY').head()
        print('\noptionChain:\n', tabulate(df, headers=[''], tablefmt='grid'))
        return True
