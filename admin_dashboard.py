import sqlite3
import streamlit as st
import pandas as pd
import os

DB_PATH = os.path.abspath("bookings.db")


def admin_dashboard():
    st.title("📊 Admin Dashboard")
    st.caption("Manage bookings")

    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    cursor = conn.cursor()

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

    df["booking_id"] = df["booking_id"].astype(int)
    df.insert(0, "No.", range(1, len(df) + 1))

    # -----------------------------
    # 🔍 FILTERS
    # -----------------------------
    st.subheader("🔍 Filters")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        name_filter = st.text_input("Customer Name")

    with col2:
        email_filter = st.text_input("Email")

    with col3:
        date_filter = st.text_input("Date (YYYY-MM-DD)")

    with col4:
        status_filter = st.selectbox(
            "Status",
            ["All", "confirmed", "cancelled"]
        )

    filtered_df = df.copy()

    if name_filter:
        filtered_df = filtered_df[
            filtered_df["Customer Name"].str.contains(name_filter, case=False, na=False)
        ]

    if email_filter:
        filtered_df = filtered_df[
            filtered_df["Email"].str.contains(email_filter, case=False, na=False)
        ]

    if date_filter:
        filtered_df = filtered_df[
            filtered_df["Date"].str.contains(date_filter, na=False)
        ]

    if status_filter != "All":
        filtered_df = filtered_df[
            filtered_df["Status"] == status_filter
        ]

    st.divider()

    # -----------------------------
    # ❌ CANCEL APPOINTMENT
    # -----------------------------
    st.subheader("❌ Cancel Appointment")

    if not filtered_df.empty:
        selected_no = st.selectbox(
            "Select booking",
            filtered_df["No."]
        )

        row = filtered_df[filtered_df["No."] == selected_no].iloc[0]
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
                cursor.execute(
                    "UPDATE bookings SET status = 'cancelled' WHERE id = ?",
                    (booking_id,)
                )
                conn.commit()
                st.success("✅ Appointment cancelled")
                st.rerun()
        else:
            st.warning("This appointment is already cancelled.")
    else:
        st.info("No bookings match the selected filters.")

    st.divider()

    # -----------------------------
    # 📋 BOOKINGS TABLE
    # -----------------------------
    st.subheader("📋 Bookings Table")

    st.dataframe(
        filtered_df.drop(columns=["booking_id"]),
        use_container_width=True,
        hide_index=True
    )

    conn.close()
