from groq import Groq

# Replace with your Groq API Key
client = Groq(
    api_key="GROQ_R_API_KEY"
)

def analyze_report(report_text):

    prompt = f"""
You are an experienced medical AI assistant.

Analyze the following medical report and explain it in very simple English.

Give the output in this format:

1. Summary
2. Abnormal Values
3. Possible Meaning
4. Health Risks
5. Diet Recommendations
6. Lifestyle Recommendations
7. When to Consult a Doctor

Medical Report:

{report_text}
"""

    response = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0.3

    )

    return response.choices[0].message.content