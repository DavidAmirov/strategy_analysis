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
        self.crossover = bt.ind.CrossOver(self.sma1, self.sma2)
     
    def next(self):
        '''Приход нового бара'''
        self.log(f'Цена закрытия={self.DataClose[0]:.2f}')
        if self.Order:
            return
        if not self.position:
            isSignalBuy = self.crossover > 0 
            if isSignalBuy:
                self.log('Покупка')
                self.Order = self.buy()
        else:
            isSignalSell = self.crossover < 0
            if isSignalSell:
                self.log('Продажа')
                self.Order = self.sell()

