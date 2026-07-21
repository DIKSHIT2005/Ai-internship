import streamlit as st
import os
from google import genai
from dotenv import load_dotenv
import json
import edge_tts
import asyncio
import requests

# Setting pgae configurations
st.set_page_config(
    page_title="StoryVerse",
    page_icon="📖",
    layout="centered",
    initial_sidebar_state="expanded"
)

load_dotenv()

st.title("📖 StoryVerse")
st.subheader("AI-Powered Visual Novel")
st.caption(
    "Create immersive adventures with AI-generated stories, artwork, and narration."
)

# Phase 1: The Director's Cut (UI & Configuration)
# Cache the Gemini client so Streamlit doesn't recreate it on every rerun
@st.cache_resource
def get_ai_client():
    return genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

client = get_ai_client()

# Phase 4.2: Multi-Media Rendering (TTS)
# Generate AI narration using Microsoft Edge TTS
async def generate_audio(text):
    communicate = edge_tts.Communicate(
        text=text,
        voice="en-US-AndrewNeural"
    )

    await communicate.save("story.mp3")


# Phase 1: The Director's Cut (UI & Configuration)
# Configure the story settings from the sidebar
st.sidebar.header("🎮 Story Settings")

story_genre = st.sidebar.selectbox(
    "📚 Story Genre",
    [
        "Dark Fantasy",
        "Cyberpunk Thriller",
        "Post-Apocalyptic Survival",
        "Psychological Horror",
        "Space Opera",
        "Mythological Adventure",
        "Detective Mystery",
        "Time Travel"
    ],
    help="Choose the world your AI adventure will take place in."
)

art_style = st.sidebar.selectbox(
    "🎨 Art Style",
    [
        "Anime",
        "Cinematic Realism",
        "Studio Ghibli",
        "Comic Book",
        "Pixel Art",
        "Dark Gothic",
        "Fantasy Concept Art",
        "Oil Painting"
    ],
    help="Choose the artistic style for AI-generated illustrations."
)

start_story = st.sidebar.button(
    "🎮 Start New Story",
    use_container_width=True
)

# Phase 1: The Director's Cut (UI & Configuration)
# Create a persistent Gemini chat session
if "gemini_chat" not in st.session_state:
    st.session_state.gemini_chat = client.chats.create(
        model="gemini-2.5-flash"
    )


# Phase 2: The Structured JSON Engine
# Generate a new interactive story and parse the AI's JSON response
if start_story:
    st.session_state.gemini_chat = client.chats.create(
        model="gemini-2.5-flash"
    )

    # Phase 5: Graceful Failures
    # Prevent the app from crashing if the Gemini API fails
    try:
        with st.spinner("✨ Generating story, artwork, and narration..."):
            response = st.session_state.gemini_chat.send_message(
                f"""
                Create the opening scene of an original interactive visual novel in the {story_genre} genre.

                Requirements:
                - Begin with a strong hook that immediately creates curiosity.
                - Write in second person ("You...") so the reader feels involved.
                - Describe the setting using vivid sensory details.
                - Introduce a clear objective, mystery, or conflict.
                - Keep the narration cinematic, immersive, and suitable for audiobook narration.
                - Use varied sentence lengths and natural flow.
                - Keep the story between 120 and 180 words.
                - End with a meaningful decision point.

                Generate an image_prompt that accurately represents THIS exact story scene.

                The image prompt must include:
                - Main character appearance
                - Environment
                - Lighting
                - Mood
                - Camera angle
                - Color palette
                - Important objects
                - Atmospheric details

                Write the image prompt as a high-quality AI image generation prompt in {art_style} style.
                Do not mention text, captions, UI elements, speech bubbles, or watermarks.

                Generate exactly three choices.

                Each choice must:
                - Meaningfully change the story
                - Be under 10 words
                - Sound like an action
                - Be unique from the others

                Respond ONLY with valid JSON.

                The JSON must contain:

                {{
                    "title": "...",
                    "story_text": "...",
                    "image_prompt": "...",
                    "options": [
                        "...",
                        "...",
                        "..."
                    ]
                }}

                No markdown.
                No code fences.
                No explanations.
                Return only JSON that can be parsed by json.loads().
                """
            )

            story = json.loads(response.text)
            st.session_state.story = story

    except Exception:
        st.toast("⚠️ Story generation failed. Please try again in a moment.")


