import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write to the specified file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
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
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    if not (os.path.exists(full_path_abs)):
        try:
            os.makedirs(os.path.dirname(full_path_abs), exist_ok=True)
        except Exception as e:
            return f"Error: creating directory: {e}"
    if os.path.exists(full_path_abs) and os.path.isdir(full_path_abs):
        return f'Error: "{file_path}" is a directory, not a file'
    try:
        with open(full_path_abs, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: writing to file: {e}"