
import aiorx
import inspect
import functools


class BaseFactory:

    def __init__(self, factory):
        self._factory = factory

    @classmethod
    def attach_method(cls, func=None, name=None, return_type=None):
        return attach_function(
            func, to=cls, name=name, return_type=return_type)


class Awaitable(BaseFactory):

    def __await__(self):
        try:
            return self._factory.__await__()
        except AttributeError:
            return self._factory().__await__()


class Observable(BaseFactory):

    def __aiter__(self):
        try:
            return self._factory.__aiter__()
        except AttributeError:
            return self._factory().__aiter__()


def guess_factory_class(function):
    if inspect.isasyncgenfunction(function):
        return Observable
    elif inspect.iscoroutinefunction(function):
        return Awaitable
    else:
        raise TypeError(function)


def make_factory_function(function, factory_class=None):
    if factory_class is None:
        factory_class = guess_factory_class(function)

    @functools.wraps(function)
    def factory_function(*args, **kwargs):
        return factory_class(lambda: function(*args, **kwargs))

    return factory_function


def attach_function(function=None,
                    to=aiorx,
                    name=None,
                    return_type=None):
    if function is None:
        return lambda function: attach_function(
            function, to=to, name=name, return_type=return_type)
    if name is None:
        name = function.__name__
    factory_function = make_factory_function(function, return_type)
    setattr(to, name, factory_function)
    return getattr(to, name)
