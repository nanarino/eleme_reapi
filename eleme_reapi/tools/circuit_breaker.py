'''基于错误次数的简单熔断器'''
from collections import deque


class CircuitFused(Exception):
    '''熔断器异常触发'''
    def __init__(self, err='高频错误导致熔断器触发'):
        Exception.__init__(self, err)


class circuit_breaker:
    '''错误次数熔断器
    
        Args:
            threshold: 允许的连续错误次数
            callback：熔断器触发回调
    '''
    def __init__(self, threshold: int, callback=None):
        self.threshold = threshold
        self.deque = deque([True] * threshold)
        self.callback = callback

    def shift(self, boolean: bool):
        '''压入熔断器队列'''
        self.deque.pop()
        self.deque.appendleft(boolean)
        if not any(self.deque):
            if callable(self.callback):
                self.callback()
            else:
                raise CircuitFused
