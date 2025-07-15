import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    model = 'gemini-2.0-flash-001'

    verbose = False

    args = sys.argv[1:]

    if not args:
        print("no prompt provided")
        exit(1)

    if args[-1] == '--verbose':
        verbose = True
        args = args[:-1]

    query = " ".join(args)

    messages = [
        types.Content(role="user", parts=[types.Part(text=query)]),
    ]
    response = client.models.generate_content(model=model, contents=query)

    print(response.text)

    if verbose:
        print(f"User prompt: {query}")
        print('**** TOKENS USED ****')
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

if __name__ == "__main__":
    main()
