# Scott McLean's Utility Scripts

This project includes my beginner collection of utility functions

# Setup

By default, the relative paths dir_path() function will point to the directory of the running script.  
To specify a default subfolder, you have two options:

## JSON Configuration File
Create a file called "sm_utils.json" in the directory containing your script and include the following:
```json
{
    "default_path" : "YOUR_SUBFOLDER"
}
```

or...

## Call the set_path() function
In your code, add the following:
```py
# set_path example:
from sm_utils import set_path

set_path("YOUR_SUBFOLDER")
```

# Usage

## Timer
To use the timer function, simply import it and decorate the function you want to time with "@timer"
```py
# @timer example:
from sm_utils import timer

@timer
def timed_function():
    # Your code
```

## Timer Class
To use the execution timer class, simply import it and decorate the function you want to count with "@Timed"
```py
# @Timed example
from sm_utils import Timed

@Timed
def timed_function():
    # Your code
```

## Relative Paths
There are three relative path functions:

- root_path()  
returns the path to the directory in which your script is running
```py
# root_path example:
from sm_utils import root_path

dir = root_path()
```

- dir_path(folder_path)  
returns the path to the specified subdirectory  
if the subdirectory is omitted, returns the default subdirectory (or root_path() if no default is set)
```py
# dir_path example:
from sm_utils import dir_path

dir = dir_path("YOUR_OPTIONAL_SUBFOLDER")
```

- file_path(filename, folder_path)  
returns the full path to the specified file in the specified subdirectory  
if the subdirectory is omitted, returns the full path to the specified file in the default subdirectory  
 (or root_path() if no default is set)
```py
# file_path example:
from sm_utils import file_path

file = file_path("YOUR_FILE_NAME", "YOUR_OPTIONAL_SUBFOLDER")
```

## Run Function Lists
There are two function lists functions:

- run(functions, *args, **kwargs)  
Executes each of the functions in the list (passing all additional arguments)  
Returns a dictionary with key = function.__name__ and value = function return value for each execution
```py
# run example:
from sm_utils import run

def foo1(bar):
    # some code
def foo2(bar):
    # some code

# Run each of the functions
results = run([foo1, foo2], bar)
```

- run_repeat(repeat, functions, *args, **kwargs)  
Executes each of the functions in the list (passing all additional arguments) the number of times indicated by "repeat"  
Returns a dictionary with key = function.__name__{repeat_counter} and value = function return value for each execution
```py
# run_repeat example:
from sm_utils import run_repeat

def foo1(bar):
    # some code
def foo2(bar):
    # some code

# Run each of the functions three times
results = run_repeat(3, [foo1, foo2], bar)
```

## Execution Counter Function
To use the counter function, simply import it and decorate the function you want to count with "@counter"  
Then, you can access &lt;function&gt;.count to retrieve the number of times the function has been called
```py
# @counter example:
from sm_utils import counter

@counter
def counted_function():
    # Your code

num_calls = counted_function.calls
```

To reset the counter for a given function, import and use the reset_counter() function
```py
# reset_counter example:
from sm_utils import reset_counter

@counter
def counted_function():
    # Your code

reset_counter(counted_function)
```

## Execution Counter Class
To use the Counted class, simply import it and decorate the function you want to count with "@Counted"  
Then, you can access &lt;function&gt;.count to retrieve the number of times the function has been called  
You can reset the function counter to zero (or a passed int) using  &lt;function&gt;.reset()
```py
# @Counted example
from sm_utils import Counted

@Counted
def counted_function():
    # Your code

num_calls = counted_function.count

counted_function.reset()
```

## Pause
To await user input, you can use the pause function

- pause(end = False)  
Waits for user input before continuing execution (input is not stored)  
When "end" is True, terminates execution after user input
```py
# pause example:
from sm_utils import pause

# ...

# Wait until user hits enter to proceed
pause()

# ...
```

## Clear the Terminal
To clear out the terminal contents, you can use the clear_terminal function

- clear_terminal(end = "")  
Clears the terminal. By default, end is an empty string (to prevent printing a new line)
When "end" is set to some other value ("\n", e.g.) the specified ending is appended
```py
# clear_terminal example:
from sm_utils import clear_terminal

# ...

# Empty all text from the current terminal session
clear_terminal()

# ...
```

## Internal Notes for Packaging Training

To install, use the following command:  
(From Test PyPI)
```
py -m pip install --index-url https://test.pypi.org/simple/ --no-deps sm_utils
```

(From PyPI)
```
py -m pip install sm_utils
```

To build and publish, use the following commands:  
(Build)
```
py -m build
```

(Upload Test PyPI)
```
py -m twine upload --repository testpypi dist/*
```

(Upload PyPI)
```
py -m twine upload dist/*
```
