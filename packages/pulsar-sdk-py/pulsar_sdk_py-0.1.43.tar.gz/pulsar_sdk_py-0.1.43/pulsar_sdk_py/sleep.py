import asyncio

from typing import Callable


async def wait_for_condition(condition_check: Callable, timeout: int):
    async def check():
        while True:
            if condition_check():
                return
            await asyncio.sleep(0.1)  # Wait for 100ms

    await asyncio.wait_for(check(), timeout)
