import streamlit as st
from chatbot import get_response
from pdf_generator import generate_pdf
from datetime import datetime

# Page setup — must be the first Streamlit command in the file
st.set_page_config(
    page_title="AI Public Health Chatbot",
    page_icon="🤖",
    layout="wide"
)

# Initialize chat history in session state (persists across reruns)
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Custom CSS styling
st.markdown("""
<style>
    .main { background-color: #f5f5f5; }
    .stButton>button { width: 100%; border-radius: 10px; }
    .health-card { padding: 20px; margin-bottom: 20px; background-color: #ffffff; border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

st.title("🤖 AI Public Health Chatbot")
st.write("Ask me anything about diseases, symptoms, prevention, and healthy lifestyle tips!")

# Two columns: chat area (wide) + sidebar-like topics panel (narrow)
col1, col2 = st.columns([3, 1])

with col2:
    st.markdown("### Health Topics")
    topics = ["Dengue", "Malaria", "COVID-19", "Diabetes",
              "Hypertension", "Tuberculosis", "Typhoid", "Cholera", "Asthma", "Anemia"]

    # One button per disease — clicking auto-fills a question
    for topic in topics:
        if st.button(topic, key=f"btn_{topic}"):
            st.session_state.pending_query = f"Tell me about {topic}"

    st.markdown("---")

    # Only show PDF button if there's something to export
    if st.session_state.chat_history:
        if st.button("📄 Download PDF Report"):
            filepath = generate_pdf(st.session_state.chat_history)
            with open(filepath, "rb") as f:
                st.download_button(
                    label="Click to save report",
                    data=f,
                    file_name=filepath.split("/")[-1],
                    mime="application/pdf"
                )

with col1:
    # Redraw all past messages every rerun (Streamlit reruns top-to-bottom each interaction)
    for chat in st.session_state.chat_history:
        with st.chat_message("user"):
            st.write(chat["question"])
        with st.chat_message("assistant"):
            st.write(chat["response"])

    # Chat input box at the bottom of the page
    query = st.chat_input("Type your question here...")

    # If a sidebar button was clicked, that takes priority over the input box
    if "pending_query" in st.session_state:
        query = st.session_state.pop("pending_query")

    if query:
        with st.chat_message("user"):
            st.write(query)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = get_response(query)   # calls chatbot.py logic
            st.write(response)

        # Save this exchange to history — keys MUST match what pdf_generator.py expects
        st.session_state.chat_history.append({
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "question": query,
            "response": response
        })

        st.rerun()   # refresh the page so the new message appears in the loop above