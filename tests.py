df = at.quoteData(('SPY', 'GDX', 'TVIX'), fields)
print("quoteData: ")
print(df)

stream = at.quoteStream(('NUGT', 'DUST'))
for tick in stream:
    print(tabulate(tick, headers='keys', tablefmt='pipe'))

intc_hourly = at.barData('INTC', historyType='I', beginTime=datetime(datetime.now().year, 9, 27))
print(tabulate(intc_hourly, headers='keys', tablefmt='pipe'))

df = at.tickData('TWTR', trades=True, quotes=True)
print(tabulate(df.head(n=10), headers='keys', tablefmt='pipe'))

df = tabulate(at.optionChain('USO'))