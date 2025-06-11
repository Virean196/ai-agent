import os
from google.genai import types
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file

def call_function(function_call_part, verbose=False):
    function_name = function_call_part.name
    function_args = function_call_part.args
    function_mapping = {"get_files_info" : get_files_info, "get_file_content" : get_file_content, "write_file": write_file, "run_python_file": run_python_file}
    #function_dict = {"working_directory": "./calculator", "function_name": function_name, "function_args": function_args}

    if verbose:
        print(f"Calling function: {function_name}({function_args})") 
    else:
        print(f" - Calling function: {function_call_part.name}")
    
    
    if function_name in function_mapping:
        function_args["working_directory"] = "./calculator"
        function_result = function_mapping[function_name](**function_args)
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"result": function_result},
                )
            ],
        )   

    else:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )