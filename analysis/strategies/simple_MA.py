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
        self.Order = None  # Заявка
        self.sma = bt.indicators.MovingAverageSimple(self.datas[0], period=self.params.SMAperiod)

    def next(self):
        '''Приход нового бара'''
        self.log(f'Цена закрытия={self.DataClose[0]:.2f}')
        if self.Order:
            return
        if not self.position:
            isSignalBuy =  self.DataClose[-1] < self.sma[0] < self.DataClose[0]
            if isSignalBuy:
                self.log('Покупка')
                self.Order = self.buy()
        else:
            isSignalSell = self.DataClose[-1] > self.sma[0] > self.DataClose[0]
            if isSignalSell:
                self.log('Продажа')
                self.Order = self.sell()
