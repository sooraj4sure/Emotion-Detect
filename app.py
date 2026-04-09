import streamlit as st
import joblib
import re
import string
import random

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="MoodLens – Emotion Detection",
    page_icon="🧠",
    layout="centered"
)

# -----------------------------
# Load saved files
# -----------------------------
model = joblib.load('model.pkl')
vectorizer = joblib.load('vectorizer.pkl')
label_map = joblib.load('label_mapping.pkl')

reverse_map = {v: k for k, v in label_map.items()}

# -----------------------------
# Emotion Config
# -----------------------------
EMOTION_CONFIG = {
    "sadness": {
        "emoji": "😢",
        "color": "#4A90D9",
        "bg": "#EBF4FF",
        "border": "#4A90D9",
        "label": "Sadness",
        "message": "It's okay to feel sad. Your feelings are valid, and this too shall pass. 💙",
        "suggestions": [
            "🎵  Put on your favorite comfort playlist and let yourself feel.",
            "📓  Write down what's bothering you — journaling can help untangle your thoughts.",
            "🚶  Take a slow walk outside, even 10 minutes of fresh air can shift your mood.",
            "📞  Reach out to a trusted friend or family member — you don't have to carry this alone.",
            "🛁  Give yourself a self-care break: warm tea, a cozy blanket, a feel-good movie.",
            "🌱  Remember: sadness is temporary. Be gentle with yourself today.",
        ],
        "quote": "\"Even the darkest night will end and the sun will rise.\" – Victor Hugo"
    },
    "anger": {
        "emoji": "😠",
        "color": "#E05C2E",
        "bg": "#FFF1EC",
        "border": "#E05C2E",
        "label": "Anger",
        "message": "Your anger is telling you something important. Let's channel it constructively. 🔥",
        "suggestions": [
            "🧘  Try box breathing: inhale 4s → hold 4s → exhale 4s → hold 4s. Repeat 4 times.",
            "🏃  Go for a run or do a quick workout — physical movement burns off adrenaline fast.",
            "✍️  Write an unsent letter to whoever/whatever upset you. Get it all out, then delete it.",
            "🥊  Punch a pillow, scream into it, or squeeze a stress ball — release the tension safely.",
            "⏳  Give yourself a 10-minute pause before responding to any situation that sparked this.",
            "🌊  Splash cold water on your face — it activates your dive reflex and calms your body.",
        ],
        "quote": "\"Speak when you are angry and you will make the best speech you will ever regret.\" – Ambrose Bierce"
    },
    "love": {
        "emoji": "❤️",
        "color": "#D44F7A",
        "bg": "#FFF0F5",
        "border": "#D44F7A",
        "label": "Love",
        "message": "What a beautiful feeling! Love is one of the greatest things we can experience. 💕",
        "suggestions": [
            "💌  Write a heartfelt note or message to someone you care about — make their day!",
            "📸  Look through old photos and relive your favourite memories with loved ones.",
            "🍳  Cook or bake something special for someone you love.",
            "🤗  Give someone a long, genuine hug — it boosts oxytocin for both of you.",
            "🌸  Do a random act of kindness today — spread the love outward.",
            "📖  Read a romantic novel or watch a feel-good love story to savour this feeling.",
        ],
        "quote": "\"The best thing to hold onto in life is each other.\" – Audrey Hepburn"
    },
    "surprise": {
        "emoji": "😲",
        "color": "#8A50D6",
        "bg": "#F5F0FF",
        "border": "#8A50D6",
        "label": "Surprise",
        "message": "Life just threw something unexpected at you! Embrace the spontaneity. ✨",
        "suggestions": [
            "🗺️  Lean into it — explore the unexpected thing further, it might be a gift in disguise.",
            "📝  Jot down what just happened while it's fresh — your future self will love reading it.",
            "🧩  If the surprise is unsettling, break it down into manageable pieces before reacting.",
            "🎲  Try something spontaneous today to match the energy — try a new food, take a detour.",
            "💬  Share your surprise with a friend — reactions are more fun when shared!",
            "🌀  Sit with the feeling for a moment — surprises often carry hidden lessons.",
        ],
        "quote": "\"Life is what happens when you're busy making other plans.\" – John Lennon"
    },
    "fear": {
        "emoji": "😨",
        "color": "#5B7FA6",
        "bg": "#EEF4FB",
        "border": "#5B7FA6",
        "label": "Fear",
        "message": "Fear means you're about to do something brave. You're not alone in this. 🤝",
        "suggestions": [
            "🌬️  Try 4-7-8 breathing: inhale 4s, hold 7s, exhale 8s — it calms your nervous system.",
            "🔦  Name the fear out loud or write it down — vague fears shrink when you face them.",
            "🧱  Break down the scary thing into the smallest possible first step. Just do that one step.",
            "👣  Talk to someone who's been through something similar — their experience is your compass.",
            "🏡  Create a safety anchor: hold something familiar, sit in a comfortable space, ground yourself.",
            "💪  Remind yourself of 3 hard things you've already survived. You're stronger than you know.",
        ],
        "quote": "\"Courage is not the absence of fear, but the triumph over it.\" – Nelson Mandela"
    },
    "joy": {
        "emoji": "😄",
        "color": "#E8A020",
        "bg": "#FFFBEC",
        "border": "#E8A020",
        "label": "Joy",
        "message": "You're radiating good energy! Celebrate this moment fully. 🎉",
        "suggestions": [
            "🎉  Celebrate! Do a little dance, treat yourself — you deserve to enjoy this.",
            "📸  Capture this moment — take a photo, write a note, document the feeling.",
            "🌟  Share your joy with someone — call a friend and spread the good vibes.",
            "🎨  Use this energy creatively — draw, write, play music, or start that project you've delayed.",
            "🌳  Go outside and soak up the world — a happy walk in nature amplifies the feeling.",
            "🙏  Take a moment to reflect on what's going well — gratitude deepens joy.",
        ],
        "quote": "\"Joy is not in things; it is in us.\" – Richard Wagner"
    },
}