# Show instructions before the first story is created
if "story" not in st.session_state:
    st.info(
        """
    👈 **Choose your adventure**

    1. Select a story genre.
    2. Pick an art style.
    3. Click **Start New Story**.
    4. Make choices to shape your own adventure.
    """
    )

# Display the current story once it exists
if "story" in st.session_state:

    title = st.session_state.story["title"]
    story_text = st.session_state.story["story_text"]
    image_prompt = st.session_state.story["image_prompt"]
    options = st.session_state.story["options"]

    # Improve image quality by adding extra descriptive keywords
    image_prompt += ", ultra detailed, masterpiece, cinematic lighting, dramatic composition, highly detailed environment, professional concept art, 8k"

    # Phase 4.1: Multi-Media Rendering (Visuals)
    # Generate and display the AI story illustration
    image_url = f"https://image.pollinations.ai/prompt/{image_prompt}"

    # Phase 5: Graceful Failures
    # Continue the story even if image generation fails
    try:
        image = requests.get(image_url)
        image.raise_for_status()

        st.image(
            image.content,
            caption=f"{title} • AI-generated artwork",
            use_container_width=True
        )

    except Exception:
        st.toast("🖼️ Image server is busy, skipping visual...")


    # Phase 3: Dynamic UI Generation
    # Display the current story scene
    st.header(title)
    st.subheader("Story")
    st.write(story_text)


    # Phase 4.2: Multi-Media Rendering (TTS)
    # Generate and play AI narration
    try:
        asyncio.run(generate_audio(story_text))
        st.audio("story.mp3")

    # Phase 5: Graceful Failures
    # Continue the story even if audio generation fails
    except Exception:
        st.toast("🔊 Audio could not be generated.")


    # Phase 3: Dynamic UI Generation
    # Display interactive choices for the next scene
    st.subheader("Choose your next move")

    for option in options:
        if st.button(option):

            with st.spinner("✨ Writing the next chapter..."):
                
                # Phase 5: Graceful Failures
                # Prevent the app from crashing while continuing the story
                try:
                    response = st.session_state.gemini_chat.send_message(
                        f"""
                        The player chose: {option}

                        Continue the existing {story_genre} story.

                        Requirements:
                        - Continue naturally from the previous scene.
                        - Never restart the story.
                        - Maintain the same characters, setting, tone, and unresolved mysteries.
                        - Build upon previous events.
                        - Write in second person ("You...").
                        - Keep the narration cinematic, immersive, and suitable for audiobook narration.
                        - Use vivid but concise descriptions.
                        - Keep the story between 120 and 180 words.
                        - End with another meaningful decision point.

                        Generate an image_prompt that accurately represents THIS exact scene.

                        Keep the main character visually consistent across scenes unless the story explicitly changes their appearance.

                        The image prompt must include:
                        - Main character appearance
                        - Environment
                        - Lighting
                        - Mood
                        - Camera angle
                        - Color palette
                        - Important objects
                        - Atmospheric details

                        Write the image prompt as a high-quality AI image generation prompt in {art_style} style.
                        Do not mention text, captions, UI elements, speech bubbles, or watermarks.

                        Generate exactly three choices.

                        Each choice must:
                        - Meaningfully change the story
                        - Be under 10 words
                        - Sound like an action
                        - Be unique from the others

                        Respond ONLY with valid JSON.

                        The JSON must contain:

                        {{
                            "title": "...",
                            "story_text": "...",
                            "image_prompt": "...",
                            "options": [
                                "...",
                                "...",
                                "..."
                            ]
                        }}

                        No markdown.
                        No code fences.
                        No explanations.
                        Return only JSON that can be parsed by json.loads().
                        """
                    )

                    story = json.loads(response.text)
                    st.session_state.story = story

                    st.rerun()

                except Exception:
                    st.toast("📖 Couldn't continue the story. Please try again.")
