import asyncio
from datetime import datetime
import inspect


async def keep_printing(name:str = "")->None:
    while True:
        print(name, end="")
        print_now()
        # await is used to block
        # allows asyncio to do something else till 0.50 seconds are over.
        # it yields function that runs later
        await asyncio.sleep(0.50)


def print_now():
    print(datetime.now())

async def print3times():
    for _ in range(3):
        print_now()
        await asyncio.sleep(0.1)

async def async_main()-> None:
    # a main function that handles all the async functions in our program
    await keep_printing("first ")
    await keep_printing("second ")
    await keep_printing("third ")


# ---- Block 1 ----
# Checking types of coro and functions 
# error: expected coroutine but got regular function

# coro1 = print3times()
# coro2 = print3times()
# print(f"type of print3times {type(print3times)}")
# print(f"type of coro1 {type(coro1)}")
# asyncio.run(print3times)
# ---- End of Block 1 ----

# ---- Block 2 ----
# running coroutines

# coro1 = print3times()
# coro2 = print3times()
# asyncio.run(coro1)
# asyncio.run(coro2)
# ---- End of Block 2 ----

# ---- Block 3 ----
# coroutine can be awaited only once

# coro1 = print3times()
# coro2 = print3times()
# asyncio.run(coro1)
# asyncio.run(coro1)
# ---- End of Block 3 ----

# ---- Block 4 ----
# checking which is awaitable and which is not

# coro2 = print3times()
# print(f"isawaitable - print3times -- {inspect.isawaitable(print3times)}")
# print(f"isawaitable - coro2 -- {inspect.isawaitable(coro2)}")
# ---- End of Block 4 ----

# ---- Block 5 ----
# await in async_main blocks second and third till first is completed.
# first is infinite loop so never runs second and third

# asyncio.run(async_main())
# ---- End of Block 5 ---- 

# ---- Block 6 ----
# gather - runs everything in single thread parallely
# generates future error - 
# all submitted awaitables that have not been completed are also cancelled.
# our case we have 3 awaitables
# it propogates cancellation to all 3 coroutines
# function -> await expr raises cancelled error

async def async_gather_main() -> None:
    try:
        await asyncio.wait_for( asyncio.gather(
            keep_printing("first "),
            keep_printing("second "),
            keep_printing("third "),
        ), 5)
    except asyncio.TimeoutError:
        print("time out!")

asyncio.run(async_gather_main())

# ---- End of Block 6 ---- 

# ---- Block 7 ----
# gather - runs everything in single thread parallely.


async def keep_printing_error_handled(name:str = "")->None:
    while True:
        print(name, end="")
        print_now()
        try:
        # await is used to block
        # allows asyncio to do something else till 0.50 seconds are over.
        # it yields function that runs later
            await asyncio.sleep(0.50)
        except asyncio.CancelledError:
            print("cancelled --- ", name)
            break



async def async_gather_main() -> None:
    try:
        await asyncio.wait_for( asyncio.gather(
            keep_printing_error_handled("first "),
            keep_printing_error_handled("second "),
            keep_printing_error_handled("third "),
        ), 5)
    except asyncio.TimeoutError:
        print("time out!")

asyncio.run(async_gather_main())

# ---- End of Block 7 ---- 

