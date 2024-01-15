#!/usr/bin/env python3
'''Task 1's module.
'''
import asyncio
from typing import List

wait_random = __import__('0-basic_async_syntax').wait_random


async def wait_n(n: int, max_delay: int) -> List[float]:
    """
    Async routine that spawns wait_random n times with the specified max_delay.

    :param n: Number of times to spawn wait_random.
    :param max_delay: Maximum delay in seconds.
    :return: List of delays in ascending order.
    """
    tasks = [wait_random(max_delay) for _ in range(n)]
    results = await asyncio.gather(*tasks)
    sorted_results = sorted(results)
    return sorted_results
