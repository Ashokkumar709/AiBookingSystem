import smtplib
from email.mime.text import MIMEText
import streamlit as st


# -------------------------------------------------
# Booking confirmation email (UNCHANGED)
# -------------------------------------------------
def send_email(to_email, booking):
    try:
        print("📧 Sending confirmation email to:", to_email)

        html_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; background-color: #f4f6f8; padding: 20px;">
            <div style="
                max-width: 600px;
                margin: auto;
                background-color: #ffffff;
                padding: 24px;
                border-radius: 10px;
                box-shadow: 0 4px 10px rgba(0,0,0,0.08);
            ">
                <h2 style="color: #2c3e50;">✅ Booking Confirmed</h2>

                <p>Hello <strong>{booking['name']}</strong>,</p>

                <p>Your booking has been successfully confirmed.</p>

                <div style="background:#f8f9fa;padding:16px;border-radius:8px;">
                    <p><strong>📌 Booking ID:</strong> {booking['booking_id']}</p>
                    <p><strong>🩺 Service:</strong> {booking['booking_type']}</p>
                    <p><strong>📅 Date:</strong> {booking['date']}</p>
                    <p><strong>⏰ Time:</strong> {booking['time']}</p>
                </div>

                <p>If you need help, just reply to this email.</p>

                <p style="font-size:12px;color:#888;">
                    Automated message – do not share your booking ID publicly.
                </p>
            </div>
        </body>
        </html>
        """

        msg = MIMEText(html_body, "html")
        msg["Subject"] = "✅ Your Booking is Confirmed"
        msg["From"] = st.secrets["EMAIL_USER"]
        msg["To"] = to_email

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(
                st.secrets["EMAIL_USER"],
                st.secrets["EMAIL_PASSWORD"]
            )
            server.send_message(msg)

        print("✅ Confirmation email sent")
        return True

    except Exception as e:
        print("❌ Confirmation email error:", e)
        st.error(f"Email failed: {e}")
        return False


# -------------------------------------------------
# Booking cancellation email (NEW)
# -------------------------------------------------
def send_cancellation_email(to_email, booking):
    try:
        print("📧 Sending cancellation email to:", to_email)

        html_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; background-color:#f4f6f8; padding:20px;">
            <div style="
                max-width:600px;
                margin:auto;
                background:#ffffff;
                padding:24px;
                border-radius:10px;
                box-shadow: 0 4px 10px rgba(0,0,0,0.08);
            ">
                <h2 style="color:#c0392b;">❌ Appointment Cancelled</h2>

                <p>Hello <strong>{booking['Customer Name']}</strong>,</p>

                <p>
                    We regret to inform you that your appointment has been
                    <strong>cancelled</strong>.
                </p>

                <div style="background:#f8f9fa;padding:16px;border-radius:8px;">
                    <p><strong>🩺 Service:</strong> {booking['Booking Type']}</p>
                    <p><strong>📅 Date:</strong> {booking['Date']}</p>
                    <p><strong>⏰ Time:</strong> {booking['Time']}</p>
                </div>

                <p>If you wish to book a new appointment, please contact us.</p>

                <p style="font-size:12px;color:#888;">
                    This is an automated cancellation notice.
                </p>
            </div>
        </body>
        </html>
        """

        msg = MIMEText(html_body, "html")
        msg["Subject"] = "❌ Your Appointment Has Been Cancelled"
        msg["From"] = st.secrets["EMAIL_USER"]
        msg["To"] = to_email

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(
                st.secrets["EMAIL_USER"],
                st.secrets["EMAIL_PASSWORD"]
            )
            server.send_message(msg)

        print("✅ Cancellation email sent")
        return True

    except Exception as e:
        print("❌ Cancellation email error:", e)
        st.error(f"Cancellation email failed: {e}")
        return False
