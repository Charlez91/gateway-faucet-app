# imports
import random
import time
from concurrent.futures import ThreadPoolExecutor
from functools import wraps

from asyncio import sleep, get_event_loop

count = 0
 
# define a retry decorator
def retry_with_exponential_backoff(
    initial_delay: float = 1,#initial delay before next retry
    exponential_base: float = 2,#rate for exponential increase
    jitter: bool = True,#randomize the increase
    max_retries: int = 5,#max number of retries
    errors: tuple = (),
    fallback_func = None
):
    """Retry a function with exponential backoff."""
    
    def wrapped_func(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Initialize variables
            num_retries = 0
            delay = initial_delay
    
            # Loop until a successful response or max_retries is hit or an exception is raised
            while True:
                try:
                    print("trying")
                    loop = get_event_loop()
                    result = await loop.run_in_executor(ThreadPoolExecutor(max_workers=10), func, *args, **kwargs)
                    return result
    
                # Retry on specific errors
                except errors as e:
                    # Increment retries
                    num_retries += 1
    
                    # Check if max retries has been reached
                    if num_retries > max_retries:
                        if fallback_func:
                            return fallback_func(*args, **kwargs)#in cases where txn_id is first
                        raise Exception(
                            f"Maximum number of retries ({max_retries}) exceeded."
                        )
    
                    # Increment the delay
                    delay *= exponential_base * (1 + jitter * random.random())
    
                    # Sleep for the delay
                    print(f"delay:{delay}")
                    #time.sleep(delay)
                    await sleep(delay)
    
                # Raise exceptions for any errors not specified
                except Exception as e:
                    print(e)
                    print(args, kwargs)
                    if fallback_func:
                        return fallback_func(*args, **kwargs)
                    return
    
        return wrapper
    return wrapped_func

