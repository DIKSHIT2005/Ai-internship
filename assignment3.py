import streamlit as st
from google import genai
import os
from dotenv import load_dotenv

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Multiverse Chatbot",
    page_icon="🤖"
)

st.title("🤖 AI Multiverse Chatbot")
st.caption("Chat with different AI personalities!")

# ---------------- LOAD API ----------------
load_dotenv()

client = genai.Client(api_key=os.getenv("api_key"))

# ---------------- MEMORY VAULT ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.header("⚙️ Choose Personality")

    personality = st.selectbox(
        "Select AI Personality",
        [
            "A common Indian man frustrated by the government",
            "A crazy Salman Khan fan",
            "A little boy who believes the world is a game",
            "A friendly teacher",
            "A Python coding expert",
            "A motivational speaker"
        ]
    )

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# ---------------- DISPLAY CHAT HISTORY ----------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ---------------- CHAT INPUT ----------------
if user_message := st.chat_input("Say something..."):

    # Save user message
    st.session_state.messages.append(
        {"role": "user", "content": user_message}
    )

    with st.chat_message("user"):
        st.markdown(user_message)

    prompt = f"""
You are acting as {personality}.

Stay completely in character.

User: {user_message}
"""

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

            st.markdown(response.text)

    # Save AI response
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response.text
        }
    )