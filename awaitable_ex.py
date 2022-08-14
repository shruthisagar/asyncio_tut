import asyncio
from datetime import datetime

def print_now():
    print(datetime.now())

async def keep_printing(name:str = "")->None:
    while True:
        print(name, end="")
        print_now()
        # await is used to block
        # allows asyncio to do something else till 0.50 seconds are over.
        # it yields function that runs later
        await asyncio.sleep(0.50)

async def async_main()-> None:
    # a main function that handles all the async functions in our program
    kp = keep_printing("Hey ")
    waiter = asyncio.wait_for(kp, 10)
    try:
        await waiter
        # suppose you don't use await in the expr, we get error 
        # saying we never awaited an async function
        # we need to enable asyncio debug and tracemalloc to get complete details
        # PYTHONASYNCIODEBUG=1 PYTHONTRACEMALLOC=1 python3 awaitable_ex.py 
        # waiter
    except asyncio.TimeoutError:
        print("time's up!")
    
if __name__ == "__main__":
    # asyncio.run(keep_printing())

    # wait for execution to complete or exit after 10 seconds 
    # asyncio.wait_for(keep_printing(), 10)
    asyncio.run(async_main())