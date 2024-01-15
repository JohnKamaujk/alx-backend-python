#!/usr/bin/env python3
'''Task 1's module.
'''
import asyncio
import time

wait_n = __import__('1-concurrent_coroutines').wait_n


async def measure_time(n: int, max_delay: int) -> float:
    """
    Measures the total execution time for wait_n(n, max_delay)
    and returns total_time / n.

    :param n: Number of times to spawn wait_random.
    :param max_delay: Maximum delay in seconds.
    :return: Average execution time per wait_random call.
    """
    start_time = time.time()

    # Using asyncio.run to run the wait_n function
    asyncio.run(wait_n(n, max_delay))

    end_time = time.time()
    total_time = end_time - start_time

    # Calculating and returning the average execution time per wait_random call
    average_time = total_time / n
    return average_time
