import streamlit as st
import requests

# Backend API URL (Docker Compose networking will resolve "backend" as hostname)
BACKEND_URL = "http://backend:8000/analyze"

# ---- PAGE CONFIG ----
st.set_page_config(page_title="Tweet Sentiment Analyzer", page_icon="🐦", layout="centered")

# ---- CUSTOM DARK THEME CSS ----
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #141e30, #243b55);
        font-family: "Segoe UI", sans-serif;
        color: #f1f1f1;
    }
    .title {
        font-size: 2.6rem;
        font-weight: bold;
        color: #f9fafb;
        text-align: center;
        margin-bottom: 10px;
    }
    .subtitle {
        text-align: center;
        font-size: 1.1rem;
        color: #d1d5db;
        margin-bottom: 25px;
    }
    textarea, .stTextInput > div > div > input {
        background-color: rgba(255,255,255,0.08) !important;
        color: #f1f1f1 !important;
        border: 1px solid #4b5563 !important;
        border-radius: 12px !important;
        font-size: 1rem !important;
    }
    textarea::placeholder {
        color: #9ca3af !important;
    }
    .stButton > button {
        background: linear-gradient(90deg, #06b6d4, #3b82f6);
        color: white !important;
        border: none;
        border-radius: 12px;
        padding: 0.6em 1.4em;
        font-size: 1rem;
        font-weight: 600;
        transition: 0.3s;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.3);
    }
    .stButton > button:hover {
        background: linear-gradient(90deg, #0891b2, #2563eb);
        transform: scale(1.04);
        box-shadow: 0px 6px 20px rgba(0,0,0,0.5);
    }
    .card {
        background: rgba(255,255,255,0.08);
        backdrop-filter: blur(10px);
        padding: 25px;
        border-radius: 18px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.4);
        margin-top: 25px;
    }
    .positive {
        color: #22c55e;
        font-weight: bold;
    }
    .negative {
        color: #ef4444;
        font-weight: bold;
    }
    .neutral {
        color: #9ca3af;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---- APP HEADER ----
st.markdown('<div class="title">🐦 Tweet Sentiment Analyzer</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Analyze the sentiment of any tweet in real-time with our AI-powered backend</div>', unsafe_allow_html=True)

# ---- INPUT ----
tweet_text = st.text_area("✍️ Enter your tweet:", "", height=120, placeholder="e.g., Dark mode looks amazing 😍")

# ---- ANALYZE BUTTON ----
if st.button("🔍 Analyze Sentiment", use_container_width=True):
    if tweet_text.strip():
        try:
            response = requests.post(BACKEND_URL, json={"text": tweet_text})

            if response.status_code == 200:
                result = response.json()
                sentiment = result.get("sentiment", "Unknown").capitalize()
                compound = result.get("scores", {}).get("compound", 0.0)

                sentiment_class = (
                    "positive" if sentiment == "Positive"
                    else "negative" if sentiment == "Negative"
                    else "neutral"
                )

                # ---- RESULT CARD ----
                st.markdown(f"""
                <div class="card">
                    <h3>✅ Analysis Result</h3>
                    <p>Sentiment: <span class="{sentiment_class}">{sentiment}</span></p>
                    <p>Compound Score: <b>{compound:.2f}</b></p>
                </div>
                """, unsafe_allow_html=True)

                # Progress bar for sentiment intensity
                st.progress(min(max((compound + 1) / 2, 0), 1))

            else:
                st.error(f"⚠️ Backend error: {response.status_code} - {response.text}")

        except Exception as e:
            st.error(f"❌ Could not connect to backend: {e}")
    else:
        st.warning("⚠️ Please enter some text before analyzing.")