# -----------------------------
# Text cleaning function
# -----------------------------
def clean_text(text):
    text = text.lower()
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# -----------------------------
# Prediction function
# -----------------------------
def predict_emotion(text):
    text = clean_text(text)
    text_vec = vectorizer.transform([text])
    pred = model.predict(text_vec)[0]
    return reverse_map[pred]

# -----------------------------
# Custom CSS
# -----------------------------
st.markdown("""
<style>
    /* Main container */
    .main { padding-top: 1rem; }

    /* Header */
    .app-header {
        text-align: center;
        padding: 2rem 1rem 1rem;
        margin-bottom: 1.5rem;
    }
    .app-header h1 {
        font-size: 2.2rem;
        font-weight: 700;
        margin: 0;
        background: linear-gradient(135deg, #6C63FF, #FF6584);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .app-header p {
        color: #888;
        font-size: 1rem;
        margin-top: 0.4rem;
    }

    /* Text area */
    .stTextArea textarea {
        border-radius: 12px !important;
        border: 1.5px solid #e0e0e0 !important;
        font-size: 1rem !important;
        padding: 1rem !important;
        transition: border-color 0.2s;
    }
    .stTextArea textarea:focus {
        border-color: #6C63FF !important;
        box-shadow: 0 0 0 3px rgba(108, 99, 255, 0.15) !important;
    }

    /* Button */
    .stButton > button {
        width: 100%;
        border-radius: 12px !important;
        padding: 0.7rem 1.5rem !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        background: linear-gradient(135deg, #6C63FF, #FF6584) !important;
        color: white !important;
        border: none !important;
        transition: opacity 0.2s, transform 0.1s;
    }
    .stButton > button:hover {
        opacity: 0.92;
        transform: translateY(-1px);
    }

    /* Result card */
    .result-card {
        border-radius: 16px;
        padding: 1.5rem;
        margin-top: 1.5rem;
        border-left: 5px solid;
    }
    .emotion-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        font-size: 1.4rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    .emotion-message {
        font-size: 0.95rem;
        color: #555;
        margin-bottom: 1rem;
        font-style: italic;
    }
    .suggestion-header {
        font-size: 0.85rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #999;
        margin-bottom: 0.6rem;
    }
    .suggestion-item {
        background: white;
        border-radius: 10px;
        padding: 0.65rem 0.9rem;
        margin-bottom: 0.5rem;
        font-size: 0.92rem;
        color: #333;
        border: 1px solid #f0f0f0;
        line-height: 1.5;
    }
    .quote-box {
        margin-top: 1.2rem;
        padding: 0.8rem 1rem;
        border-radius: 10px;
        background: rgba(0,0,0,0.03);
        font-size: 0.85rem;
        color: #777;
        font-style: italic;
        border-left: 3px solid #ddd;
    }

    /* History section */
    .history-item {
        background: #fafafa;
        border-radius: 10px;
        padding: 0.6rem 0.9rem;
        margin-bottom: 0.4rem;
        font-size: 0.88rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border: 1px solid #eee;
    }
    .history-text { color: #444; flex: 1; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
    .history-emotion { font-weight: 600; margin-left: 0.8rem; }

    /* Footer */
    .footer {
        text-align: center;
        color: #bbb;
        font-size: 0.8rem;
        margin-top: 3rem;
        padding-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Session state
# -----------------------------
if "history" not in st.session_state:
    st.session_state.history = []

# -----------------------------
# Header
# -----------------------------
st.markdown("""
<div class="app-header">
    <h1>🧠 MoodLens</h1>
    <p>Detect the emotion behind your words and get personalised support</p>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# Input section
# -----------------------------
user_input = st.text_area(
    "How are you feeling? Share what's on your mind...",
    placeholder="e.g. I've been feeling really overwhelmed lately and don't know what to do...",
    height=140,
    label_visibility="visible"
)

col1, col2 = st.columns([3, 1])
with col1:
    predict_btn = st.button("✨ Detect My Emotion", use_container_width=True)
with col2:
    clear_btn = st.button("🗑️ Clear", use_container_width=True)

if clear_btn:
    st.rerun()

# -----------------------------
# Prediction + Result
# -----------------------------
if predict_btn:
    if user_input.strip() == "":
        st.warning("⚠️ Please enter some text before predicting.")
    else:
        with st.spinner("Analysing your emotion..."):
            emotion = predict_emotion(user_input)

        config = EMOTION_CONFIG.get(emotion, EMOTION_CONFIG["joy"])

        # Save to history
        preview = user_input[:60] + ("..." if len(user_input) > 60 else "")
        st.session_state.history.insert(0, {
            "text": preview,
            "emotion": emotion,
            "emoji": config["emoji"]
        })
        if len(st.session_state.history) > 5:
            st.session_state.history = st.session_state.history[:5]

        # Pick 3 random suggestions
        tips = random.sample(config["suggestions"], min(3, len(config["suggestions"])))

        # Render result card
        suggestions_html = "".join(
            f'<div class="suggestion-item">{tip}</div>' for tip in tips
        )

        st.markdown(f"""
        <div class="result-card" style="background:{config['bg']}; border-color:{config['border']};">
            <div class="emotion-badge" style="color:{config['color']};">
                {config['emoji']} {config['label']} Detected
            </div>
            <div class="emotion-message">{config['message']}</div>
            <div class="suggestion-header">💡 What you can do right now</div>
            {suggestions_html}
            <div class="quote-box">{config['quote']}</div>
        </div>
        """, unsafe_allow_html=True)

# -----------------------------
# Emotion Guide
# -----------------------------
with st.expander("📊 Emotion Guide — what can this detect?"):
    cols = st.columns(3)
    emotions_list = list(EMOTION_CONFIG.items())
    for i, (key, val) in enumerate(emotions_list):
        with cols[i % 3]:
            st.markdown(f"""
            <div style="text-align:center; padding: 0.8rem; border-radius: 12px;
                        background:{val['bg']}; border: 1px solid {val['border']}20; margin-bottom:0.5rem;">
                <div style="font-size:1.8rem;">{val['emoji']}</div>
                <div style="font-weight:600; color:{val['color']}; font-size:0.9rem;">{val['label']}</div>
            </div>
            """, unsafe_allow_html=True)

# -----------------------------
# Recent History
# -----------------------------
if st.session_state.history:
    st.markdown("#### 🕘 Recent Detections")
    for item in st.session_state.history:
        st.markdown(f"""
        <div class="history-item">
            <span class="history-text">"{item['text']}"</span>
            <span class="history-emotion">{item['emoji']} {item['emotion'].capitalize()}</span>
        </div>
        """, unsafe_allow_html=True)

# -----------------------------
# Footer
# -----------------------------