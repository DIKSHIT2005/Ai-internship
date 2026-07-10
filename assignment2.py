# Ai Multiverse Chatbot 

import streamlit as st
from google import genai
import os
from dotenv import load_dotenv

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="AI Multiverse Chatbot",
    page_icon="🤖",
    layout="centered"
)

# -------------------- LOAD API --------------------
load_dotenv()

client = genai.Client(api_key=os.getenv("api_key"))

# -------------------- CUSTOM CSS --------------------
st.markdown("""
<style>
.main {
    background-color: #f5f7fa;
}
h1 {
    text-align: center;
    color: #4F46E5;
}
.stButton>button {
    width: 100%;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# -------------------- TITLE --------------------
st.title("🤖 AI Multiverse Chatbot")
st.caption("Talk with different AI personalities!")

# -------------------- SIDEBAR --------------------
with st.sidebar:
    st.header("⚙️ Settings")

    personality = st.selectbox(
        "Choose Personality",
        [
            "A common Indian man frustrated by the government",
            "A crazy football fan",
            "A little boy who believes the world is a game",
            "A friendly teacher",
            "A Python coding expert",
            "A motivational speaker"
        ]
    )

    if st.button("🗑 Clear Chat"):
        st.session_state.chat_history = []

# -------------------- SESSION STATE --------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# -------------------- INPUT --------------------
user_message = st.text_input("💬 Start the conversation:")

# -------------------- SEND BUTTON --------------------
if st.button("🚀 Send"):

    if user_message.strip() != "":

        prompt = f"""
You are acting as: {personality}

Stay completely in character.

User: {user_message}
"""

        with st.spinner("🤔 Thinking..."):

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

            ai_reply = response.text

            st.session_state.chat_history.append(
                ("🧑 You", user_message)
            )
            st.session_state.chat_history.append(
                ("🤖 AI", ai_reply)
            )

    else:
        st.warning("Please enter a message.")

# -------------------- CHAT HISTORY --------------------
if st.session_state.chat_history:

    st.subheader("💬 Chat History")

    for sender, message in st.session_state.chat_history:
        st.markdown(f"**{sender}:** {message}")

# -------------------- STATS --------------------
if st.session_state.chat_history:

    st.divider()

    st.subheader("📊 Chat Statistics")

    total_messages = len(st.session_state.chat_history) // 2

    st.write(f"Total Conversations : **{total_messages}**")

# -------------------- DOWNLOAD CHAT --------------------
if st.session_state.chat_history:

    chat = ""

    for sender, message in st.session_state.chat_history:
        chat += f"{sender}: {message}\n\n"

    st.download_button(
        "📥 Download Chat",
        chat,
        file_name="chat_history.txt"
    )

# -------------------- FOOTER --------------------
st.markdown("---")
st.caption("Made with ❤️ using Streamlit + Gemini AI")