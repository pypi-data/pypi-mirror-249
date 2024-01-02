import peewee


def patch_models(lemon):
    from lemon_rag.lemon_runtime import models
    for attr_name in dir(models):

        attr = getattr(models, attr_name)
        # print(type(attr))
        if not isinstance(attr, type):
            continue
        if not issubclass(attr, peewee.Model):
            continue
        setattr(models, attr_name, lemon.lemon_rag.get(attr_name, lemon.project_ledger.get(attr_name)))


def patch_log(lemon):
    from lemon_rag.utils import log
    setattr(log, "lemon_info", lemon.utils.log.info)


def patch_wrappers(lemon):
    from lemon_rag.lemon_runtime import wrappers
    setattr(wrappers, "file_system", lemon.filesystem)


def patch_all(lemon):
    patch_models(lemon)
    patch_log(lemon)
    patch_wrappers(lemon)
