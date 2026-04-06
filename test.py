# test_client.py
import asyncio
from src.arXiv_rtool.arXivClient import ArXivClient
from src.arXiv_rtool.rateLimiter import RateLimiter


async def main():
    client = ArXivClient(RateLimiter(3))
    papers = await client.fetch("transformer")
    print(f"Got {len(papers)} papers")
    for p in papers:
        print(p.title)


asyncio.run(main())
