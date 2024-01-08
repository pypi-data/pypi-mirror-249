import importlib

func = importlib.import_module('runtime.core.func')
all_func = func.all_func
name_to_func_mapping = {
    value.get("name"): value for key, value in all_func.items()
}


def get_all_func_names():
    return list(name_to_func_mapping.keys())
