import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

from config import AI_MODEL, SYSTEM_PROMPT
from call_function import available_functions, call_function

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
  
    user_prompt = " ".join(args)

    messages = [
        types.Content(role='user', parts=[types.Part(text=user_prompt)]),
    ]

    if verbose:
        print('\nUSER PROMPT:')
        print(f'\t{user_prompt}')

    print(execute_prompt(AI_CLIENT, messages, verbose))
        

def execute_prompt(client, messages, verbose):
    response = client.models.generate_content(
        model=AI_MODEL, 
        contents=messages, 
        config=types.GenerateContentConfig(tools=[available_functions], system_instruction=SYSTEM_PROMPT)
    )
  
    if not response.function_calls:
        return response.text

    function_responses = []
    for function_call_part in response.function_calls:
        function_call_result = call_function(function_call_part, verbose)
        if not function_call_result.parts or not function_call_result.parts[0].function_response:
            raise Exception('Invalid function response')
        if verbose:
            print(f'-> {function_call_result.parts[0].function_response.response}')
        function_responses.append(function_call_result.parts[0])

    if verbose:
        print('TOKENS USED:')
        print(f'\tPrompt tokens: {response.usage_metadata.prompt_token_count}')
        print(f'\tResponse tokens: {response.usage_metadata.candidates_token_count}')

    if not function_responses:
        raise Exception('No responses generated')

if __name__ == "__main__":
    main()
