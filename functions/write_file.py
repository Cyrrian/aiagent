import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write to the specified file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file": types.Schema(
                type=types.Type.STRING,
                description="The file to write to, relative to the working directory. If not provided, returns an error.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file specified. If not provided, does nothing.",
            ),
        },
    ),
)

def write_file(working_directory, file_path, content):
    working_directory_abs = os.path.abspath(working_directory)
    full_path_abs = os.path.abspath(os.path.join(working_directory_abs, file_path))

    if not full_path_abs.startswith(working_directory_abs):
        result = f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        return result
    
    with open(full_path_abs, "w") as f:
        f.write(content)

    if os.path.exists(full_path_abs):
        with open(full_path_abs, "r") as f:
            if f.read() == content:
                result = f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
                return result
            
    result = f'Error: File "{file_path}" not written successfully'
    return result