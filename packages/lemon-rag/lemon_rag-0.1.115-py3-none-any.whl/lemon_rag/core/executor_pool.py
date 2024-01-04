import queue
from concurrent.futures import ThreadPoolExecutor
from typing import Generator, Iterable, Callable

streaming_pool = ThreadPoolExecutor(max_workers=16)


def submit_generator_task(generator: Iterable[str]) -> queue.Queue:
    q = queue.Queue(maxsize=128)

    def inner_task():
        for value in generator:
            print("iterate the generator", value)
            q.put(value)
        q.put("end")

    streaming_pool.submit(inner_task)
    return q


CallbackTask = Callable[[queue.Queue], None]


def submit_callback_task(t: CallbackTask) -> queue.Queue:
    q = queue.Queue(maxsize=128)

    def inner_task():
        t(q)
        q.put("end")

    streaming_pool.submit(inner_task)
    return q
