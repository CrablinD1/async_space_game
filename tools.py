import asyncio


async def sleep(tic=1):
    for _ in range(tic):
        await asyncio.sleep(0)
