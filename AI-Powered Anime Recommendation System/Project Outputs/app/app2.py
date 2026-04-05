# AniBaba Streamlit Application
# Run with: streamlit run app/app2.py
# NOTE: Cannot be run inside a Jupyter/Colab notebook cell directly.

import streamlit as st
from pipeline.pipeline import AnimeRecommendationPipeline
from dotenv import load_dotenv
from utils.bgimage import set_background

st.set_page_config(
    page_title="AniBaba | AI Anime Recommender",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded"
)

load_dotenv()
set_background('imgs/bg.png')

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Outfit', sans-serif; }
    .title-text {
        background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-size: 3rem; font-weight: 700; text-align: center; margin-bottom: 0.5rem;
    }
    .subtitle-text { text-align: center; color: #aaaaaa; font-size: 1.2rem; margin-bottom: 3rem; }
    .stChatMessage {
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 15px; padding: 10px; margin-bottom: 10px;
    }
    section[data-testid="stSidebar"] { background-color: #1a1a1a; border-right: 1px solid #333; }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def init_pipeline():
    return AnimeRecommendationPipeline()

pipeline = init_pipeline()

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Konnichiwa! 🌸 I'm AniBaba. Tell me what kind of anime you're looking for, or ask me about specific titles!"}
    ]

with st.sidebar:
    st.title("🏯 Control Center")
    if st.button("Clear Conversation", type="primary", use_container_width=True):
        st.session_state.messages = [{"role": "assistant", "content": "History cleared! What shall we watch next?"}]
        st.rerun()
    st.divider()
    st.markdown("### 💡 Tips")
    st.info(
        "Try asking for:\n"
        "- *'Dark fantasy anime like Attack on Titan'*\n"
        "- *'Wholesome romance taking place in high school'*\n"
        "- *'Cyberpunk sci-fi with mind-bending plots'*"
    )
    st.markdown("---")
    st.markdown("Made with ❤️ for Anime Fans")

st.markdown('<div class="title-text">Anime Recommender</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle-text">Your AI Companion for the Next Binge-Worthy Series</div>', unsafe_allow_html=True)

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What are you in the mood for?"):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = pipeline.recommend(prompt)
                st.markdown(response)
            except Exception as e:
                response = f"Sorry, I encountered an error: {str(e)}"
                st.error(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
