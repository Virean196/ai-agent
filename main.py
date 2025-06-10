import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

def check_for_verbose(args):
    for arg in args:
        if arg == "--verbose":
            return True
        else:
            return False

def main(*argv):
    user_prompt = sys.argv[1]
    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)]),]

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    model = 'gemini-2.0-flash-001'
    response = client.models.generate_content(model=model, contents=messages)
    if response:
        if len(sys.argv) > 2:
            if check_for_verbose:
                print(f"User prompt: {sys.argv[1]}")
                print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
                print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        else:
            print(response.text)
    else:
        print("Error, invalid prompt")
        return 1


main()