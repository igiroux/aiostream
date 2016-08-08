
import aiorx
import inspect
import functools


class Observable:

    def __init__(self, factory):
        try:
            self._factory = factory.__aiter__
        except AttributeError:
            self._factory = factory

    def __aiter__(self):
        return self._factory().__aiter__()

    def __await__(self):
        return self._await().__await__()

    async def _await(self):
        async for item in self:
            pass
        return item

    @classmethod
    def attach_method(cls, func=None, name=None):
        return attach_function(func, to=cls, name=name)


def attach_function(function=None, to=aiorx, name=None):
    if function is None:
        return lambda function: attach_function(function, to=to, name=name)
    if name is None:
        name = function.__name__

    @functools.wraps(function)
    def factory_function(*args, **kwargs):
        return Observable(lambda: function(*args, **kwargs))

    setattr(to, name, factory_function)
    return getattr(to, name)
