import aiorx
import asyncio


# This awaitable computes 11² + 13² in 1.5 second
observable = (aiorx
    .interval(0.1)               # Count from zero every 0.1 s
    .skip(10)                    # Skip the first 10 numbers
    .take(5)                     # Take the following 5
    .filter(lambda x: x % 2)     # Keep odd numbers
    .map(lambda x: x ** 2)       # Square the results
    .reduce(lambda x, y: x + y)  # Add the numbers together
)


# Run the awaitable
loop = asyncio.get_event_loop()
result = loop.run_until_complete(observable)
print('11² + 13² = ', result)

# Can run several times
result = loop.run_until_complete(observable)
print('11² + 13² = ', result)

# Clean up
loop.run_until_complete(asyncio.sleep(0))
loop.close()
