import os
import subprocess

def run_python_file(working_directory, file_path):
    target_path = os.path.join(working_directory, file_path)
    try:
        if os.path.abspath(target_path).startswith(os.path.abspath(os.path.abspath(working_directory))):
            if os.path.exists(target_path):
                if ".py" in target_path:
                    output = subprocess.run(["python3",target_path], timeout=30, capture_output=True)
                    stdout_output = output.stdout.decode('utf-8')
                    stderr_output = output.stderr.decode('utf-8')
                    return_code = output.returncode
                    if return_code != 0:
                        return f"Process exited with code {return_code}\nSTDOUT: \n{stdout_output}\nSTDERR: \n{stderr_output}"
                    if not stdout_output.strip() and not stderr_output.strip():
                        return ("No output produced")
                    return f"STDOUT: \n{stdout_output}\nSTDERR: \n{stderr_output}"
                else:
                    return f'Error: "{file_path}" is not a Python file.'
            else:
                return f'Error: File "{file_path}" not found.'
        else:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    except Exception as e:
        return f"Error: executing Python file: {e}"