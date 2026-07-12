import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def get_bot_response(message):

    prompt = f"""
You are an AI Health Assistant.

Rules:

- Give general health advice only.
- Do not prescribe medicines.
- Recommend consulting a doctor for emergencies.
- Keep answers under 150 words.
- Be polite and easy to understand.

User:
{message}
"""

    try:

        response = client.chat.completions.create(

            model="llama-3.3-70b-versatile",

            messages=[
                {
                    "role":"system",
                    "content":"You are an AI medical assistant."
                },
                {
                    "role":"user",
                    "content":prompt
                }
            ],

            temperature=0.4,

            max_tokens=300

        )

        return response.choices[0].message.content

    except Exception as e:

        print(e)

        return "Sorry, AI service is unavailable."