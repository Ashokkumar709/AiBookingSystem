import streamlit as st
import sqlite3
from langchain_groq import ChatGroq

from intent import detect_intent
from booking_flow import get_next_field, QUESTIONS, validate, summarize
from database import save_booking
from email_tool import send_email
from rag_tool import build_rag
from admin_dashboard import admin_dashboard
from admin_auth import admin_login, admin_logout

# st.autorefresh(interval=3000, key="booking_status_refresh")


# -------------------------------------------------
# Constants
# -------------------------------------------------
MAX_MEMORY = 25


def trim_memory():
    if len(st.session_state.messages) > MAX_MEMORY:
        st.session_state.messages = st.session_state.messages[-MAX_MEMORY:]


def get_recent_chat_context():
    history = []
    for m in st.session_state.messages[-MAX_MEMORY:]:
        role = "User" if m["role"] == "user" else "Assistant"
        history.append(f"{role}: {m['content']}")
    return "\n".join(history)


# -------------------------------------------------
# DB helper: get latest booking status for user
# -------------------------------------------------
def get_latest_booking_status(email):
    conn = sqlite3.connect("bookings.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT bookings.status
        FROM bookings
        JOIN customers ON bookings.customer_id = customers.customer_id
        WHERE customers.email = ?
        ORDER BY bookings.created_at DESC
        LIMIT 1
    """, (email,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None


# -------------------------------------------------
# Page config
# -------------------------------------------------
st.set_page_config(
    page_title="AI Booking Assistant",
    page_icon="🤖",
    layout="wide"
)

# -------------------------------------------------
# UI styles
# -------------------------------------------------
st.markdown("""
<style>
.stChatMessage { padding: 6px 0; }

.stChatMessage[data-testid="stChatMessage-user"] {
    flex-direction: row-reverse;
}
.stChatMessage[data-testid="stChatMessage-user"] .stMarkdown {
    background-color: #DCF8C6;
    padding: 12px;
    border-radius: 14px;
    max-width: 75%;
}
.stChatMessage[data-testid="stChatMessage-assistant"] .stMarkdown {
    background-color: #F1F0F0;
    padding: 12px;
    border-radius: 14px;
    max-width: 75%;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# LLM
# -------------------------------------------------
llm = ChatGroq(
    api_key=st.secrets["GROQ_API_KEY"],
    model="llama-3.1-8b-instant"
)

# -------------------------------------------------
# Session state
# -------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "booking" not in st.session_state:
    st.session_state.booking = {}

if "booking_mode" not in st.session_state:
    st.session_state.booking_mode = False

if "booking_started" not in st.session_state:
    st.session_state.booking_started = False

if "booking_status" not in st.session_state:
    st.session_state.booking_status = "idle"  # idle | in_progress | confirmed | cancelled

if "uploader_key" not in st.session_state:
    st.session_state.uploader_key = 0

# -------------------------------------------------
# Sidebar
# -------------------------------------------------
with st.sidebar:
    st.markdown("## 🤖 AI Booking Assistant")
    st.caption("RAG + Conversational Booking")

    st.divider()

    page = st.radio("Navigation", ["💬 Chat", "📊 Admin Dashboard"])

    st.divider()

    if st.button("🆕 New Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.booking = {}
        st.session_state.booking_mode = False
        st.session_state.booking_started = False
        st.session_state.booking_status = "idle"
        st.session_state.uploader_key += 1
        if "vs" in st.session_state:
            del st.session_state.vs
        st.rerun()

    st.divider()

    st.caption("Status")
    if st.session_state.booking_status == "in_progress":
        st.warning("📅 Booking in progress")
    elif st.session_state.booking_status == "confirmed":
        st.success("✅ Booking confirmed")
    elif st.session_state.booking_status == "cancelled":
        st.error("❌ Booking cancelled")
    else:
        st.success("🟢 Idle")

# -------------------------------------------------
# Admin Page
# -------------------------------------------------
# -------------------------------------------------
# Admin Page (AUTH PROTECTED)
# -------------------------------------------------
if page == "📊 Admin Dashboard":
    if not admin_login():
        st.stop()

    with st.sidebar:
        if st.button("🔓 Logout Admin"):
            admin_logout()

    admin_dashboard()
    st.stop()


# -------------------------------------------------
# Main UI
# -------------------------------------------------
st.title("🤖 AI Booking Assistant")
st.caption("Ask questions from PDFs or book appointments via chat")

# -------------------------------------------------
# PDF Upload
# -------------------------------------------------
pdfs = st.file_uploader(
    "Upload PDFs for Q&A",
    type="pdf",
    accept_multiple_files=True,
    key=f"pdf_uploader_{st.session_state.uploader_key}"
)

if pdfs:
    paths = []
    for i, pdf in enumerate(pdfs):
        path = f"temp_{i}.pdf"
        with open(path, "wb") as f:
            f.write(pdf.getbuffer())
        paths.append(path)

    try:
        st.session_state.vs = build_rag(paths)
        st.success("PDFs processed successfully.")
    except Exception as e:
        st.error(f"Invalid PDF uploaded: {e}")

# -------------------------------------------------
# Chat history
# -------------------------------------------------
for m in st.session_state.messages:
    with st.chat_message(m["role"], avatar="🧑" if m["role"] == "user" else "🤖"):
        st.markdown(m["content"])

# -------------------------------------------------
# Chat input
# -------------------------------------------------
user_input = st.chat_input("Type your message...")

if user_input:
    # User message
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )
    trim_memory()

    with st.chat_message("user", avatar="🧑"):
        st.markdown(user_input)

    # ---------------- Detect admin cancellation ----------------
    if "email" in st.session_state.booking:
        latest_status = get_latest_booking_status(st.session_state.booking["email"])
        if latest_status == "cancelled":
            st.session_state.booking_status = "cancelled"

    # ---------------- Intent routing ----------------
    if st.session_state.booking_mode:
        intent = "booking"
    else:
        intent = detect_intent(llm, user_input)
        if intent == "booking":
            st.session_state.booking_mode = True
            st.session_state.booking_started = False
            st.session_state.booking_status = "in_progress"

    # ---------------- Booking flow ----------------
    if intent == "booking":
        if not st.session_state.booking_started:
            st.session_state.booking_started = True
            response = QUESTIONS["name"]

        else:
            field = get_next_field(st.session_state.booking)

            if field:
                if validate(field, user_input):
                    st.session_state.booking[field] = user_input
                    next_field = get_next_field(st.session_state.booking)
                    response = QUESTIONS[next_field] if next_field else summarize(st.session_state.booking)
                else:
                    response = "❌ Invalid input. Please try again."

            else:
                if user_input.strip().lower() == "yes":
                    booking_id = save_booking(st.session_state.booking)
                    st.session_state.booking["booking_id"] = booking_id

                    email_sent = send_email(
                        st.session_state.booking["email"],
                        st.session_state.booking
                    )

                    st.session_state.booking_status = "confirmed"

                    if email_sent:
                        response = f"✅ Booking confirmed! ID: {booking_id}\n📧 Confirmation email sent."
                    else:
                        response = f"⚠️ Booking confirmed (ID: {booking_id}) but email failed."

                    st.session_state.booking = {}
                    st.session_state.booking_mode = False
                    st.session_state.booking_started = False

                else:
                    response = "❌ Booking cancelled."
                    st.session_state.booking = {}
                    st.session_state.booking_mode = False
                    st.session_state.booking_started = False
                    st.session_state.booking_status = "idle"

    # ---------------- RAG + MEMORY Q&A ----------------
    else:
        chat_history = get_recent_chat_context()

        if "vs" in st.session_state:
            docs = st.session_state.vs.similarity_search(user_input, k=3)
            context = "\n".join(docs)


            prompt = f"""
You are a helpful AI assistant.

Conversation so far:
{chat_history}

Relevant document context:
{context}

User question:
{user_input}
"""
            response = llm.invoke(prompt).content

        else:
            prompt = f"""
You are a helpful AI assistant.

Conversation so far:
{chat_history}

User message:
{user_input}
"""
            response = llm.invoke(prompt).content

    # Assistant message
    st.session_state.messages.append(
        {"role": "assistant", "content": response}
    )
    trim_memory()

    with st.chat_message("assistant", avatar="🤖"):
        st.markdown(response)
