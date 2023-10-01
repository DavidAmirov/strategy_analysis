import datetime
import backtrader as bt


class MAStrategy(bt.Strategy):
    '''Пересечение цены МА.'''
    
    params = (
        ('SMAperiod', 200)
    )


    def log(self, txt, dt=None):
        '''Вывод строки с датой на конслоь'''
        dt = dt or self.datas[0].datetime.date(0)  # Заданная дата или дата текущего бара
        print(f'{dt.isoformat()}, {txt}')  # Вывод даты с текстом на консоль

    
    def __init__(self):
        '''Инициализация торговой системы.'''
        self.DataClose = self.datas[0].close
        self.order = None  # Заявка
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
        self.order = None

    
    def notify_trade(self, trade):
        '''Изменение статуса позиции.'''
        if not trade.isclosed:
            return 
        self.log(f'Закрытие позиции, {trade.pnl:.2f}, {trade.pnlcomm:.2f}')

    
    def next(self):
        '''Приход нового бара'''
        self.log(f'Цена закрытия={self.DataClose[0]:.2f}')
        if self.Order:
            return
        if not self.position:
            isSignalBuy = self.DataClose[0] > self.sma[0]
            if isSignalBuy:
                self.log('Покупка')
                self.order = self.buy()
        else:
            isSignalSell = self.DataClose[0] < self.sma[0]
            if isSignalSell:
                self.log('Продажа')
                self.order = self.sell()