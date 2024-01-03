import traceback

from lemon_rag.api.local import get_rid, get_user


def lemon_info(value: str):
    pass

def info(msg: str, *args):
    suffix = f" rid={get_rid()} user_id={get_user()}"
    try:
        log_expr = (msg + suffix) % args
        print(log_expr)
        lemon_info(log_expr)
    except Exception as e:
        print(traceback.format_exc())
        lemon_info(traceback.format_exc())
