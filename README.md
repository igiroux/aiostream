aiorx
=====

A toy implementation of [ReactiveX][1] using [asyncio][2] and asynchronous generators ([PEP 525][3]).


Synopsis
--------

The [ReactiveX introduction][4] shows the following table:

|              | Single items | Multiple items |
|--------------|--------------|----------------|
| Synchronous  | Function     | Iterable       |
| Asynchronous | Future       | Observable     |

This definition of what an observable is matches closely the [asynchronous iterable][5] definition introduced by [PEP 492][6]. Moreover, [PEP 525][3] provides asynchronous generators that can be used to easily implement the [operators][7] defined by ReactiveX, e.g:

```python
async def skip(ait, n):
    async for item in ait:
        if n > 0:
		    n -= 1
		else:
            yield item
```

It is then quite straight forward to implement and use ReactiveX objects with asyncio.


Example
-------

A working [example][8] is provided. It features the following awaitable:

```python
# This awaitable computes 11² + 13² in 1.5 second
awaitable = (aiorx
    .interval(0.1)               # Count from zero every 0.1 s
    .skip(10)                    # Skip the first 10 numbers
    .take(5)                     # Take the following 5
    .filter(lambda x: x % 2)     # Keep odd numbers
    .map(lambda x: x ** 2)       # Square the results
    .reduce(lambda x, y: x + y)  # Add the numbers together
)
```


Requirement
-----------

- Python 3.6 with [PEP 525 implementation][9]

[1]: http://reactivex.io/
[2]: https://docs.python.org/3.4/library/asyncio.html
[3]: https://www.python.org/dev/peps/pep-0525/
[4]: http://reactivex.io/intro.html
[5]: https://docs.python.org/3/glossary.html#term-asynchronous-iterable
[6]: https://www.python.org/dev/peps/pep-0492
[7]: http://reactivex.io/documentation/operators.html
[8]: ./example.py
[9]: https://github.com/1st1/cpython/tree/async_gen
