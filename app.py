import streamlit as st
from datetime import datetime

# Import the backend function from the  backend's file
# Uncomment this line when your colleague creates backend.py:
from backend import analyze_symptoms

# ============================================
# FRONTEND CODE (Your Part)
# ============================================

# Page configuration
st.set_page_config(
    page_title="Medical Symptom Assistant",
    page_icon="🏥",
    layout="wide"
)

# Custom CSS for styling
st.markdown("""
    <style>
    .main {
        background-color: #f0f2f6;
    }
    .stAlert {
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hello! I'm here to help you understand your symptoms. Please describe what you're experiencing, and I'll provide some insights. Remember, this is for informational purposes only and not a substitute for professional medical advice.",
            "timestamp": datetime.now().strftime("%H:%M")
        }
    ]

# Header Section
st.title("🏥 Medical Symptom Assistant")
st.markdown("### Describe your symptoms for analysis")

# Medical Disclaimer
st.warning("⚠️ **Medical Disclaimer:** This tool provides general information only. Always consult a healthcare professional for medical advice and diagnosis.")

st.divider()

# Chat Display Container
chat_container = st.container()

# Display all previous messages
with chat_container:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            st.caption(f"🕒 {message['timestamp']}")

# User Input Box
user_input = st.chat_input("Describe your symptoms here...")

# Handle user input
if user_input:
    # Get current timestamp
    timestamp = datetime.now().strftime("%H:%M")
    
    # Add user message to chat history
    st.session_state.messages.append({
        "role": "user",
        "content": user_input,
        "timestamp": timestamp
    })
    
    # Display user message
    with chat_container:
        with st.chat_message("user"):
            st.markdown(user_input)
            st.caption(f"🕒 {timestamp}")
    
    # Show loading spinner while processing
    with st.spinner("🔍 Analyzing your symptoms..."):
        # TODO: Call your colleague's backend function here
        
        bot_response = analyze_symptoms(
            user_input,
            history=st.session_state.messages
        )
    
    # Add bot response to chat history
    bot_timestamp = datetime.now().strftime("%H:%M")
    st.session_state.messages.append({
        "role": "assistant",
        "content": bot_response,
        "timestamp": bot_timestamp
    })
    
    # Display bot message
    with chat_container:
        with st.chat_message("assistant"):
            st.markdown(bot_response)
            st.caption(f"🕒 {bot_timestamp}")
    
    # Refresh the page to show new messages
    st.rerun()

# ============================================
# Sidebar with Instructions
# ============================================

with st.sidebar:
    st.header("ℹ️ How to Use")
    st.markdown("""
    1. **Type** your symptoms in the chat box below
    2. **Press Enter** to send your message
    3. **Wait** for the AI to analyze
    4. **Review** the diagnosis and recommendations
    """)
    
    st.divider()
    
    st.header("📋 Tips for Better Results")
    st.markdown("""
    - Be **specific** about your symptoms
    - Mention **duration** (e.g., "for 3 days")
    - Include **severity** (mild/moderate/severe)
    - List **all symptoms** you're experiencing
    - Mention any **medications** you're taking
    """)
    
    st.divider()
    
    st.header("💡 Example Inputs")
    st.info("""
    ✓ "I have a fever of 101°F, dry cough, and body aches for 2 days"
    
    ✓ "Severe headache on left side, sensitivity to light, nausea"
    
    ✓ "Stomach cramps, diarrhea, and mild fever since yesterday"
    """)
    
    st.divider()
    
    # Statistics
    st.header("📊 Session Info")
    message_count = len(st.session_state.messages)
    user_messages = len([m for m in st.session_state.messages if m["role"] == "user"])
    st.metric("Total Messages", message_count)
    st.metric("Your Messages", user_messages)
    
    st.divider()
    
    # Clear chat button
    if st.button("🗑️ Clear Chat History", type="primary", use_container_width=True):
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "Hello! I'm here to help you understand your symptoms. Please describe what you're experiencing.",
                "timestamp": datetime.now().strftime("%H:%M")
            }
        ]
        st.rerun()
    
    st.divider()
    
    # Footer
    st.caption("💻 Built with Streamlit")
    st.caption("🏥 Medical Symptom Assistant v1.0")