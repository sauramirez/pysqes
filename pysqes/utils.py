import importlib


def import_fn(fn_name):
    """
    Return python function object from the function name argument that's in the form of "module.func"
    """
    module_name, attribute = fn_name.rsplit('.', 1)
    module = importlib.import_module(module_name)
    return getattr(module, attribute)


def import_module(module_name):
    return importlib.import_module(module_name)
