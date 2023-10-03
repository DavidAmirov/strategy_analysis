import backtrader as bt

from .base import BaseStrategy


class twoMA(BaseStrategy):
    '''Пересечение цены МА.'''
    
    params = (
        ('SMAperiod1', 10),
        ('SMAperiod2', 40),
    )

    def __init__(self):
        '''Инициализация торговой системы.'''
        self.DataClose = self.datas[0].close
        self.DataHigh = self.datas[0].high
        self.Datalow = self.datas[0].low
        self.Order = None
        self.sma1 = bt.indicators.MovingAverageSimple(self.datas[0], period=self.params.SMAperiod1)
        self.sma2 = bt.indicators.MovingAverageSimple(self.datas[0], period=self.params.SMAperiod2)
     
    def next(self):
        '''Приход нового бара'''
        self.log(f'Цена закрытия={self.DataClose[0]:.2f}')
        if self.Order:
            return
        if not self.position:
            isSignalBuy =  self.sma1[-1] < self.sma2[-1] and self.sma1[0] >= self.sma2[0] and self.DataHigh[0] > self.sma1[0]
            if isSignalBuy:
                self.log('Покупка')
                self.Order = self.buy()

        else:
            isSignalSell = self.sma1[-1] > self.sma2[-1] and self.sma1[0] <= self.sma2[0] and self.Datalow[0] < self.sma1[0]
            if isSignalSell:
                self.log('Продажа')
                self.Order = self.sell()
