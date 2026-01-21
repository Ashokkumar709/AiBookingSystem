import sqlite3
import streamlit as st
import pandas as pd
import os

from email_tool import send_cancellation_email  # ✅ NEW IMPORT


DB_PATH = os.path.abspath("bookings.db")


def admin_dashboard():
    st.title("📊 Admin Dashboard")
    st.caption("Manage bookings")

    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    cursor = conn.cursor()

    # ---------------------------------------------
    # Fetch bookings
    # ---------------------------------------------
    df = pd.read_sql_query("""
        SELECT
            bookings.id AS booking_id,
            customers.name AS "Customer Name",
            customers.email AS "Email",
            customers.phone AS "Phone",
            bookings.booking_type AS "Booking Type",
            bookings.date AS "Date",
            bookings.time AS "Time",
            bookings.status AS "Status",
            bookings.created_at AS "Created At"
        FROM bookings
        JOIN customers ON bookings.customer_id = customers.customer_id
        ORDER BY bookings.id DESC
    """, conn)

    if df.empty:
        st.info("No bookings found.")
        conn.close()
        return

    # 🔑 Ensure correct datatype
    df["booking_id"] = df["booking_id"].astype(int)

    df.insert(0, "No.", range(1, len(df) + 1))

    # ---------------------------------------------
    # Cancel Appointment
    # ---------------------------------------------
    st.subheader("❌ Cancel Appointment")

    selected_no = st.selectbox("Select booking", df["No."])
    row = df[df["No."] == selected_no].iloc[0]

    booking_id = int(row["booking_id"])

    st.markdown(f"""
**Customer:** {row['Customer Name']}  
**Email:** {row['Email']}  
**Booking Type:** {row['Booking Type']}  
**Date:** {row['Date']}  
**Time:** {row['Time']}  
**Current Status:** `{row['Status']}`
""")

    if row["Status"] != "cancelled":
        if st.button("Cancel Appointment"):
            # 1️⃣ Update DB
            cursor.execute(
                "UPDATE bookings SET status = 'cancelled' WHERE id = ?",
                (booking_id,)
            )
            conn.commit()

            # 2️⃣ Send cancellation email
            email_sent = send_cancellation_email(
                row["Email"],
                row.to_dict()
            )

            if email_sent:
                st.success("❌ Appointment cancelled & email sent")
            else:
                st.warning("❌ Appointment cancelled but email failed")

            # 3️⃣ Re-fetch updated data
            df = pd.read_sql_query("""
                SELECT
                    bookings.id AS booking_id,
                    customers.name AS "Customer Name",
                    customers.email AS "Email",
                    customers.phone AS "Phone",
                    bookings.booking_type AS "Booking Type",
                    bookings.date AS "Date",
                    bookings.time AS "Time",
                    bookings.status AS "Status",
                    bookings.created_at AS "Created At"
                FROM bookings
                JOIN customers ON bookings.customer_id = customers.customer_id
                ORDER BY bookings.id DESC
            """, conn)

            df["booking_id"] = df["booking_id"].astype(int)
            df.insert(0, "No.", range(1, len(df) + 1))

    else:
        st.warning("This appointment is already cancelled.")

    st.divider()

    # ---------------------------------------------
    # Bookings table
    # ---------------------------------------------
    st.subheader("📋 Bookings Table")

    st.dataframe(
        df.drop(columns=["booking_id"]),
        use_container_width=True,
        hide_index=True
    )

    conn.close()
