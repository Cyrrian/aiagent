import os

def get_file_content(working_directory, file_path):
    MAX_CHARS = 10000

    working_directory_abs = os.path.abspath(working_directory)
    full_path_abs = os.path.abspath(os.path.join(working_directory_abs, file_path))

    if not full_path_abs.startswith(working_directory_abs):
        result = f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        return result

    if not os.path.isfile(full_path_abs):
        result = f'Error: File not found or is not a regular file: "{file_path}"'
        return result
    
    with open(full_path_abs, "r") as f:
        file_content_string = f.read(MAX_CHARS)

        if len(f.read()) > MAX_CHARS:
            file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'

    return file_content_string