# Progxec python library

The Progxec python library can be used to call compile and call C++ files to get outputs of executables in python files. This library will provide a standard way to execute the C++ files.
This library will be further extended to call programming languages, other than C++ within python itself.

## Installation

- Pending
    
## Features

- Call Executables
- Compile C++ files
- Execute C++ through Python and store data


## API Reference

#### Import the Module

```
  from execute_cpp import ecpp
```

#### Call the C++ execute function
The **`exec`** function takes ***`filename`*** as the input parameter.
```
ecpp.exec(filename)
```
**Example**
```
  output = ecpp.exec("main.cpp")
  print(output)
```

## Usage/Examples

**main.cpp** 
```cpp
from execute_cpp import ecpp

output = ecpp.exec("main.cpp")
print(output)
```

**script.py** 
```python
from execute_cpp import ecpp

output = ecpp.exec("main.cpp")
print(output)
```

## Authors

- [@jaysheel-ops](https://github.com/jaysheel-ops)

