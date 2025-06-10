import os

def get_file_content(working_directory, file_path):
    MAX_CHARS = 10000
    target_path = os.path.join(working_directory, file_path)
    try:
        if os.path.abspath(target_path).startswith(os.path.abspath(os.path.abspath(working_directory))):
            if os.path.isfile(target_path):
                with open(target_path, "r") as f:
                    file_content_string = f.read(MAX_CHARS)
                    if len(file_content_string) == MAX_CHARS:
                        return file_content_string + f'\n[...File "{file_path}" truncated at 10000 characters]'
                    else:
                        return file_content_string
            else:
                return f'Error: File not found or is not a regular file: "{file_path}"'
        else:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    except Exception as e:
        return f"Error: {str(e)}"