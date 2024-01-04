import traceback

from lemon_rag.api.local import get_rid, get_user


def lemon_info(value: str):
    pass


file = "/var/log/supervisor/backup.log"


def info(msg: str, *args):
    suffix = f" rid={get_rid()} user_id={get_user()}"
    try:
        log_expr = (msg + suffix) % args
        print(log_expr)
        lemon_info(log_expr)
        with open(file, "a") as f:
            f.write(log_expr + "\n")
    except Exception as e:
        print(traceback.format_exc())
        lemon_info(traceback.format_exc())
        with open(file, "a") as f:
            f.write(traceback.format_exc()+"\n")
