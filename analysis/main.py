import datetime

import backtrader as bt
from strategies.MacdMARsi import MacdMARsi
from strategies.twoMA import twoMA
from strategies.simple_MA import MAStrategy

if __name__ == '__main__':
    cerebro = bt.Cerebro()  # Движок backtrader
    cerebro.addstrategy(MacdMARsi, SMAperiod=200)      # (twoMA, SMAperiod1=50, SMAperiod2=120)
    cerebro.broker.setcash(100000)
    data = bt.feeds.GenericCSVData(
        dataname='Data\TQBR.SBER_M15.txt',
        separator='\t',
        dtformat='%d.%m.%Y %H:%M',
        #tmformat= '%H:%M',
        fromdate=datetime.datetime(2015, 1, 25),
        todate=datetime.datetime(2023, 9, 1),
        openinterest = None
    )
    cerebro.adddata(data)
    cerebro.addsizer(bt.sizers.PercentSizer, percents=50)  #bt.sizers.FixedSize, stake=50   bt.sizers.PercentSizer, percents=50
    cerebro.broker.setcommission(commission=0.001)
    print(f'Стартовый капитал: {cerebro.broker.getvalue():.2f}')
    cerebro.run()  # Запуск торговой системы
    print(f'Конечный капитал: {cerebro.broker.getvalue():.2f}')
    cerebro.plot()