import os
import time
import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Page Config
st.set_page_config(page_title="AI Prompt Consultant", page_icon="🤖", layout="wide")

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

system_prompt = """
Aap ek Senior Prompt Engineering Consultant hain. 
Aapka kaam user ko AI Prompts write, refine aur optimize karne mein madad karna hai.
Hamesha professional, concise aur clear tone mein Urdu/Hindi-English (Roman) mix mein jawab dein.
"""

# Header
st.title("🤖 AI Prompt Engineering Consultant")
st.caption("Professional Prompt Generator & Marketing Copy Architecture")

# Sidebar - Preset Library
st.sidebar.header("🎯 Quick Prompt Presets")
st.sidebar.write("In buttons par click karke direct prompt template load karein:")

# Chat History Setup
if "messages" not in st.session_state:
    st.session_state.messages = []

# Function with Stable Fallback Endpoints
def handle_prompt(prompt_text):
    if prompt_text:
        st.session_state.messages.append({"role": "user", "content": prompt_text})
        
        bot_reply = None
        # Stable production models array
        models_to_try = ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-3.8-flash"]
        
        for model_name in models_to_try:
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt_text,
                    config=types.GenerateContentConfig(
                        system_instruction=system_prompt,
                        temperature=0.7,
                    )
                )
                bot_reply = response.text
                if bot_reply:
                    break
            except Exception as e:
                time.sleep(1)
                continue

        if not bot_reply:
            bot_reply = "API connection active hai lekin server temporary unavailable hai. 10-15 seconds baad dobara try karein."

        st.session_state.messages.append({"role": "assistant", "content": bot_reply})

# Sidebar Buttons
if st.sidebar.button("📦 E-commerce Product Description"):
    handle_prompt("Mujhe ek e-commerce product description ke liye high-converting master prompt bana kar do.")

if st.sidebar.button("📢 Facebook Ad Copy (R+G+A+F+O)"):
    handle_prompt("Mujhe R + G + A + F + O framework par based Facebook Ad copy ka master prompt bana kar do.")

if st.sidebar.button("🎬 CapCut / Reel Script Prompt"):
    handle_prompt("Mujhe short video (Reels/TikTok) script ke liye engaging prompt architecture tayar karke do.")

if st.sidebar.button("🎨 Photoshop/Canva Banner Prompt"):
    handle_prompt("Mujhe graphic designer ke liye ad banner visual description aur text layout prompt bana kar do.")

if st.sidebar.button("🗑️ Clear Chat History"):
    st.session_state.messages = []
    st.rerun()

# Render Chat History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Bottom Chat Input Box
user_input = st.chat_input("Apni requirement batayein...")
if user_input:
    handle_prompt(user_input)
    st.rerun()