import streamlit as st
import pandas as pd
import nltk
import random
import time

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# --------------------------------------------------
# Download NLTK Resources
# --------------------------------------------------
try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt")

try:
    nltk.data.find("tokenizers/punkt_tab")
except LookupError:
    nltk.download("punkt_tab")

try:
    nltk.data.find("corpora/stopwords")
except LookupError:
    nltk.download("stopwords")

# --------------------------------------------------
# Streamlit Page Config
# --------------------------------------------------
st.set_page_config(
    page_title="AI FAQ Assistant",
    page_icon="🤖",
    layout="wide"
)

# --------------------------------------------------
# Custom CSS
# --------------------------------------------------
st.markdown("""
<style>

.main{
    background:#0f172a;
}

.block-container{
    padding-top:2rem;
}

h1{
    text-align:center;
}

.stChatMessage{
    border-radius:15px;
    padding:10px;
}

.suggestion{
    text-align:center;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# Load FAQ
# --------------------------------------------------
data = pd.read_csv("faq.csv")

stop_words = set(stopwords.words("english"))

# --------------------------------------------------
# Preprocessing
# --------------------------------------------------
def preprocess(text):

    text = str(text).lower()

    words = word_tokenize(text)

    words = [word for word in words if word.isalnum()]

    words = [word for word in words if word not in stop_words]

    return " ".join(words)

data["Processed"] = data["Question"].apply(preprocess)

# --------------------------------------------------
# TF-IDF
# --------------------------------------------------
vectorizer = TfidfVectorizer()

tfidf_matrix = vectorizer.fit_transform(data["Processed"])

# --------------------------------------------------
# Suggested Questions
# --------------------------------------------------
suggestions = [
    "What is AI?",
    "What is Machine Learning?",
    "What is Deep Learning?",
    "What is NLP?",
    "What is Computer Vision?",
    "What is ChatGPT?",
    "What is TensorFlow?",
    "What is PyTorch?",
    "What is Generative AI?",
    "Can AI replace humans?",
    "What is reinforcement learning?",
    "What is supervised learning?"
]

# --------------------------------------------------
# Sidebar
# --------------------------------------------------
with st.sidebar:


    st.write("### Example Questions")

    for q in random.sample(suggestions,5):
        st.write("•",q)

    st.markdown("---")

    if st.button("🗑 Clear Chat"):

        st.session_state.messages=[]

        st.rerun()

# --------------------------------------------------
# Welcome
# --------------------------------------------------
st.title("🤖 AI FAQ Assistant")

st.caption("Ask me anything about Artificial Intelligence.")

# --------------------------------------------------
# Session State
# --------------------------------------------------
if "messages" not in st.session_state:

    st.session_state.messages=[]

# Display old messages

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

# --------------------------------------------------
# Suggestion Buttons
# --------------------------------------------------
st.markdown("### 💡 Suggested Questions")

cols=st.columns(3)

sample=random.sample(suggestions,6)

for i,q in enumerate(sample):

    if cols[i%3].button(q,use_container_width=True):

        st.session_state.selected=q

# --------------------------------------------------
# Chat Input
# --------------------------------------------------
prompt=st.chat_input("Ask anything about AI...")

if "selected" in st.session_state:

    prompt=st.session_state.pop("selected")
    # --------------------------------------------------
# Process User Question
# --------------------------------------------------
if prompt:

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    # Preprocess question
    processed_input = preprocess(prompt)

    # Convert to TF-IDF vector
    input_vector = vectorizer.transform([processed_input])

    # Calculate similarity
    similarity = cosine_similarity(input_vector, tfidf_matrix)

    max_score = similarity.max()

    # Typing animation
    with st.chat_message("assistant"):

        thinking = st.empty()

        for text in [
            "🧠 Thinking.",
            "🧠 Thinking..",
            "🧠 Thinking..."
        ]:
            thinking.markdown(text)
            time.sleep(0.3)

        # Find best answer
        if max_score >= 0.30:

            best_match = similarity.argmax()

            answer = data.iloc[best_match]["Answer"]

        else:

            answer = (
                "😔 Sorry, I couldn't find a relevant answer.\n\n"
                "Try asking something related to Artificial Intelligence."
            )

        thinking.empty()

        st.markdown(answer)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )

# --------------------------------------------------
# Footer
# --------------------------------------------------
st.markdown("---")

st.markdown(
    """
    <div style='text-align:center;color:gray;font-size:14px'>
        🤖 AI FAQ Assistant<br>
    
    """,
    unsafe_allow_html=True,
)