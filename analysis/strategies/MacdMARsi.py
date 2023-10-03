import backtrader as bt

from .base import BaseStrategy

class MacdMARsi(BaseStrategy):
    params = (
        ('SMAperiod', 100),
        #('Macdperiod', 12)
    )

    def __init__(self):
        '''Инициализация торговой системы.'''
        self.DataClose = self.datas[0].close
        self.DataHigh = self.datas[0].high
        self.Datalow = self.datas[0].low
        self.Order = None
        self.sma = bt.indicators.MovingAverageSimple(self.datas[0], period=self.params.SMAperiod)
        self.macd = bt.indicators.MACD(self.datas[0])
        self.rsi = bt.indicators.RelativeStrengthIndex(self.datas[0])
    
    def next(self):
        '''Приход нового бара'''
        self.log(f'Цена закрытия={self.DataClose[0]:.2f}')
        if self.Order:
            return
        if not self.position:
            macd_signal1 = self.macd.macd[-1] < self.macd.signal[0] and self.macd.macd[0] > self.macd.signal[0] and self.macd.macd < 0
            macd_signal2 = self.macd.macd[-2] < self.macd.signal[-1] and self.macd.macd[-1] > self.macd.signal[-1] and self.macd.macd < 0
            # macd_signal3 = self.macd.macd[-3] < self.macd.signal[-2] and self.macd.macd[-2] > self.macd.signal[-2] and self.macd.macd < 0
            # macd_signal4 = self.macd.macd[-4] < self.macd.signal[-3] and self.macd.macd[-3] > self.macd.signal[-3] and self.macd.macd < 0
            rsi_signal = self.rsi.rsi[-1] < 30 and self.rsi.rsi[0] > 30 or self.rsi.rsi[-1] < 50 and self.rsi.rsi[0] >= 50
            isSignalBuy = macd_signal1 or macd_signal2 and rsi_signal 
            if isSignalBuy:
                self.log('Покупка')
                self.Order = self.buy()

        else:
            macd_signal1 = self.macd.macd[-1] > self.macd.signal[0] and self.macd.macd[0] < self.macd.signal[0] and self.macd.macd > 0
            macd_signal2 = self.macd.macd[-2] > self.macd.signal[-1] and self.macd.macd[-1] < self.macd.signal[-1] and self.macd.macd > 0
            # macd_signal3 = self.macd.macd[-3] > self.macd.signal[-2] and self.macd.macd[-2] < self.macd.signal[-2] and self.macd.macd > 0
            # macd_signal4 = self.macd.macd[-4] > self.macd.signal[-3] and self.macd.macd[-3] < self.macd.signal[-3] and self.macd.macd > 0
            rsi_signal = self.rsi.rsi[-1] > 70 and self.rsi.rsi[0] < 70 or self.rsi.rsi[-1] > 50 and self.rsi.rsi[0] <= 50
            isSignalBuy = macd_signal1 or macd_signal2 and rsi_signal 
            if isSignalBuy:
                self.log('Продажа')
                self.Order = self.sell()
