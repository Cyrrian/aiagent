import os
from dotenv import load_dotenv
from google import genai

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    model = 'gemini-2.0-flash-001'

    query = 'Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum.'
    response = client.models.generate_content(model=model, contents=query)

    print(response.text)
    print('**** TOKENS USED ****')
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

if __name__ == "__main__":
    main()
