import os
import subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run the specified python file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file": types.Schema(
                type=types.Type.STRING,
                description="The file to run, relative to the working directory. If not provided or if not a python fille, returns an error.",
            ),
            "args": types.Schema(
                type=types.Type.STRING,
                description="Option arguments to provide to the python file.",
            ),

        },
    ),
)

def run_python_file(working_directory, file_path, args=[]):
    working_directory_abs = os.path.abspath(working_directory)
    full_path_abs = os.path.abspath(os.path.join(working_directory_abs, file_path))

    result = ""

    if not full_path_abs.startswith(working_directory_abs):
        result = f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        return result
    
    if not os.path.exists(full_path_abs):
        result =  f'Error: File "{file_path}" not found.'
        return result
    
    if not full_path_abs.endswith('.py'):
        result = f'Error: "{file_path}" is not a Python file.'
        return result
    
    process_result = subprocess.run(['uv', 'run', full_path_abs, *args], capture_output=True, timeout=30)

    if len(process_result.stdout):
        result += f"STDOUT: {process_result.stdout}"
    if len(process_result.stderr):
        result += f"STDOUT: {process_result.stderr}"

    return result