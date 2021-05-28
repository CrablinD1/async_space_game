import asyncio


async def sleep(tic=1):
    await asyncio.sleep(tic * 0.1)
