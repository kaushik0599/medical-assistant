import requests
import os
import streamlit as st

# ================== 🔐 API KEY ==================
try:
    API_KEY = st.secrets["OPENROUTER_API_KEY"]
except:
    API_KEY = os.getenv("OPENROUTER_API_KEY")


# ================== 🚨 EMERGENCY DETECTION ==================
def detect_emergency(text):
    text = text.lower()
    emergency_keywords = [
        "chest pain", "heart attack", "can't breathe", "cannot breathe",
        "difficulty breathing", "difficulty in breathing", "trouble breathing",
        "unconscious", "severe bleeding", "heavy bleeding",
        "stroke", "fainting", "seizure", "collapse", "overdose", "poisoning",
        "suicidal", "suicide", "not breathing", "stopped breathing"
    ]
    return any(word in text for word in emergency_keywords)


# ================== 📊 SEVERITY ==================
def get_severity(text):
    text = text.lower()
    severe = ["chest pain", "breathing", "blood", "bleeding", "stroke", "unconscious", "overdose", "seizure"]
    moderate = ["fever", "infection", "vomiting", "dizziness", "pain", "migraine", "fracture", "rash"]
    if any(word in text for word in severe):
        return "🔴 Severe"
    elif any(word in text for word in moderate):
        return "🟡 Moderate"
    else:
        return "🟢 Mild"


# ================== 🧠 MEDICAL FILTER ==================
def is_medical_query(user_input):
    text = user_input.lower()

    non_medical_exact = [
        "dance tutorial", "movie recommend", "song lyrics", "play a game",
        "write code", "programming help", "youtube", "instagram", "tiktok",
        "stock market", "crypto", "recipe", "travel", "weather"
    ]
    if any(phrase in text for phrase in non_medical_exact):
        return False

    medical_keywords = [
        "pain", "ache", "fever", "cough", "cold", "sneeze", "sneezing",
        "runny nose", "stuffy nose", "congestion", "sore throat", "throat",
        "headache", "migraine", "nausea", "vomiting", "diarrhea", "constipation",
        "fatigue", "tired", "weakness", "dizzy", "dizziness", "fainting",
        "swelling", "swollen", "rash", "itching", "itchy", "burning",
        "bleeding", "blood", "bruise", "bruising", "wound", "injury",
        "cramps", "spasm", "stiffness", "numbness", "tingling",
        "shortness of breath", "breathing", "chest", "palpitation",
        "appetite", "weight loss", "weight gain", "night sweats", "chills",
        "eye", "ear", "nose", "skin", "stomach", "abdomen", "back",
        "joint", "muscle", "bone", "neck", "shoulder", "knee", "ankle",
        "diabetes", "hypertension", "asthma", "allergy", "allergic",
        "infection", "viral", "bacterial", "fungal", "flu", "influenza",
        "covid", "corona", "hiv", "aids", "std", "sti",
        "cancer", "tumor", "cyst", "ulcer", "hernia",
        "arthritis", "osteoporosis", "anemia", "thyroid",
        "anxiety", "depression", "stress", "insomnia", "sleep",
        "acne", "eczema", "psoriasis", "dermatitis",
        "urinary", "uti", "kidney", "liver", "gallbladder",
        "appendix", "appendicitis", "pneumonia", "bronchitis",
        "sinusitis", "tonsils", "tonsillitis",
        "fracture", "sprain", "strain", "dislocation",
        "epilepsy", "dementia",
        "medicine", "medication", "drug", "tablet", "capsule", "syrup",
        "antibiotic", "paracetamol", "ibuprofen", "aspirin", "cetirizine",
        "amoxicillin", "metformin", "insulin", "steroids", "inhaler",
        "cream", "ointment", "drops", "injection", "vaccine", "dose",
        "side effect", "overdose", "prescription", "dosage",
        "doctor", "hospital", "clinic", "diagnose", "diagnosis",
        "treatment", "remedy", "cure", "surgery", "test", "lab",
        "sick", "ill", "unwell", "symptom", "condition", "disease",
        "health", "medical", "hurt", "feel", "suffering",
    ]

    for word in medical_keywords:
        if word in text:
            return True

    patterns = ["i have", "i am feeling", "i feel", "suffering from", "symptoms of", "what is", "can i take"]
    for p in patterns:
        if p in text and len(text.split()) >= 3:
            return True

    return False


# ================== 🤖 MAIN FUNCTION ==================
def analyze_symptoms(symptoms, history=None):

    # 🚨 Emergency check FIRST — before anything else
    if detect_emergency(symptoms):
        return """🚨 **EMERGENCY WARNING**

Your symptoms may indicate a **life-threatening condition**.

👉 **Call emergency services immediately — 108 / 112**
👉 **Go to the nearest hospital ER right away**

⛔ Do NOT rely on this app in emergencies."""

    # ❌ Not medical
    if not is_medical_query(symptoms):
        return """❌ **This assistant only handles medical queries.**

Please describe a symptom, condition, or medicine. Examples:
- *"I have a cough and cold for 2 days"*
- *"What are the side effects of ibuprofen?"*
- *"My stomach hurts after eating"*"""

    # 🔐 API key check
    if not API_KEY:
        return "❌ API key missing. Set `OPENROUTER_API_KEY` in Streamlit secrets."

    # Build conversation history
    messages = []
    if history:
        for msg in history[:-1]:
            if msg["role"] in ("user", "assistant"):
                messages.append({"role": msg["role"], "content": msg["content"]})
    messages.append({"role": "user", "content": symptoms})

    try:
        res = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "openai/gpt-3.5-turbo",
                "messages": [
                    {
                        "role": "system",
                        "content": """You are a knowledgeable and empathetic medical assistant.
Always respond in this structure:
1. **Symptom Summary** – briefly restate what the user described
2. **Possible Conditions** – list 2-4 likely causes
3. **Home Care & Advice** – practical steps they can take
4. **Medicines** – common OTC options if applicable (with standard dosage)
5. **When to See a Doctor** – red flag signs to watch for

Be clear, concise, and compassionate. Never refuse a genuine medical question about symptoms, conditions, or medicines.
Always end with a reminder that this is not a substitute for professional medical advice."""
                    },
                    *messages
                ]
            }
        )

        result = res.json()

        if "choices" not in result:
            return f"❌ API Error: {result}"

        ai_response = result["choices"][0]["message"]["content"]
        severity = get_severity(symptoms)

        follow_up = """

🩺 I need a bit more information to assist you better:

• How long have you had these symptoms?
• Are they getting better or worse?
• Do you have any other symptoms?

Please reply with more details.
"""

        return f"**Severity Level: {severity}**\n\n{ai_response}{follow_up}"

    except Exception as e:
        return f"❌ Error: {str(e)}"
