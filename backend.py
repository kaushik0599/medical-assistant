import requests
import os

API_KEY = os.getenv("OPENROUTER_API_KEY")

def is_medical_query(text):
    text = text.lower()

    medical_keywords = [
        "pain", "fever", "cough", "cold", "headache", "vomit", "nausea",
        "injury", "infection", "disease", "symptom", "doctor", "medicine",
        "body", "stomach", "chest", "leg", "arm", "eye", "ear"
    ]

    for word in medical_keywords:
        if word in text:
            return True

    return False


def analyze_symptoms(symptoms, history=None):
    try:
        # 🚫 Block irrelevant queries
        if not is_medical_query(symptoms):
            return """❌ This system is designed only for medical symptom analysis.

Please describe health-related symptoms like:
- fever, pain, cough, headache, etc.

For other queries, please use general AI tools like ChatGPT."""

        url = "https://openrouter.ai/api/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        }

        data = {
            "model": "openai/gpt-3.5-turbo",
            "messages": [
                {
                    "role": "user",
                    "content": f"""
You are a medical assistant.

STRICT RULES:
- ONLY answer medical symptom-related queries
- Do NOT answer general or unrelated questions

User symptoms: {symptoms}

Give:
- Symptom summary
- Possible conditions
- Advice
- When to see a doctor
"""
                }
            ]
        }

        response = requests.post(url, headers=headers, json=data)
        result = response.json()

        if "choices" in result:
            return result["choices"][0]["message"]["content"]
        else:
            return f"API Error: {result}"

    except Exception as e:
        return f"Error: {str(e)}"
