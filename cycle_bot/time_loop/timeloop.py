import asyncio
import time

import schedule


cycles = [123, 234, 345, 456]


async def time_loop():
    while True:
        this_time = time.time()

        if this_time >= cycles[0]:
            pass  # drop cycle from queue, send message to user, send status to database

        else:
            time.sleep(0.1)


def start_loop():
    asyncio.run(time_loop())
