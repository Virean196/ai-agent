import os

def write_file(working_directory, file_path, content):
    target_path = os.path.join(working_directory, file_path)
    try:
        if os.path.abspath(target_path).startswith(os.path.abspath(os.path.abspath(working_directory))):
            if os.path.exists(target_path) and os.path.isfile(target_path):
                with open(target_path, "w") as f:
                    f.write(content)
                    print(f'Successfully wrote to "{file_path}" ({len(content)} characters written)')
            else:
                directory, filename = os.path.split(file_path)
                os.makedirs(os.path.join(working_directory, directory))
                with open(os.path.join(working_directory, os.path.join(directory,filename)), "w") as f:
                    f.write(content)
                    print(f'Successfully wrote to "{file_path}" ({len(content)} characters written)')
        else:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    except Exception as e:
        return f"Error: {str(e)}"