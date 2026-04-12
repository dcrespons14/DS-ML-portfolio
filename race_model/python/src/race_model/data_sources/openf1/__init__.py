from importlib import import_module

def __getattr__(name):
    try:
        module = import_module(f"{__name__}.{name}")
        globals()[name] = module
        return module
    except ModuleNotFoundError:
        raise AttributeError(f"openf1 has no attribute '{name}'")
