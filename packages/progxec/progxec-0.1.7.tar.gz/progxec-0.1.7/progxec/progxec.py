import os, subprocess


def compiler_available(): 
    """
    Check if the GPP (GNU Compiler Collection for C and C++) is available.

    Returns:
        bool: True if the GPP compiler is available, False otherwise.

    Note:
        This function attempts to run the 'g++ --version' command using the `subprocess` module
        to check if the GPP compiler is available. If the command runs successfully, it assumes
        that the compiler is available and returns True. If an error occurs (either due to a
        subprocess error or if 'g++' is not found), it returns False.

    Example:
        >>> is_available = compiler_available()
        >>> print(is_available)
        True
    """
    try:
        # Try running g++ with the version flag to check if it's available
        subprocess.run(['g++', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        # If an error occurs or if g++ is not found, return False
        return False


def compile_cpp(file_path):
    """
    Compile a C++ source code file using the g++ compiler.

    Parameters:
        file_path (str): The path to the C++ source code file.

    Returns:
        str: The path to the compiled executable file.

    Raises:
        subprocess.CalledProcessError: If the compilation process fails.

    Note:
        This function uses the `subprocess` module to run the g++ compiler and compile
        the specified C++ source code file. If the compilation is successful, it returns
        the path to the compiled executable file. If an error occurs during compilation,
        a `subprocess.CalledProcessError` is raised.

    Example:
        >>> executable_path = compile_cpp("source_code.cpp")
        >>> print(executable_path)
        "source_code_executable.exe"
    """
    try:
        # Run the g++ command to compile the C++ file
        subprocess.run(['g++', file_path, '-o', f'{file_path[:-4]}_executable'], check=True)

        # Return the path to the compiled executable file
        return f'{file_path[:-4]}_executable.exe'
    
    except subprocess.CalledProcessError as e:
        # Return an error message if the compilation fails
        raise SystemError(f"Compilation failed with error: {e}")



def exec_exe_file(exe_path):
    """
    Execute a compiled executable file and capture its output.

    Parameters:
        exe_path (str): The path to the compiled executable file.

    Returns:
        str: The captured output of the executed executable.

    Raises:
        SystemError: If an error occurs during the execution of the executable.

    Note:
        This function uses the `subprocess` module to run the specified executable file
        and capture its output. If an error occurs during execution, a `SystemError` is raised
        with a descriptive error message.

    Example:
        >>> result = exec_exe_file("compiled_program.exe")
        >>> x = return(result)
        >>> print(x)
        "Hello, World!"
    """
    try:
        # Run the '.exe' file and capture its output
        result = subprocess.check_output(exe_path, shell=True, text=True)
        return result.strip()
    except subprocess.CalledProcessError as e:
        # Handle any errors that occur during execution
        raise SystemError(f"Error executing '{exe_path}': {e}")


def exec_cpp(file_name):
    """
    Execute a compiled C++ program given its file name.

    Parameters:
        file_name (str): The name of the C++ source code file.

    Returns:
        Any: The result of executing the compiled C++ program.

    Raises:
        FileExistsError: If the specified file does not exist.
        SystemError: If the GPP (GNU Compiler Collection for C and C++) is not present.

    Note:
        This function assumes the availability of a function `compiler_available` that checks
        whether the GPP compiler is available. It also assumes the existence of functions
        `compile_cpp` and `exec_exe_file` to compile the C++ code and execute the resulting
        executable, respectively.
    """
    x = None

    # Check if the GPP compiler is available
    if compiler_available():
        # Check if the specified file exists
        if os.path.isfile(file_name):
            # Compile the C++ code
            file_name = compile_cpp(file_name) 
            # Execute the compiled executable
            x = exec_exe_file(file_name) 
            return x
        else:
            raise FileExistsError("The specified file does not exist.")
    else:
        raise SystemError("GPP (GNU Compiler Collection for C and C++) not present")
