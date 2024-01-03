import importlib
import logging
import types

# The attribute lookups that should be immune to the lazy loading magic start with this
# prefix.
_LAZY_LOADER_PREFIX = "_ll"


class _LazyLoader(types.ModuleType):
    """Lazily import a module, mainly to avoid pulling in large dependencies.

    This class is not meant to be accessed publicly, see the 'dynamic_import' function
    below for how to use the lazy loading feature.

    If the

    Taken from tensorflow's LazyLoader:

    https://github.com/tensorflow/tensorflow/blob/master/tensorflow/python/util/lazy_loader.py
    """

    def __init__(self, local_name, parent_module_globals, name, warning=None):
        self._ll_local_name = local_name
        self._ll_parent_module_globals = parent_module_globals
        self._ll_warning = warning

        # These members allows doctest correctly process this module member without
        # triggering self._load(). self._load() mutates parant_module_globals and
        # triggers a dict mutated during iteration error from doctest.py.
        # - for from_module()
        super().__setattr__("__module__", name.rsplit(".", 1)[0])
        # - for is_routine()
        super().__setattr__("__wrapped__", None)

        super().__init__(name)

    def _load(self):
        """Load the module and insert it into the parent's globals."""
        # Import the target module and insert it into the parent's namespace
        module = importlib.import_module(self.__name__)
        self._ll_parent_module_globals[self._ll_local_name] = module

        # Emit a warning if one was specified
        if self._ll_warning:
            logging.warning(self._ll_warning)
            # Make sure to only warn once.
            self._ll_warning = None

        # Update this object's dict so that if someone keeps a reference to the
        #   LazyLoader, lookups are efficient (__getattr__ is only called on lookups
        #   that fail).
        self.__dict__.update(module.__dict__)

        # Mark that this module was lazily loaded so we can check for it in other
        # projects/contexts.
        module._ll_lazily_loaded = True
        return module

    def __getattr__(self, name):
        module = self._load()
        return getattr(module, name)

    def __setattr__(self, name, value):
        if name.startswith(_LAZY_LOADER_PREFIX):
            super().__setattr__(name, value)
        else:
            module = self._load()
            setattr(module, name, value)
            self.__dict__[name] = value
            try:
                # check if the module has __all__
                if name not in self.__all__ and name != "__all__":
                    self.__all__.append(name)
            except AttributeError:
                pass

    def __delattr__(self, name):
        if name.startswith(_LAZY_LOADER_PREFIX):
            super().__delattr__(name)
        else:
            module = self._load()
            delattr(module, name)
            self.__dict__.pop(name)
            try:
                # check if the module has __all__
                if name in self.__all__:
                    self.__all__.remove(name)
            except AttributeError:
                pass

    def __repr__(self):
        # Carefully to not trigger _load, since repr may be called in very
        # sensitive places.
        return f"<LazyLoader {self.__name__} as {self._ll_local_name}>"

    def __dir__(self):
        module = self._load()
        return dir(module)

    def __reduce__(self):
        imported_module = importlib.import_module, (self.__name__,)

        # Mark that this module was lazily loaded so we can check for it in other
        # projects/contexts.
        imported_module._ll_lazily_loaded = True

        return imported_module


def dynamic_import(
    local_name: str,
    lazy: bool = True
):
    """Perform the import, either lazily or not.

    Args:
        local_name: the name of the module to import. Note that you can't
            pass in the name of a variable within a module here, only modules are
            supported.
            Example: "pandas"
            Example: "os.path"
        lazy: bool of whether to lazily import. True by default, and if set to False,
            eagerly import the given module instead. This is useful if you want to
            lazily or eagerly import based on a flag, for example.
    """
    if lazy:
        return _LazyLoader(local_name, globals(), local_name)
    else:
        return importlib.import_module(local_name)


__all__ = ["dynamic_import"]
