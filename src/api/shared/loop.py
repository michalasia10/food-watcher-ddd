import asyncio


async def get_event_loop():
    loop = asyncio.get_event_loop()
    yield loop
