
import asyncio
from time import time
from typing import Callable, Coroutine
import httpx

todo = set()
async def progress(url:str, algo: Callable[...,Coroutine]) -> None:
    asyncio.create_task(algo(url), name=url)
    todo.add(url)
    start = time()
    while len(todo):
        print(f"{len(todo)}: "+", ".join(sorted(todo))[-38:])
        # background tasks run here..
        await asyncio.sleep(0.5)

    end = time()
    print(f"{int(end-start)} seconds")

async def progress1(url:str, algo: Callable[...,Coroutine]) -> None:
    task = asyncio.create_task(algo(url), name=url)
    todo.add(task)
    start = time()
    while len(todo):
        # background tasks run here..
        done, _pending = await asyncio.wait(todo, timeout= 0.5)
        todo.difference_update(done)
        urls = (t.get_name() for t in todo)
        # print(", ".join(sorted(urls)))
        # can find concurrency by len(todo)
        print(f"{len(todo)}: " + ", ".join(sorted(urls)))
    end = time()
    print(f"{int(end-start)} seconds")

addr = "https://langa.pl/crawl/"
async def crawl1(prefix: str, url: str = "") -> None:
    url = url or prefix
    client = httpx.AsyncClient()
    try: 
        res = await client.get(url)
    finally:
        await client.aclose()
    for line in res.text.splitlines():
        if line.startswith(prefix):
            todo.add(line)
            await crawl1(prefix,line)
    todo.discard(url)

async def crawl2(prefix: str, url: str = "") -> None:
    url = url or prefix
    client = httpx.AsyncClient()
    try: 
        res = await client.get(url)
    finally:
        await client.aclose()
    for line in res.text.splitlines():
        if line.startswith(prefix):
            # creating a background task.
            # what do we do if we need some result to be handled?
            # what do we do if it fails in btw?
            # store tasks and handle cancellation
            # asyncio.create_task(crawl2(prefix, line), name=line,)
            task = asyncio.create_task(crawl2(prefix, line), name=line,)
            todo.add(task)
    # task will help us maintain using asyncio.wait
    # todo.discard(url)


# asyncio.run(progress(addr, crawl1))
# asyncio.run(progress(addr, crawl2))

asyncio.run(progress1(addr, crawl2))
    