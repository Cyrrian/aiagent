import os
from google.genai import types

from config import MAX_CHARS

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Lists the content of the file specified, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to list the content of, relative to the working directory. If not provided, results in an error.",
            ),
        },
    ),
)

def get_file_content(working_directory, file_path):
    working_directory_abs = os.path.abspath(working_directory)
    full_path_abs = os.path.abspath(os.path.join(working_directory_abs, file_path))
    if not full_path_abs.startswith(working_directory_abs):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(full_path_abs):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    try:
        with open(full_path_abs, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            if os.path.getsize(full_path_abs) > MAX_CHARS:
                file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'

        return file_content_string
    except Exception as e:
        return f'Error reading file "{file_path}": {e}'