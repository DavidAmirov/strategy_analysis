import backtrader as bt

from .base import BaseStrategy


class MAStrategy(BaseStrategy):
    '''Пересечение цены МА.'''
    
    params = (
        ('SMAperiod', 200),
    )

    def __init__(self):
        '''Инициализация торговой системы.'''
        self.DataClose = self.datas[0].close
        self.DataHigh = self.datas[0].high
        self.DataLow = self.datas[0].low
        self.Volume = self.datas[0].volume
        self.Order = None  # Заявка
        self.sma = bt.indicators.MovingAverageSimple(self.datas[0], period=self.params.SMAperiod)

    def next(self):
        '''Приход нового бара'''
        self.log(f'Цена закрытия={self.DataClose[0]:.2f}')
        if self.Order:
            return
        if not self.position:
            isSignalBuy =  self.DataLow[0] < self.sma[0] < self.DataHigh[0] and self.Volume > 70000
            if isSignalBuy:
                self.log('Покупка')
                self.Order = self.buy()
        else:
            isSignalSell = self.DataHigh[0] > self.sma[0] > self.DataLow[0]
            if isSignalSell:
                self.log('Продажа')
                self.Order = self.sell()
