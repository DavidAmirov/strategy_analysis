import datetime

import backtrader as bt

#from strategies.simple_MA import MAStrategy
class MAStrategy(bt.Strategy):
    '''Пересечение цены МА.'''
    
    params = (
        ('SMAperiod', 200),
    )


    def log(self, txt, dt=None):
        '''Вывод строки с датой на конслоь'''
        dt = dt or self.datas[0].datetime.date(0)  # Заданная дата или дата текущего бара
        print(f'{dt}, {txt}')  # Вывод даты с текстом на консоль

    
    def __init__(self):
        '''Инициализация торговой системы.'''
        self.DataClose = self.datas[0].close
        self.Order = None  # Заявка
        self.sma = bt.indicators.MovingAverageSimple(self.datas[0], period=self.params.SMAperiod)

    
    def notify_order(self, order):
        '''Изменение статуса заявки.'''
        if order.status in [order.Submitted, order.Accepted]:
            return
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(f'Покупка @{order.executed.price:.2f}, Cost={order.executed.value:.2f}, Comm={order.executed.comm:.2f}')
            elif order.issell():
                self.log(f'Продажа @{order.executed.price:.2f}, Cost={order.executed.value:.2f}, Comm={order.executed.comm:.2f}')
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Canceled/Margin/Rejected')
        self.Order = None

    
    def notify_trade(self, trade):
        '''Изменение статуса позиции.'''
        if not trade.isclosed:
            return 
        self.log(f'Закрытие позиции, {trade.pnl:.2f}, {trade.pnlcomm:.2f}')

    
    def next(self):
        '''Приход нового бара'''
        #self.log(f'Цена закрытия={self.DataClose[0]:.2f}')
        if self.Order:
            return
        if not self.position:
            isSignalBuy =  self.DataClose[-1] < self.sma[0] < self.DataClose[0]
            if isSignalBuy:
                self.log('Покупка')
                self.Order = self.buy()
            # isSignalSell = self.DataClose[-1] > self.sma[0] and self.DataClose[0] < self.sma[0]
            # if isSignalSell:
            #     self.log('Продажа')
            #     self.Order = self.sell()
        else:
            isSignalSell = self.DataClose[-1] > self.sma[0] > self.DataClose[0]
            if isSignalSell:
                self.log('Продажа')
                self.Order = self.sell()
            # isSignalBuy = self.DataClose[-1] > self.sma[0] and self.DataClose[0] < self.sma[0]
            # if isSignalBuy:
            #     self.log('Покупка')
            #     self.Order = self.buy()

if __name__ == '__main__':
    cerebro = bt.Cerebro()  # Движок backtrader
    cerebro.addstrategy(MAStrategy, SMAperiod=200)
    cerebro.broker.setcash(100000)
    data = bt.feeds.GenericCSVData(
        dataname='Data\TQBR.SBER_D1.txt',
        separator='\t',
        dtformat='%d.%m.%Y %H:%M',
        #tmformat= '%H:%M',
        fromdate=datetime.datetime(2011, 1, 25),
        todate=datetime.datetime(2023, 9, 1),
        openinterest = None
    )
    cerebro.adddata(data)
    cerebro.addsizer(bt.sizers.FixedSize, stake=50)
    cerebro.broker.setcommission(commission=0.001)
    print(f'Стартовый капитал: {cerebro.broker.getvalue():.2f}')
    cerebro.run()  # Запуск торговой системы
    print(f'Конечный капитал: {cerebro.broker.getvalue():.2f}')
    cerebro.plot()