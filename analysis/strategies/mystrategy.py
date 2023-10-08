import backtrader as bt

from .base import BaseStrategy


class MyStrategy(BaseStrategy):

    params = (
        ('SMAperiod1', 10),
        #('SMAperiod2', 40),
        #('SMAperiod3', 80)
    )
    
    def __init__(self):
        '''Инициализация торговой системы.'''
        self.DataClose = self.datas[0].close
        self.DataHigh = self.datas[0].high
        self.DataLow = self.datas[0].low
        self.Volume = self.datas[0].volume
        self.Order = None
        self.sma1 = bt.indicators.MovingAverageSimple(self.datas[0], period=self.params.SMAperiod1)
        #self.sma2 = bt.indicators.MovingAverageSimple(self.datas[0], period=self.params.SMAperiod2)
        #self.sma3 = bt.indicators.MovingAverageSimple(self.datas[0], period=self.params.SMAperiod3)
        self.macd = bt.indicators.MACD(self.datas[0])
        self.rsi = bt.indicators.RelativeStrengthIndex(self.datas[0])
    
    def next(self):
        '''Приход нового бара'''
        #self.log(f'Цена закрытия={self.DataClose[0]:.2f}')
        if self.Order:
            return
        if not self.position:

            isSignalBuy = self.sma1[0] < self.DataHigh[0] and self.macd.macd[-1] < self.macd.signal[-1] and self.macd.macd[0] > self.macd.signal[0] 
            if isSignalBuy:
                self.log(f'Покупка  {self.macd.macd[-1]}   {self.macd.signal[-1]} {self.macd.macd[0]}   {self.macd.signal[0]}')
                self.Order = self.buy()

        else:
            isSignalBuy = self.rsi.rsi[-1] < 50 < self.rsi.rsi[0] or self.rsi.rsi[-1] < 70 < self.rsi.rsi[0] or self.rsi.rsi[-1] > 50 > self.rsi.rsi[0]
            if isSignalBuy:
                self.log('Продажа')
                self.Order = self.sell()

