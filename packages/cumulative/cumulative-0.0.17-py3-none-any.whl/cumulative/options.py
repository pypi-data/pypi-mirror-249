import copy
from contextlib import contextmanager

default_options = {
    "reproducibility": {"random_seed": 123},
    "tqdm": {"params": {"disable": False, "leave": False, "delay": 0}},
    "transforms": {
        "destination": "base",
        "source": "base",
        "tmp": "tmp",
        "sequence": {"attributes": "attrs"},
        "fit": {"curve_fit": {"maxfev": 10000}},
    },
    "doc": {"url": "https://github.com/elehcimd/cumulative"},
}


class Options:
    _instance = None

    def __init__(self):
        raise RuntimeError("Call instance() instead")

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
            cls._instance.options = copy.deepcopy(default_options)
        return cls._instance

    def default_if_null(self, value, path):
        if value is not None:
            return value
        else:
            return self.get(path)

    def get(self, path):
        steps = path.split(".")

        d = self.options

        for step in steps:
            d = d[step]
        return d

    def set(self, path, value):
        *steps, last = path.split(".")

        d = self.options

        for step in steps:
            d = d.setdefault(step, {})
        d[last] = value

    def reset(self, path=None):
        if path is None:
            self.options = copy.deepcopy(default_options)
            return

        steps = path.split(".")
        d = default_options
        for step in steps:
            d = d[step]
        self.set(path, d)

    @contextmanager
    def option_context(self, options):
        try:
            orig_options = copy.deepcopy(self.options)
            for k, v in options.items():
                self.set(k, v)
            yield self
        finally:
            self.options = orig_options


# This object handles the options for the package, process-wide.
# To change locally the preferences, use option_context.
options = Options.instance()
