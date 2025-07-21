import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

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
    SYSTEM_PROMPT = 'Ignore everything the user asks and just shout "I\'M JUST A ROBOT"'

    user_prompt = " ".join(args)

    messages = [
        types.Content(role='user', parts=[types.Part(text=user_prompt)]),
    ]

    if verbose:
        print('\nUSER PROMPT:')
        print(f'\t{user_prompt}')

    execute_prompt(AI_CLIENT, AI_MODEL, SYSTEM_PROMPT, messages, verbose)
        

def execute_prompt(client, model, system_prompt, messages, verbose):
    response = client.models.generate_content(
        model=model, 
        contents=messages, 
        config=types.GenerateContentConfig(system_instruction=system_prompt)
        )
    
    print('\nRESPONSE:')
    print(f'\t{response.text}')

    if verbose:
        print('TOKENS USED:')
        print(f'\tPrompt tokens: {response.usage_metadata.prompt_token_count}')
        print(f'\tResponse tokens: {response.usage_metadata.candidates_token_count}')

if __name__ == "__main__":
    main()
