import os, subprocess

def _is_gpp_available():
    try:
        # Try running g++ with the version flag to check if it's available
        subprocess.run(['g++', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        # If an error occurs or if g++ is not found, return False
        return False

def _compile_cpp_file(file_path):
    try:
        # Run the g++ command to compile the C++ file
        subprocess.run(['g++', file_path, '-o', f'{file_path[:-4]}_executable'], check=True)

        # Print a success message
        return  f'{file_path[:-4]}_executable.exe'
        print(f"Compilation successful. Executable '{file_path[:-4]}_executable' created.")
    
    except subprocess.CalledProcessError as e:
        # Print an error message if the compilation fails
        print(f"Compilation failed with error: {e}")

def _execute_exe_file(exe_path):
    try:
        # Run the '.exe' file and capture its output
        result = subprocess.check_output(exe_path, shell=True, text=True)
        return result.strip()
    except subprocess.CalledProcessError as e:
        # Handle any errors that occur during execution
        raise SystemError(f"Error executing '{exe_path}': {e}")
        # print(f"Error executing '{exe_path}': {e}")
        # return None


def exec(file_name):
    x = None
    if _is_gpp_available():
        if os.path.isfile(file_name):
            file_name = _compile_cpp_file(file_name)
            x = _execute_exe_file(file_name)
            return x
        else:
            raise FileExistsError("The filedoes not exist.")
    else:
        raise SystemError("GPP not present")  


