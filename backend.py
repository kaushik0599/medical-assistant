import requests

API_KEY = "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"

def analyze_symptoms(symptoms, history=None):
    try:
        url = "https://openrouter.ai/api/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        data = {
            "model": "openai/gpt-3.5-turbo",
            "messages": [
                {"role": "user", "content": f"User symptoms: {symptoms}. Give medical advice."}
            ]
        }

        response = requests.post(url, headers=headers, json=data)
        result = response.json()

        return result["choices"][0]["message"]["content"]

    except Exception as e:
        return f"Error: {str(e)}"