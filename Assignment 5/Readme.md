# 📖 StoryVerse

### AI-Powered Visual Novel

StoryVerse is an AI-powered interactive visual novel built with **Streamlit**, **Google Gemini**, **Pollinations AI**, and **Microsoft Edge TTS**.

It lets you choose a story genre and art style, then generates an engaging adventure with AI narration, illustrations, and branching choices that shape the story as you play.

---

## ✨ Features

- 🎭 Multiple story genres and artistic styles
- 🤖 AI-generated interactive storytelling with Google Gemini
- 🖼️ Scene-specific AI illustrations using Pollinations AI
- 🔊 AI narration powered by Microsoft Edge TTS
- 🎮 Branching choices that influence the story
- 📦 Structured JSON responses for reliable AI interactions
- 💾 Persistent story progression using Streamlit Session State
- ⚡ Cached Gemini client for improved performance
- 🛡️ Graceful error handling for API, image, and audio generation

---

## 🛠️ Tech Stack

- Python
- Streamlit
- Google Gemini API
- Pollinations AI
- Microsoft Edge TTS
- JSON
- Requests
- Asyncio
- python-dotenv

---

## 🚀 Getting Started

### Clone the repository

```bash
git clone <repository-url>
cd StoryVerse
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Create a `.env` file

```env
GEMINI_API_KEY=your_api_key_here
```

### Run the application

```bash
streamlit run assignment5.py
```

---

## 🎥 Demo

A demonstration video of StoryVerse is available in the **demo/** folder.

---

## 📂 Project Structure

```text
StoryVerse/
│
├── assignment5.py      # Main Streamlit application
├── README.md
├── requirements.txt
└── demo/
    └── demo.mp4
```

---

## 🧠 How It Works

1. Select a story genre and visual art style.
2. Google Gemini generates a cinematic story scene, an image prompt, and three branching choices using structured JSON.
3. Pollinations AI creates an illustration for the current scene.
4. Microsoft Edge TTS converts the narration into spoken audio.
5. Choosing an option sends the decision back to Gemini, allowing the story to continue while maintaining context.

---

## 📚 About the Project

StoryVerse was developed as **Assignment 5** for the **MirAI School of Technology – Virtual Summer Internship 2026**.

The project showcases:

- Prompt engineering for structured AI outputs
- JSON-based response parsing
- Multi-modal AI integration (Text + Image + Audio)
- Dynamic AI-driven storytelling
- Stateful application development with Streamlit
- Session-based conversation management
- Dynamic UI generation
- Robust exception handling
