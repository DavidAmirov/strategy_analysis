import backtrader as bt



class BaseStrategy(bt.Strategy):
    

    def log(self, txt, dt=None):
        '''Вывод строки с датой на конслоь'''
        dt = dt or self.datas[0].datetime.date(0)
        print(f'{dt}, {txt}')
    

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
