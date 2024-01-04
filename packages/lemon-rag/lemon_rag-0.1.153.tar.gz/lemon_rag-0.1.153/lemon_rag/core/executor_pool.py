import copy
import importlib
import queue
import traceback
from concurrent.futures import ThreadPoolExecutor
from typing import Generator, Iterable, Callable

from lemon_rag.utils import log

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
    q = queue.Queue(maxsize=1024)
    utils = importlib.import_module("baseutils.utils")
    cu = utils.LemonContextVar.current_user.get()
    copy_cu = copy.copy(cu)

    def inner_task():
        utils.LemonContextVar.current_user.set(copy_cu)
        log.info("inner task start running")
        try:
            t(q)
            log.info("inner task succeed")
        except:
            log.info("inner task failed")
            log.info(traceback.format_exc())
        finally:
            log.info("inner task finished running, ready to send 'end'")
            q.put("end")

    streaming_pool.submit(inner_task)
    return q
