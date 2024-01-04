"""A collection of useful beginner Python utility functions"""

#region Execution Timer
import timeit

def timer(func: callable) -> callable:
    """Time the execution of a the decorated function"""
    def wrapped(*args, **kwargs):
        start = timeit.default_timer()
        res = func(*args, **kwargs)
        end = timeit.default_timer()
        delta = end - start

        if delta > 60: ex_time = f"{int(delta // 60)} m : {round(delta % 60, 4)} s"
        elif delta * 1_000_000 < 1: ex_time = f"{round(delta * 1_000_000_000, 4)} ns"
        elif delta * 1_000 < 1: ex_time = f"{round(delta * 1_000_000, 4)} µs"
        elif delta < 1: ex_time = f"{round(delta * 1000, 4)} ms"
        else: ex_time = f"{round(delta, 4)} s"        
        print(f"Execution Time: {ex_time}")

        return res
    return wrapped

class Timed(object):
    """Class to time the execution of the decorated function"""

    def __init__(self, arg) -> None:
        """Initialize callable state for the decorated function"""
        self._arg = arg
    
    def __call__(self, *args, **kwargs) -> callable:
        """Time the function and print out the result"""
        start = timeit.default_timer()
        res = self._arg(*args, **kwargs)
        end = timeit.default_timer()
        delta = end - start

        if delta > 60: ex_time = f"{int(delta // 60)} m : {round(delta % 60, 4)} s"
        elif delta * 1_000_000 < 1: ex_time = f"{round(delta * 1_000_000_000, 4)} ns"
        elif delta * 1_000 < 1: ex_time = f"{round(delta * 1_000_000, 4)} µs"
        elif delta < 1: ex_time = f"{round(delta * 1000, 4)} ms"
        else: ex_time = f"{round(delta, 4)} s"        
        print(f"Execution Time: {ex_time}")

        return res
#endregion

#region Relative Path Functions
import sys, os, json

"""Default folder for accessing files"""
default_path: str|None=None

def root_path() -> str:
    """Return the root execution path of the script"""
    return os.path.dirname(sys.argv[0])

def set_path(folder: str|None=None) -> str:
    """Set the default folder for accessing files"""
    if folder: return folder
    json_path = os.path.join(root_path(), "sm_utils.json")
    if not os.path.isfile(json_path): return "data"
    with open(json_path) as f:
        data = json.load(f)
    global default_path
    default_path = data["default_path"]
    return data["default_path"]

set_path()

def dir_path(folder_path: str=default_path) -> str:
    """Return the specified path under the root directory"""
    if not folder_path: return root_path()
    return os.path.join(root_path(), folder_path)

def file_path(filename: str, folder_path: str = default_path) -> str:
    """Return the specified complete file path"""
    return os.path.join(dir_path(folder_path), filename)

class RelativePath:
    """Class to support relative paths in VS Code without changing terminal directory"""

    def __init__(self, folder: str|None=None):
        """Initialize the paths"""
        self.root_path = os.path.dirname(sys.argv[0])
        self.set_path(folder)

    def set_path(self, folder: str|None=None) -> str:
        """Set the default folder for accessing files"""
        if folder: return folder
        json_path = os.path.join(self.root_path, "sm_utils.json")
        if not os.path.isfile(json_path): return "data"
        with open(json_path) as f:
            data = json.load(f)
            self.default_path = data["default_path"]

    def dir_path(self, folder: str = default_path) -> str:
        """Return the specified path under the root directory"""
        if not folder: return os.path.join(self.root_path, self.default_path)
        return os.path.join(self.root_path, folder)

    def file_path(self, filename: str, folder: str=default_path) -> str:
        """Return the specified complete file path"""
        return os.path.join(self.dir_path(folder), filename)
#endregion

#region Run List of Functions
def run(functions: list[callable], *args, **kwargs) -> dict[str, callable]:
    """Execute a list of functions"""
    ret = {}
    for function in functions:
        print(f"\nFunction: {function.__name__}")
        ret[function.__name__] = function(*args, **kwargs)
    return ret

def run_repeat(repeat: int, functions: list[callable], *args, **kwargs) -> dict[str, callable]:
    """Execute a list of functions, repeating each a specified number of times"""
    ret = {}
    for function in functions:
        print(f"\nFunction: {function.__name__}")
        for i in range(repeat):
            ret[f"{function.__name__}_{i}"] = function(*args, **kwargs)
    return ret
#endregion

#region Call Counter
def counter(func: callable) -> callable:
    """Counts the number of calls to the passed function"""
    def wrapped(*args, **kwargs):
        wrapped.calls += 1
        return func(*args, **kwargs)
    wrapped.calls = 0
    return wrapped

def reset_counter(func: callable) -> None:
    """Resets the count for a decorated function to zero"""
    func.calls = 0

class Counted(object):
    """Decorator class to count calls to the decorated function"""
    def __init__(self, arg: any):
        """Initialize counter for the decorated function"""
        self._arg = arg
        self.reset()

    def __call__(self, *args, **kwds) -> callable:
        """Increment counter when the decorated function is called"""
        self.count += 1
        return self._arg(*args, **kwds)

    def reset(self, n: int=0):
        """Reset counter for the decorated function"""
        self.count = n
#endregion

#region Terminal Interactions
def pause(end: bool=False) -> None:
    """Wait for user input"""
    act = "end program" if end else "continue"
    input(f"Press <ENTER> to {act}...")
    if end: quit()

def clear_terminal(end: str="") -> None:
    """Clear the terminal"""
    print("\033c", end=end)
#endregion
