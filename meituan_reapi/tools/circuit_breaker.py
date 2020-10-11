'''基于暂存队列的简单熔断器'''
from collections import deque
from time import sleep
from functools import reduce, partial
from typing import Callable, Iterable, Optional, Union, Any


def sleeper(secs: Union[float, int] = 60) -> Callable:
    '''返回套娃的time.sleep(secs=60)'''
    def wait():
        sleep(secs)

    return wait


class CircuitFused(Exception):
    '''熔断器异常触发'''
    def __init__(self, err: str = '达到阈值，熔断器触发'):
        super().__init__(self, err)


class circuit_breaker():
    '''简单的错误熔断器
    
        Args:
            threshold: 允许的连续错误次数(大于1整数)/错误率(0到1) 默认是7
            callback：熔断器触发回调，不设置将在触发熔断时抛出CircuitFused异常
                callback可接受一个参数，将传入熔断器本身
            keyword-only:
                maxlen: 最大样本长度，整数，默认None
                initlen: 初始样本长度，整数，默认100

        Ps:
            如果为次数熔断，initlen和maxlen都将被赋值为threshold次数
            如果为次数熔断，初始化后的threshold属性将被赋值为1.0
            如果为错误率熔断，initlen不宜设置的过大，且不能超过maxlen（如果设置）
            callback一般设置为sleeper()
    '''
    def __init__(self,
                 threshold: Union[float, int] = 7,
                 callback: Optional[Callable] = None,
                 *,
                 maxlen: Optional[int] = None,
                 initlen: int = 100):

        self.callback = callback
        if threshold >= 1 and isinstance(threshold, int):
            if maxlen and maxlen != threshold:
                raise TypeError("参数错误：错误次数类型的熔断器的maxlen即是次数，不能设置")
            self.maxlen = threshold
            self.initlen = threshold
            self.threshold = 1.0
        elif 0 < threshold < 1:
            maxlen = maxlen or None
            initlen = initlen or 100
            if initlen and (not isinstance(initlen, int) or initlen < 1):
                raise TypeError("参数错误：initlen参数应该是不小于1的整数")
            if maxlen and (not isinstance(maxlen, int) or maxlen < initlen):
                raise TypeError("参数错误：maxlen参数必须是整数且不小于initlen参数")
            self.maxlen = maxlen
            self.initlen = initlen
            self.threshold = threshold
        else:
            raise TypeError("参数错误：threshold参数应该在0-1之间或者大于1的整数")
        self.sample = deque([True] * self.initlen, maxlen=self.maxlen)

    def __len__(self) -> int:
        '''返回样本列表长度'''
        return len(self.sample)

    @property
    def err_rate(self) -> float:
        '''样本的错误率'''
        return 1 - (reduce(lambda x, y: x + y, self.sample, 0) / len(self))

    def shift(self, is_success: bool):
        '''将新样本载入熔断器样本队列'''
        self.sample.appendleft(bool(is_success))
        if self.err_rate >= self.threshold:
            if callable(self.callback):
                try:
                    self.callback(self)
                except TypeError:
                    self.callback()
            else:
                if self.threshold == 1.0:
                    raise CircuitFused(f'连续{len(self)}次错误导致熔断器触发')
                raise CircuitFused('错误率达到阈值导致熔断器触发')
        return self

    def extend(self, iterable: Iterable):
        '''迭代载入新样本'''
        for is_success in iterable:
            self.shift(is_success)
        return self

    def reset(self):
        '''重新初始化熔断器状态'''
        self.sample = deque([True] * self.initlen, maxlen=self.maxlen)
        return self


def retry(*tasks: Callable,
          error=(Exception, ),
          err_callback: Optional[Callable] = None,
          cb: Optional[circuit_breaker] = None,
          cb_times: int = 7,
          cb_callback: Optional[Callable] = None) -> Union[list, Any]:
    '''やりなおす! 重试执行函数 捕获到指定的异常将会重试 如果超过次数会触发回调或抛出CircuitFused异常
    
        Args:
            tasks: 可执行的任务.
            error: 指定的作为熔断器样本的异常类型.
            err_callback: 异常样本触发回调.
                err_callback可接受一个参数，将传入错误信息
            cb[cb_times, cb_callback] 熔断器对象.
                cb_times: 最大重试次数,默认是7
                cb_callback: 熔断器触发回调，不设置将在触发熔断时抛出CircuitFused异常
                    cb_callback可接受一个参数，将传入熔断器本身

        
        Return:
            如果只有一个任务 返回成功的任务结果
            如果有多个任务 返回成功样本的任务结果列表

    '''
    cb = circuit_breaker(cb_times, cb_callback) if cb is None else cb
    ret = None
    rets = []
    for task in tasks:
        while 1:
            try:
                ret = task()
                cb.shift(True)
                break
            except error as err_info:
                if callable(err_callback):
                    try:
                        err_callback(err_info)
                    except TypeError:
                        err_callback()
                cb.shift(False)
        rets.append(ret)
    return ret if len(rets) == 1 else rets


#永远重试，每次间隔15秒
retry_for_good = partial(retry, cb=None, cb_times=1, cb_callback=sleeper(15))