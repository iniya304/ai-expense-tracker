import os
from dotenv import load_dotenv
from groq import Groq

# Load the API key from .env
load_dotenv()
api_key = os.getenv('GROQ_API_KEY')

if not api_key:
    print("ERROR: GROQ_API_KEY not found. Check your .env file.")
else:
    print("API key loaded successfully.")

    client = Groq(api_key=api_key)

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": "Say hello in one short sentence."}
        ]
    )

    print("\n----- AI RESPONSE -----")
    print(response.choices[0].message.content)