# 🎨 AI Image Studio (Assignment 4)

An AI-powered image generation web app built with **Streamlit** and the **Pollinations AI API**.  
This project allows users to describe an image in natural language, customize style and resolution, and instantly generate downloadable artwork.

---

## 🚀 Project Overview

This assignment demonstrates how to build an interactive AI application using Python and REST APIs.  
Users can enter creative prompts, apply visual styles, enable prompt enhancement, and generate high-quality images from a simple web interface.

---

## ✨ Features

- 🧠 **Text-to-Image Generation** using Pollinations API
- 🖌️ **Multiple Art Styles** (Photorealistic, Anime, Vintage Victorian, Sketch)
- 📐 **Custom Image Dimensions** (width/height sliders)
- ✨ **Magic Enhance Mode** for richer, more descriptive prompts
- 🎲 **Surprise Me** random prompt generator
- 📥 **One-click PNG Download** of generated output
- 💻 **Interactive UI** built with Streamlit

---

## 🧰 Tech Stack

- **Python**
- **Streamlit**
- **Requests**
- **Pollinations AI API**

---

## 📂 Project Structure

```text
assignment 4/
├── assignment4.py
└── README.md
```

---

## ⚙️ Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/DIKSHIT2005/Ai-internship.git
   cd Ai-internship/assignment\ 4
   ```

2. **Install dependencies**
   ```bash
   pip install streamlit requests
   ```

3. **Run the app**
   ```bash
   streamlit run assignment4.py
   ```

4. Open the local Streamlit URL (usually `http://localhost:8501`) in your browser.

---

## ▶️ How to Use

1. Select an **art style** from the sidebar.
2. Set image **width** and **height**.
3. Optionally enable **Magic Enhance**.
4. Enter an image prompt in the text box.
5. Click **Generate Image**.
6. View and **download** the generated image.
7. Or click **🎲 Surprise Me!** to auto-generate from a random prompt.

---

## 🧪 Example Prompts

Try these sample ideas:

- `A futuristic samurai standing in neon rain at night`
- `A floating island with waterfalls above the clouds`
- `A tiny dragon sleeping inside a teacup`
- `A cozy cyberpunk café in Tokyo at sunset`

---

## 🎓 Learning Outcomes

Through this assignment, I practiced:

- Integrating external AI services via REST APIs
- Constructing prompts for image generation
- Designing interactive front-end controls with Streamlit
- Handling API responses and binary image display
- Creating downloadable artifacts from generated content

---

## 🔮 Future Improvements

- Add URL encoding for safer prompt handling
- Improve error messages with API response details
- Add prompt history and saved generations
- Allow more styles and presets
- Add loading metrics (generation time, retries)

---

## ✅ Assignment Status

**Completed** – Functional AI image generation app with customization, randomization, and download support.
