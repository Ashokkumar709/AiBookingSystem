# 🤖 AI Booking Assistant (RAG + Admin Dashboard)

A conversational AI assistant built with **Streamlit**, **LLM (Groq)**, and **RAG**
to handle document-based Q&A and appointment bookings with an admin dashboard.

---

## ✨ Features

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
│   └── secrets.toml.example
├── requirements.txt
├── README.md
└── .gitignore

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository

git clone https://github.com/Ashokkumar709/AiBookingSystem.git  
cd AiBookingSystem

### 2️⃣ Install Dependencies

pip install -r requirements.txt

### 3️⃣ Configure Secrets

Create the file:

.streamlit/secrets.toml

Add the following inside:

GROQ_API_KEY = "your_groq_api_key"  
EMAIL_USER = "your_email@gmail.com"  
EMAIL_PASSWORD = "your_gmail_app_password"

⚠️ For Gmail, you must use an App Password, not your normal email password.

---

## ▶️ Run the Application

streamlit run app.py

---

## 🧪 How to Test the Application

### 🔹 Test PDF-Based Q&A (RAG)

- Upload a text-based PDF
- Ask questions related to the document
- The system retrieves relevant chunks and answers using the LLM

---

### 🔹 Test Booking Flow

Type:

Book an appointment

Then provide details step-by-step:

- Name
- Email
- Phone number
- Service type
- Date and time

Review the booking summary and confirm.  
You will receive a confirmation email after successful booking.

---

## 🔐 Admin Dashboard Testing

### 🔑 Admin Login Credentials

Username: admin  
Password: password123

---

### 🧭 Accessing the Admin Dashboard

- Open the sidebar in the Streamlit app
- Select Admin Dashboard
- Login using the credentials above
- View all bookings
- Cancel bookings (email notification is sent automatically)

---

## 📌 Notes

- PDF files must contain selectable text (not scanned images).
- SQLite database is stored locally.
- Email requires valid SMTP credentials.

---

## 🚀 Future Improvements

- OAuth-based admin authentication
- Google Calendar integration
- Multi-admin roles
- Cloud database (PostgreSQL / Firebase)
- Deployment on Streamlit Cloud / AWS
