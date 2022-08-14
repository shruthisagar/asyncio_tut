import asyncio
import httpx


async def crawl0(prefix:str, url:str = "")->None:
    url = url or prefix
    print(f"Crawling {url}")
    client = httpx.AsyncClient()
    try: 
        res = await client.get(url)
    finally:
        await client.aclose()
    for line in res.text.splitlines():
        print(prefix)
        print(line)
        if line.startswith(prefix):
            await crawl0(prefix,line)
    

asyncio.run(crawl0("https://langa.pl/crawl/"))