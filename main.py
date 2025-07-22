import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.get_files_info import schema_get_files_info

def main():
    load_dotenv()

    args = []
    verbose = '--verbose' in sys.argv

    for arg in sys.argv[1:]:
        if not arg.startswith('--'):
            args.append(arg)

    if not args:
        print('AI Agent')
        print('\nUsage: python main.py "PROMPT" [--verbose]')
        exit(1)

    API_KEY = os.environ.get("GEMINI_API_KEY")
    AI_CLIENT = genai.Client(api_key=API_KEY)
    AI_MODEL = 'gemini-2.0-flash-001'
    SYSTEM_PROMPT = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
        ]
    )

    config = types.GenerateContentConfig(tools=[available_functions], system_instruction=SYSTEM_PROMPT)

    user_prompt = " ".join(args)

    messages = [
        types.Content(role='user', parts=[types.Part(text=user_prompt)]),
    ]

    if verbose:
        print('\nUSER PROMPT:')
        print(f'\t{user_prompt}')

    execute_prompt(AI_CLIENT, AI_MODEL, config, messages, verbose)
        

def execute_prompt(client, model, config, messages, verbose):
    response = client.models.generate_content(
        model=model, 
        contents=messages, 
        config=config
    )
    
    print('\nRESPONSE:')
    print(f'\t{response.text}')

    if response.function_calls:
        print('\nFUNCTION CALLS:')
        for call in response.function_calls:
            print(f'{call.name}({call.args})')

    if verbose:
        print('TOKENS USED:')
        print(f'\tPrompt tokens: {response.usage_metadata.prompt_token_count}')
        print(f'\tResponse tokens: {response.usage_metadata.candidates_token_count}')

if __name__ == "__main__":
    main()
