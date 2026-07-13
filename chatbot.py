import os
import json
from dotenv import load_dotenv
from openai import OpenAI

# Load .env
load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    raise ValueError("OPENROUTER_API_KEY not found.")

client = OpenAI(
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1"
)


def load_disease_data():
    try:
        with open("disease_data.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def get_local_response(user_input):
    disease_data = load_disease_data()
    query = user_input.lower()

    for disease in disease_data:
        if disease.lower() in query:
            data = disease_data[disease]

            return f"""
Disease: {disease}
Symptoms: {', '.join(data['symptoms'])}
Prevention: {', '.join(data['prevention'])}
Treatment: {data['treatment']}
Vaccination: {data['vaccination']}
"""
    return None


def get_ai_response(user_query):
    response = client.chat.completions.create(
        model="meta-llama/llama-3.3-70b-instruct:free",
        messages=[
            {
                "role": "system",
                "content": """
You are an AI Public Health Chatbot.

1. Explain diseases.
2. Explain symptoms.
3. Suggest prevention methods.
4. Promote vaccination awareness.
5. Promote healthy lifestyle practices.
6. Never provide diagnosis.
7. Always recommend consulting healthcare professionals.
"""
            },
            {
                "role": "user",
                "content": user_query
            }
        ]
    )

    return response.choices[0].message.content


def get_response(user_query):
    local_response = get_local_response(user_query)

    if local_response:
        return local_response

    try:
        return get_ai_response(user_query)

    except Exception as e:
        return f"""
AI Service Error:
{str(e)}
"""

