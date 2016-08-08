import asyncio
import itertools

from .factory import Observable, attach_function
from .common import aenumerate, amap, areduce, afilter


# Observable methods

@Observable.attach_method
def map(self, coro, *aits):
    return amap(coro, self, *aits)


@Observable.attach_method
def filter(self, coro):
    return afilter(coro, self)


@Observable.attach_method
def reduce(self, coro, init=None):
    return areduce(coro, self, init)


@Observable.attach_method
def zip(self, *aits):
    return amap(tuple, self, *aits)


@Observable.attach_method
async def skip(self, arg):
    async for i, item in aenumerate(self):
        if i >= arg:
            yield item


@Observable.attach_method
async def take(self, arg):
    if arg <= 0:
        return
    async for i, item in aenumerate(self):
        yield item
        if i+1 >= arg:
            break


@Observable.attach_method
async def until(self, coro):
    coro = asyncio.coroutine(coro)
    async for item in self:
        if await coro(item):
            break
        yield item


@Observable.attach_method
async def first(self):
    async for item in self:
        yield item


@Observable.attach_method
async def last(self):
    async for item in self:
        pass
    yield item


@Observable.attach_method
async def to_list(self):
    result = []
    async for item in self:
        result.append(item)
    return result


@Observable.attach_method
async def action(self, coro):
    coro = asyncio.coroutine(coro)
    async for item in self:
        await coro(item)
        yield item


@Observable.attach_method
def print_debug(self, msg='debug'):
    func = lambda x: print(msg, ':', x)
    return self.action(func)


# Plain functions

reduce = attach_function(areduce, name='reduce')
map = attach_function(amap, name='map')
filter = attach_function(amap, name='filter')


@attach_function
async def interval(t, start=0):
    for current in itertools.count(start):
        await asyncio.sleep(t)
        yield current
