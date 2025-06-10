import os

def get_files_info(working_directory, directory=None):
    try:
        returned_string = []
        target_directory = os.path.join(working_directory, directory)
        if os.path.abspath(target_directory).startswith(os.path.abspath(os.path.abspath(working_directory))):
            if os.path.isdir(target_directory):
                item_list = os.listdir(target_directory)
                for item in item_list:
                    item_path = os.path.join(target_directory,item)
                    item_size = os.path.getsize(item_path)
                    is_dir = os.path.isfile(item_path)
                    returned_string.append(f"- {os.path.basename(item_path)}: file_size={item_size}, is_dir={is_dir}")
                return "\n".join(returned_string)    
            else:
                return f'Error: "{directory}" is not a directory'
        else:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    except Exception as e:
        return f"Error: {str(e)}"