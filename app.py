import streamlit as st
from faq_data import faq_data
from rapidfuzz import process

# -------------------------------
# PAGE CONFIGURATION
# -------------------------------

st.set_page_config(
    page_title="College FAQ Assistant",
    page_icon="🎓",
    layout="wide"
)

# -------------------------------
# CUSTOM CSS
# -------------------------------

st.markdown("""
<style>

.main{
    background:#f6f8fc;
}

.block-container{
    padding-top:2rem;
}

.title{
    text-align:center;
    color:#1f77ff;
    font-size:42px;
    font-weight:bold;
}

.subtitle{
    text-align:center;
    color:gray;
    margin-bottom:20px;
}

</style>
""", unsafe_allow_html=True)

# -------------------------------
# TITLE
# -------------------------------

st.markdown(
"<div class='title'>🎓 College FAQ Assistant</div>",
unsafe_allow_html=True
)

st.markdown(
"<div class='subtitle'>Ask anything about your college.</div>",
unsafe_allow_html=True
)

# -------------------------------
# SESSION STATE
# -------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "first_question" not in st.session_state:
    st.session_state.first_question = False

# -------------------------------
# SIDEBAR
# -------------------------------

st.sidebar.title("🎓 College Assistant")

if st.sidebar.button("🗑 Clear Chat"):

    st.session_state.messages = []
    st.session_state.first_question = False
    st.rerun()

st.sidebar.markdown("---")

st.sidebar.subheader("Example Questions")

st.sidebar.write("• What courses are offered?")
st.sidebar.write("• What are the college timings?")
st.sidebar.write("• Is hostel accommodation available?")
st.sidebar.write("• Does the college provide scholarships?")
st.sidebar.write("• What is the fee structure?")

# -------------------------------
# PREPARE DATA
# -------------------------------

questions = list(faq_data.keys())

# -------------------------------
# WELCOME MESSAGE
# -------------------------------

if not st.session_state.first_question:

    st.info("""
👋 **Welcome!**

I am your **College FAQ Assistant**.

You can ask me questions about:

- 🎓 Admissions
- 🏠 Hostel
- 💰 Fees
- 📚 Courses
- 💼 Placements
- 📖 Library
- 🏆 Scholarships
- ⚽ Sports

Start typing your question below.
""")

# -------------------------------
# DISPLAY CHAT HISTORY
# -------------------------------

for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# -------------------------------
# FIND ANSWER
# -------------------------------

def get_answer(user_question):

    match = process.extractOne(
        user_question,
        questions
    )

    if match is None:
        return """
❌ Sorry, I couldn't find an answer.

Please ask questions related to the college.
"""

    matched_question = match[0]
    score = match[1]

    if score < 65:
        return """
❌ Sorry, I couldn't find an answer.

Try asking about:

• Admissions
• Courses
• Hostel
• Fees
• Placements
• Scholarships
• Library
• Transport
• Sports
"""

    return faq_data[matched_question]
# -------------------------------
# USER INPUT
# -------------------------------

user_input = st.chat_input("💬 Ask your question here...")

# -------------------------------
# PROCESS MESSAGE
# -------------------------------

if user_input:

    # Hide welcome message after first question
    st.session_state.first_question = True

    # Get chatbot answer
    answer = get_answer(user_input)

    # Save user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    # Save assistant message
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )

    # Refresh page
    st.rerun()

# -------------------------------
# FOOTER
# -------------------------------

st.markdown("---")

st.markdown(
    """
    <div style="
        text-align:center;
        color:gray;
        font-size:14px;
        padding-bottom:10px;">
        © 2026 College FAQ Assistant
    </div>
    """,
    unsafe_allow_html=True
)