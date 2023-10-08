import datetime

import backtrader as bt
from strategies.MacdMARsi import MacdMARsi
from strategies.twoMA import twoMA
from strategies.simple_MA import MAStrategy
from strategies.mystrategy import MyStrategy


if __name__ == '__main__':
    cerebro = bt.Cerebro()  # Движок backtrader
    cerebro.addstrategy(twoMA, SMAperiod1=10, SMAperiod2=40)      # (twoMA, SMAperiod1=50, SMAperiod2=120)     MacdMARsi, SMAperiod=200
    cerebro.broker.setcash(100000)
    data = bt.feeds.GenericCSVData(
        dataname='Data\TQBR.SBER_M60.txt',
        datetime=0,
        timeframe=bt.TimeFrame.Minutes,  # для минутнах таймфреймов
        separator='\t',
        dtformat='%d.%m.%Y %H:%M',
        tmformat='%H:%M',
        fromdate=datetime.datetime(2022, 1,  14),
        todate=datetime.datetime(2023, 9, 28),
        openinterest = -1,   
    )
    cerebro.adddata(data)
    cerebro.addsizer(bt.sizers.PercentSizer, percents=50)  #bt.sizers.FixedSize, stake=50   bt.sizers.PercentSizer, percents=50
    cerebro.broker.setcommission(commission=0.001)
    print(f'Стартовый капитал: {cerebro.broker.getvalue():.2f}')
    cerebro.run()  # Запуск торговой системы
    print(f'Конечный капитал: {cerebro.broker.getvalue():.2f}')
    cerebro.plot()