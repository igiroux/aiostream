import aiorx
import asyncio


awaitable = (aiorx
    .interval(0.1)
    .skip(10)
    .take(5)
    .filter(lambda x: x % 2)
    .map(lambda x: x ** 2)
    .reduce(lambda x, y: x + y)
)


# Run the awaitable
loop = asyncio.get_event_loop()
result = loop.run_until_complete(awaitable)
print('11² + 13² = ', result)

# Can run several times
loop = asyncio.get_event_loop()
result = loop.run_until_complete(awaitable)
print('11² + 13² = ', result)

# Clean up
loop.run_until_complete(asyncio.sleep(0))
loop.close()
