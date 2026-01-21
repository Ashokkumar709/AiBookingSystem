# 🤖 AI Booking Assistant (RAG + Admin Dashboard)

A conversational AI assistant built with **Streamlit**, **LLM (Groq)**, and **RAG**
to handle document-based Q&A and appointment bookings with an admin dashboard.

---

##  Features

- 💬 Conversational booking assistant
- 📄 PDF-based Q&A using RAG
- 📅 Step-by-step appointment booking
- 📧 Email confirmation & cancellation
- 🔐 Admin authentication
- 📊 Admin dashboard to manage bookings
- ❌ Cancel appointments with email notification
- 🧠 Short-term conversational memory

---

## 🏗️ Architecture Overview

- **Frontend:** Streamlit
- **LLM:** Groq (LLaMA 3.1)
- **Vector Store:** LangChain
- **Database:** SQLite
- **Email:** SMTP (Gmail)
- **Auth:** Session-based admin login

---

## 📂 Project Structure

AI-Booking-Assistant/
├── app.py
├── admin_dashboard.py
├── admin_auth.py
├── booking_flow.py
├── database.py
├── email_tool.py
├── intent.py
├── rag_tool.py
├── .streamlit/
│ └── secrets.toml.example
├── requirements.txt
├── README.md
└── .gitignore