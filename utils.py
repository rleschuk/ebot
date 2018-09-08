
from time import time
from collections import deque


class Memory(object):
    def __init__(self, func, condition=None, maxlen=None, **kwargs):
        self._func = func
        self._condition = condition
        self._memo = deque([], maxlen)
        if self._condition is None:
            self._condition = lambda obj, memo: True

    def __call__(self, *args, **kwargs):
        memo = self.get_memo(args)
        if memo is None or not self._condition(self, memo):
            memo = self.set_memo(args, kwargs, memo)
        return memo['result']

    @property
    def __name__(self):
        return self._func.__name__

    @property
    def now(self):
        return int(time())

    def get_memo(self, args):
        args_ = [e['args'] for e in self._memo]
        if args in args_:
            return self._memo[args_.index(args)]

    def set_memo(self, args, kwargs, memo=None):
        if memo is None:
            memo = {
                'args': args,
                'timestamp': self.now,
                'result': self._func(*args, **kwargs)
            }
            self._memo.append(memo)
        else:
            memo['timestamp'] = self.now
            memo['result'] = self._func(*args, **kwargs)
        return memo

    @staticmethod
    def timed(seconds=10):
        def wrapped(func):
            return Memory(func,
                condition = lambda o, m: o.now - m.get('timestamp', 0) < seconds
            )
        return wrapped

    @staticmethod
    def limited(maxlen=None):
        def wrapped(func):
            return Memory(func, maxlen=maxlen)
        return wrapped


if __name__ == '__main__':

    @Memory.timed(10)
    def test1(x):
        return 'test1', x, time()

    @Memory.limited(1)
    def test2(x):
        return 'test2', x, time()
