import queue
from concurrent.futures import ThreadPoolExecutor
from typing import Generator, Iterable

streaming_pool = ThreadPoolExecutor(max_workers=16)


def submit_streaming_task(generator: Iterable[str]) -> queue.Queue:
    q = queue.Queue(maxsize=128)

    def inner_task():
        for value in generator:
            print("iterate the generator", value)
            q.put(value)
        q.put("end")

    streaming_pool.submit(inner_task)
    return q
