import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.call_function import call_function

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

def check_for_verbose(args):
    if "--verbose" in args:
        return True
    else: 
        return False

def main(*argv):
    user_prompt = sys.argv[1]
    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)]),]

    schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
    )

    schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Get the content of a file in the specified directory, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file, relative to the working directory. If not provided, will return error message. If the file has more than 10000 characters it will return a truncated version of the file with 10000 characters",
            ),
        },
    ),
    )

    schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description= "Overwrites into a file in the specified directory,constrained to the working directory. If the directory doesn't exist and the is within the working directory, creates a directory and the file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file, relative to the working directory. If not provided, will return error message. If the file has more than 10000 characters it will return a truncated version of the file with 10000 characters",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content that is to be written into the file"
            )
        },
    ),
    )

    schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description= "Runs a python file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file, relative to the working directory. If not provided, will return error message. If the file doesn't end in .py, returns an error. If the file doesn't exist, returns error",
            ),
        },
    ),
    )

    available_functions = types.Tool(function_declarations=[schema_get_files_info,schema_get_file_content,schema_write_file, schema_run_python_file])
  

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    model = 'gemini-2.0-flash-001'
    response = client.models.generate_content(model=model, contents=messages,config=types.GenerateContentConfig(tools=[available_functions],system_instruction=system_prompt))
    if response:
        verbose = check_for_verbose(sys.argv)
        for function_call in response.function_calls:
            function_call_result = call_function(function_call, verbose)
            if function_call_result.parts[0].function_response.response:
                if verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")
                else:
                    print(function_call_result.parts[0].function_response.response["result"])
            else: 
                raise Exception("CRITICAL ERROR")
    else:
        print("Error, invalid prompt")
        return 1


main()