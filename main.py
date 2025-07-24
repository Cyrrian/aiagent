import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.write_file import schema_write_file, write_file
from functions.run_python_file import schema_run_python_file, run_python_file

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
    - Read file contents
    - Execute Python files with optional arguments
    - Write or overwrite files

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_write_file,
            schema_run_python_file,

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
            function_call_result = call_function(call, verbose)
            if not function_call_result.parts[0].function_response.response:
                raise Exception('Invalid function response')
            else:
                if verbose:
                    print(f'-> {function_call_result.parts[0].function_response.response}')

    if verbose:
        print('TOKENS USED:')
        print(f'\tPrompt tokens: {response.usage_metadata.prompt_token_count}')
        print(f'\tResponse tokens: {response.usage_metadata.candidates_token_count}')

def call_function(function_call_part, verbose=False):

    if verbose:
        print(f'Calling function: {function_call_part.name}({function_call_part.args})')
    else:
        print(f' - Calling function: {function_call_part.name}')
    
    function_name = function_call_part.name

    function_args = function_call_part.args
    function_args['working_directory'] = './calculator'

    match function_name:
        case 'get_files_info':
            function_result = get_files_info(function_args['working_directory'], function_args['directory'])
        case 'get_file_content':
            function_result = get_file_content(function_args['working_directory'], function_args['file'])
        case 'write_file':
            function_result = write_file(function_args['working_directory'], function_args['file'], function_args['content'])
        case 'run_python_file':
            if not 'args' in function_args:
                function_args['args'] = ''
            function_result = run_python_file(function_args['working_directory'], function_args['file'], function_args['args'])
        case _:
            return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )



if __name__ == "__main__":
    main()
