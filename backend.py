import requests
import os

API_KEY = os.getenv("OPENROUTER_API_KEY")

def analyze_symptoms(symptoms, history=None):
    try:
        url = "https://openrouter.ai/api/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://medical-assistant-wc3pco29rjtwseudpwc3m9.streamlit.app",
            "X-Title": "Medical Assistant"
        }

        data = {
            "model": "mistralai/mistral-7b-instruct",
            "messages": [
                {
                    "role": "user",
                    "content": f"""
You are a helpful medical assistant.

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

        # Safe handling
        if "choices" in result:
            return result["choices"][0]["message"]["content"]
        else:
            return f"API Error: {result}"

    except Exception as e:
        return f"Error: {str(e)}"
