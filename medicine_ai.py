import os
from dotenv import load_dotenv
from groq import Groq

# Load .env file
load_dotenv()

# Groq Client
client = Groq(
    api_key=os.getenv("GROQ_M_API_KEY")
)


def analyze_medicine(ocr_text):

    prompt = f"""
You are an experienced pharmacist and medical assistant.

The following text was extracted from a medicine strip using OCR.

OCR Text:
{ocr_text}

Identify the medicine and generate a complete medical report.

Return your response in the following format only.

Medicine Name:
Generic Name:
Medicine Type:
Used For:
How It Works:
Dosage:
Common Side Effects:
Serious Side Effects:
Who Should Avoid It:
Food Interactions:
Pregnancy Advice:
Storage:
When to Consult a Doctor:

If the OCR text is unclear, identify the most likely medicine and mention that it is an estimated identification.

Do not include markdown.
Keep the language simple for patients.
"""

    try:

        response = client.chat.completions.create(

            model="llama-3.3-70b-versatile",

            messages=[
                {
                    "role": "system",
                    "content": "You are an expert pharmacist."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0.3,

            max_tokens=1000

        )

        return response.choices[0].message.content

    except Exception as e:

        return f"Groq Error: {str(e)}"
    
if __name__ == "__main__":

    text = """
    DOLO 650
    Paracetamol Tablets IP
    """

    print(analyze_medicine(text))