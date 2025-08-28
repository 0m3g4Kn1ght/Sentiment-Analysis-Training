import streamlit as st
import requests
import pandas as pd

# Backend API base URL
BASE_URL = "http://localhost:8000"

# ---- PAGE CONFIG ----
st.set_page_config(page_title="Tweet Sentiment Analyzer", layout="centered")

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

# ---- SESSION STATE ----
if "account_id" not in st.session_state:
    st.session_state.account_id = None
if "is_admin" not in st.session_state:
    st.session_state.is_admin = False
if "page" not in st.session_state:
    st.session_state.page = "Login"


# ---- PAGE ROUTING ----
def login_page():
    st.markdown('<div class="title">Login</div>', unsafe_allow_html=True)
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login", use_container_width=True):
        resp = requests.post(f"{BASE_URL}/login", json={"username": username, "password": password})
        if resp.status_code == 200:
            data = resp.json()
            st.session_state.account_id = data["account_id"]
            st.session_state.page = "Analyze"
            # check admin
            try:
                admin_check = requests.get(f"{BASE_URL}/admin/{st.session_state.account_id}")
                st.session_state.is_admin = admin_check.status_code == 200
            except:
                st.session_state.is_admin = False
            st.success("Login successful")
        else:
            st.error(resp.json().get("detail", "Login failed"))

    if st.button("Go to Register", use_container_width=True):
        st.session_state.page = "Register"


def register_page():
    st.markdown('<div class="title">Register</div>', unsafe_allow_html=True)
    username = st.text_input("New Username")
    password = st.text_input("New Password", type="password")

    if st.button("Register", use_container_width=True):
        resp = requests.post(f"{BASE_URL}/register", json={"username": username, "password": password})
        if resp.status_code == 200:
            st.success("Registration successful. Please log in.")
            st.session_state.page = "Login"
        else:
            st.error(resp.json().get("detail", "Registration failed"))

    if st.button("Back to Login", use_container_width=True):
        st.session_state.page = "Login"


def analyze_page():
    st.markdown('<div class="title">Tweet Sentiment Analyzer</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Analyze the sentiment of any tweet in real-time</div>', unsafe_allow_html=True)

    tweet_text = st.text_area("Enter your tweet:", "", height=120, placeholder="e.g., Dark mode looks amazing")

    if st.button("Analyze Sentiment", use_container_width=True):
        if tweet_text.strip():
            try:
                resp = requests.post(f"{BASE_URL}/analyze", json={"account_id": st.session_state.account_id, "text": tweet_text})
                if resp.status_code == 200:
                    result = resp.json()
                    sentiment = result.get("sentiment", "Unknown").capitalize()

                    sentiment_class = (
                        "positive" if sentiment == "Positive"
                        else "negative" if sentiment == "Negative"
                        else "neutral"
                    )

                    st.markdown(f"""
                    <div class="card">
                        <h3>Analysis Result</h3>
                        <p>Sentiment: <span class="{sentiment_class}">{sentiment}</span></p>
                    </div>
                    """, unsafe_allow_html=True)

                else:
                    st.error(f"Error: {resp.json().get('detail', 'Backend error')}")

            except Exception as e:
                st.error(f"Could not connect to backend: {e}")
        else:
            st.warning("Please enter some text before analyzing.")

    if st.button("View History", use_container_width=True):
        st.session_state.page = "History"
    if st.session_state.is_admin and st.button("Admin Panel", use_container_width=True):
        st.session_state.page = "Admin"
    if st.button("Logout", use_container_width=True):
        requests.post(f"{BASE_URL}/logout", params={"account_id": st.session_state.account_id})
        st.session_state.account_id = None
        st.session_state.page = "Login"


def history_page():
    st.markdown('<div class="title">History</div>', unsafe_allow_html=True)
    try:
        resp = requests.get(f"{BASE_URL}/history/{st.session_state.account_id}")
        if resp.status_code == 200:
            history = resp.json().get("history", [])
            if history:
                df = pd.DataFrame(history)
                st.dataframe(df, use_container_width=True)
            else:
                st.info("No history available.")
        else:
            st.error("Could not fetch history.")
    except Exception as e:
        st.error(f"Error fetching history: {e}")

    if st.button("Back", use_container_width=True):
        st.session_state.page = "Analyze"


def admin_page():
    st.markdown('<div class="title">Admin Panel</div>', unsafe_allow_html=True)
    try:
        resp = requests.get(f"{BASE_URL}/admin/{st.session_state.account_id}")
        if resp.status_code == 200:
            users = resp.json().get("users", [])
            df = pd.DataFrame(users)
            st.dataframe(df, use_container_width=True)
        else:
            st.error(resp.json().get("detail", "Not authorized"))
    except Exception as e:
        st.error(f"Error loading admin panel: {e}")

    if st.button("Back", use_container_width=True):
        st.session_state.page = "Analyze"


# ---- MAIN ----
if st.session_state.page == "Login":
    login_page()
elif st.session_state.page == "Register":
    register_page()
elif st.session_state.page == "Analyze":
    analyze_page()
elif st.session_state.page == "History":
    history_page()
elif st.session_state.page == "Admin":
    admin_page()
