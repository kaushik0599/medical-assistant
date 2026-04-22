import requests
import os
import streamlit as st

# ================== 🔐 API KEY ==================
API_KEY = st.secrets.get("OPENROUTER_API_KEY") or os.getenv("OPENROUTER_API_KEY")


# ================== 🚨 EMERGENCY DETECTION ==================
def detect_emergency(text):
    text = text.lower()

    emergency_keywords = [
        "chest pain", "heart attack", "can't breathe", "difficulty breathing",
        "unconscious", "severe bleeding", "stroke", "fainting",
        "seizure", "no pulse", "collapse"
    ]

    return any(word in text for word in emergency_keywords)


# ================== 📊 SEVERITY ==================
def get_severity(text):
    text = text.lower()

    severe = ["chest pain", "breathing", "blood", "unconscious", "severe", "stroke"]
    moderate = ["fever", "infection", "vomiting", "dizziness", "pain"]

    if any(word in text for word in severe):
        return "🔴 Severe"
    elif any(word in text for word in moderate):
        return "🟡 Moderate"
    else:
        return "🟢 Mild"


# ================== 🧠 SMART MEDICAL FILTER ==================
def is_medical_query(user_input):
    text = user_input.lower()

    # Basic rejection patterns
    non_medical_patterns = [
        "learn", "course", "dance", "movie", "song", "code", "programming",
        "weapon", "game", "youtube", "instagram", "travel"
    ]

    # If clearly non-medical
    if any(word in text for word in non_medical_patterns):
        return False

    # Accept if contains health-like context
    medical_indicators = [
        "pain", "fever", "headache", "infection", "disease",
        "symptom", "sick", "hurt", "doctor", "medicine",
        "cancer", "diabetes", "asthma", "pressure", "breathing"
    ]

    return any(word in text for word in medical_indicators)


# ================== 🤖 MAIN FUNCTION ==================
def analyze_symptoms(symptoms, history=None):

    # 🚨 Emergency first
    if detect_emergency(symptoms):
        return """🚨 EMERGENCY WARNING

Your symptoms may indicate a serious condition.

👉 Please seek IMMEDIATE medical help
👉 Call emergency services or visit nearest hospital

Do NOT rely on this app in emergencies.
"""

    # ❌ Not medical
    if not is_medical_query(symptoms):
        return """❌ This system is designed ONLY for medical queries.

Please describe health-related issues like:
• "I have fever and headache"
• "Chest pain for 2 days"
• "Symptoms of diabetes"

For other queries, please use general AI tools like ChatGPT.
"""

    # 🔐 API check
    if not API_KEY:
        return "❌ API key missing. Set OPENROUTER_API_KEY in Streamlit Secrets or environment."

    try:
        url = "https://openrouter.ai/api/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        data = {
            "model": "openai/gpt-3.5-turbo",
            "messages": [
                {
                    "role": "system",
                    "content": """You are a medical assistant.

Give structured output:
1. Symptom Summary
2. Possible Conditions
3. Advice
4. When to see a doctor

Keep it simple and clear."""
                },
                {
                    "role": "user",
                    "content": symptoms
                }
            ]
        }

        response = requests.post(url, headers=headers, json=data)
        result = response.json()

        # 🧠 Extract safely
        if "choices" not in result:
            return f"API Error: {result}"

        ai_response = result["choices"][0]["message"]["content"]

        # 📊 Add severity
        severity = get_severity(symptoms)

        # 🤖 Follow-up
        follow_up = """

Follow-up questions:
• How long have you had these symptoms?
• Is the condition improving or worsening?
• Any additional symptoms?
"""

        final_output = f"Severity Level: {severity}\n\n{ai_response}\n{follow_up}"

        return final_output

    except Exception as e:
        return f"Error: {str(e)}"
