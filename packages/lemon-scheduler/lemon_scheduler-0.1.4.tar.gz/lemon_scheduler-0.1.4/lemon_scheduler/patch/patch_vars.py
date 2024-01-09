import peewee


def patch_models(lemon):
    from lemon_scheduler.lemon_runtime import models
    for attr_name in dir(models):

        attr = getattr(models, attr_name)
        # print(type(attr))
        if not isinstance(attr, type):
            continue
        if not issubclass(attr, peewee.Model):
            continue
        runtime_model = lemon.定时器模块.get(attr_name, None)
        setattr(models, attr_name, runtime_model)


def patch_lemon(lemon):
    from lemon_scheduler.lemon_runtime import wrappers
    setattr(wrappers, "lemon", lemon)


def patch_all(lemon):
    patch_models(lemon)
    patch_lemon(lemon)
