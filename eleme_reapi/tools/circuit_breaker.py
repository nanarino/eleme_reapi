'''基于暂存队列的简单熔断器'''
from collections import deque
from time import sleep
from functools import reduce


def sleeper(secs: float = 60):
    '''返回套娃的time.sleep(secs=60)'''
    def wait():
        sleep(secs)

    return wait


class CircuitFused(Exception):
    '''熔断器异常触发'''
    def __init__(self, err='达到阈值，熔断器触发'):
        Exception.__init__(self, err)


class circuit_breaker():
    '''简单的错误熔断器
    
        Args:
            threshold: 允许的连续错误次数/错误率
            callback：熔断器触发回调

        ps:
            callback一般设置为sleeper()
    '''
    threshold = 0

    def __init__(self, threshold: float, callback=None):

        self.callback = callback
        if threshold >= 1:
            self.threshold_times = threshold
            self.deque = deque([True] * threshold, maxlen=threshold)
        elif 0 < threshold < 1:
            self.threshold = threshold
            self.deque = deque()
        else:
            raise ValueError("threshold参数应该在0-1之间或者大于1的整数")

    def __len__(self):
        '''返回长度'''
        return len(self.deque)

    @property
    def err_rate(self):
        '''错误率'''
        return 1 - (reduce(lambda x, y: x + y, self.deque, 0) / len(self))

    def shift(self, is_success: bool):
        '''压入熔断器队列'''
        self.deque.appendleft(is_success)

        if threshold:=self.threshold:
            if self.err_rate > threshold:
                print(self.callback)
                if callable(self.callback):
                    self.callback()
                else:
                    raise CircuitFused('错误率达到阈值导致熔断器触发')
        else:
            if not any(self.deque):
                if callable(self.callback):
                    self.callback()
                else:
                    raise CircuitFused('高频连续错误导致熔断器触发')
        return self

    def re_init(self):
        '''重新初始化熔断器状态'''
        if self.threshold:
            self.deque = deque()
        else:
            self.deque.extendleft([True] * self.threshold_times)
