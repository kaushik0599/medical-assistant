import requests
import os

# ===== API KEY =====
try:
    import streamlit as st
    API_KEY = st.secrets.get("OPENROUTER_API_KEY")
except:
    API_KEY = None

if not API_KEY:
    API_KEY = os.getenv("OPENROUTER_API_KEY")

URL = "https://openrouter.ai/api/v1/chat/completions"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}" if API_KEY else "",
    "Content-Type": "application/json"
}

# ===== 🔥 SMART HYBRID FILTER =====
def is_medical_query(user_input):
    text = user_input.lower()

    # ✅ Fast reliable keywords (broad coverage)
    basic_keywords = [
        "pain", "ache", "fever", "headache", "cough", "cold",
        "vomit", "nausea", "dizzy", "fatigue", "weakness",
        "infection", "injury", "burn", "bleeding",

        "cancer", "diabetes", "asthma", "covid", "arthritis",
        "stroke", "heart", "tumor", "thyroid", "bp", "pressure",
        "multiple sclerosis", "ms"
    ]

    # ✅ If obvious match → accept immediately
    if any(word in text for word in basic_keywords):
        return True

    # 🔁 fallback to AI (only if needed)
    if not API_KEY:
        return False

    try:
        data = {
            "model": "openai/gpt-3.5-turbo",
            "messages": [
                {
                    "role": "system",
                    "content": "Reply ONLY YES or NO. Is this about health, disease, symptoms, or medical advice?"
                },
                {"role": "user", "content": user_input}
            ],
            "max_tokens": 5
        }

        res = requests.post(URL, headers=HEADERS, json=data)
        result = res.json()

        answer = result.get("choices", [{}])[0].get("message", {}).get("content", "").strip().upper()

        return "YES" in answer

    except:
        return False


# ===== 🧠 MAIN FUNCTION =====
def analyze_symptoms(symptoms, history=None):

    if not API_KEY:
        return "❌ API key missing. Set OPENROUTER_API_KEY."

    # ❌ Block irrelevant
    if not is_medical_query(symptoms):
        return """❌ This system is designed ONLY for medical queries.

Please describe health-related issues like:
• "I have fever and headache"
• "Chest pain for 2 days"
• "Symptoms of diabetes"

For other queries, use general AI tools."""

    try:
        data = {
            "model": "openai/gpt-3.5-turbo",
            "messages": [
                {
                    "role": "system",
                    "content": """You are a medical assistant.

Format:
Symptom Summary:
Possible Conditions:
Advice:
When to See a Doctor:

Be simple, safe, and helpful."""
                },
                {
                    "role": "user",
                    "content": f"User input: {symptoms}"
                }
            ]
        }

        res = requests.post(URL, headers=HEADERS, json=data)
        result = res.json()

        if "choices" not in result:
            return f"⚠️ API Error: {result}"

        return result["choices"][0]["message"]["content"]

    except Exception as e:
        return f"⚠️ Error: {str(e)}"
