import asyncio
import itertools


# Shortcut functions

def aiter(ait):
    return ait.__aiter__()


async def anext(ait):
    return await ait.__anext__()


# Flow control functions

async def amap(coro, *aits):
    aits = list(map(aiter, aits))
    coro = asyncio.coroutine(coro)
    try:
        while True:
            args = []
            for ait in aits:
                args.append(await anext(ait))
            yield await coro(*args)
    except StopAsyncIteration:
        pass


async def afilter(coro, ait):
    coro = asyncio.coroutine(coro)
    async for item in ait:
        if await coro(item):
            yield item


async def areduce(coro, ait, init=None):
    ait = aiter(ait)
    coro = asyncio.coroutine(coro)
    value = await anext(ait) if init is None else init
    async for item in ait:
        value = await coro(value, item)
    return value


# Extra functions

def azip(*aits):
    return amap(tuple, *aits)


def aenumerate(ait, start=0):
    counter = itertools.count(start)
    func = lambda arg: (next(counter), arg)
    return amap(func, ait)
