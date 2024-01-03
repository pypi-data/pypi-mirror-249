from enum import Enum, auto
import contextlib
import time


class Task(Enum):
    RECT = 0
    POINT = auto()
    POLYGON = auto()

    


class Mode(Enum):
    READ = 0
    MARK = auto()
    DOODLE = auto()



class Profiler(contextlib.ContextDecorator):
    """This for a simple Profiler from python"""

    def __init__(self, desc=None, verbose=True, logger=None, precision=7):
        self.verbose = verbose
        # self.desc = f"[{desc}]" if desc != "" else ""
        self.prefix = f"🥝::{'Profiler' if desc is None else desc} => "
        self.logger = logger or print
        self.precision = precision
        # self.ms = ms


    def __enter__(self):
        self.t0 = time.time()
        return self

    def __exit__(self, type, value, traceback):
        self.duration = time.time() - self.t0
        if self.verbose:
            # self.logger(
            #     f"{self.prefix}{(time.time() - self.t0) * 1e3:.{self.precision}f} ms."
            # )
            self.summary(t0=self.t0, t1=time.time())

    def __call__(self, obj):
        def wrapper(*args, **kwargs):
            t0 = time.time()
            ret = obj(*args, **kwargs)
            if self.verbose:
                # self.logger(
                #     f"{self.prefix}{(time.time() - t0) * 1e3:.2f} ms."
                # )
                self.summary(t0=t0, t1=time.time())
            return ret
        return wrapper


    def summary(self, t0, t1):
        _t = (t1 - t0) * 1e3
        # if self.ms:
        #     _t *= 1e3
        # _s = f"{self.prefix}{_t:.{self.precision}f}" + "ms" if self.ms else "s"
        _s = f"{self.prefix}{_t:.{self.precision}f}" + "ms"
        self.logger(_s)

