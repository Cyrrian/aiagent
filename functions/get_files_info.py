import os

def get_files_info(working_directory, directory="."):
    working_directory_abs = os.path.abspath(working_directory)
    full_path_abs = os.path.abspath(os.path.join(working_directory_abs, directory))

    if directory == ".":
        dir_name = "current"
    else:
        dir_name = f"'{directory}'"

    result = f"Result for {dir_name} directory:"

    if not full_path_abs.startswith(working_directory_abs):
        result += f'\n\tError: Cannot list "{directory}" as it is outside the permitted working directory'
        return result

    if not os.path.isdir(full_path_abs):
        result += f'\n\tError: "{directory}" is not a directory'
        return result
    
    dir_contents = os.listdir(full_path_abs)
    for item in dir_contents:
        item_abs = os.path.join(full_path_abs, item)
        result += f"\n - {item}: file_size={os.path.getsize(item_abs)} is_dir={os.path.isdir(item_abs)}"

    return result