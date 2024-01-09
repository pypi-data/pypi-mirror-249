import copy
import importlib
from concurrent.futures import ThreadPoolExecutor, Executor
from typing import Callable

pool = ThreadPoolExecutor(max_workers=8)


def submit_task(executor: Executor, func: Callable, *args, **kwargs):
    utils = importlib.import_module("baseutils.utils")
    cu = utils.LemonContextVar.current_user.get()
    copy_cu = copy.copy(cu)

    def inner(*args, **kwargs):
        utils.LemonContextVar.current_user.set(copy_cu)
        utils.LemonContextVar.current_connector.set(None)
        utils.LemonContextVar.other_connector.set(None)
        utils.LemonContextVar.current_root_form.set(None)
        utils.LemonContextVar.current_transaction.set(None)
        utils.LemonContextVar.current_lsm.set(None)
        utils.LemonContextVar.current_workspace.set(None)
        utils.LemonContextVar.taskid.set(None)
        utils.LemonContextVar.condition.set(None)
        utils.LemonContextVar.atomic_resource_locks.set(None)
        try:
            func(*args, **kwargs)
        except:
            pass

    return executor.submit(inner, *args, **kwargs)


