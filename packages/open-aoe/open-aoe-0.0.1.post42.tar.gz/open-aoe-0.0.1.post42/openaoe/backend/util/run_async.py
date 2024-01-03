#!/bin/python
# run async, without await before return response
import asyncio


async def run_async(fn, *args, **kwargs):
    loop = asyncio.get_event_loop()
    loop.create_task(fn(*args, **kwargs))
