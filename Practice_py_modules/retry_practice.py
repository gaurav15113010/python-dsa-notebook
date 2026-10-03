"""
Coding exercise — Bounded retries

Requirements:
- operation is an async function taking no arguments.
- Return its result immediately when it succeeds.
- Retry only TimeoutError and ConnectionError.
- Wait 1 second before the second attempt, 2 seconds before the third, then 4 seconds, and so on.
- max_attempts includes the initial call: 3 means at most three calls.
- After the final failed attempt, re-raise the exception without another wait.
- Other exceptions should propagate immediately.
- Reject max_attempts < 1.
"""

import asyncio

async def operation():
    await asyncio.sleep(1)
    return "Success"



async def call_with_retry(operation, max_attempts=3):
    if max_attempts<1:
        raise ValueError("max_attempts must be at least 1")
    for attempt in range(1,max_attempts+1):
        try:
            return await operation()
        except (TimeoutError,ConnectionError):
            if attempt==max_attempts:
                raise
            else:
                await asyncio.sleep(2**(attempt-1))

                
