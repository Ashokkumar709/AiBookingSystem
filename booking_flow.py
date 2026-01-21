import re

# -------------------------------------------------
# Booking fields order
# -------------------------------------------------
FIELDS = ["name", "email", "phone", "booking_type", "date", "time"]

QUESTIONS = {
    "name": "What is your full name?",
    "email": "What is your email address?",
    "phone": "What is your phone number?",
    "booking_type": "What service do you want to book?",
    "date": "Preferred date (YYYY-MM-DD)?",
    "time": "Preferred time? (HH:MM AM/PM)"
}

# -------------------------------------------------
# Validation regex
# -------------------------------------------------
NAME_REGEX = r"^[A-Za-z ]{2,}$"
EMAIL_REGEX = r"^[^@]+@[^@]+\.[^@]+$"
PHONE_REGEX = r"^\d{10,15}$"
DATE_REGEX = r"^\d{4}-\d{2}-\d{2}$"
TIME_REGEX = r"^(0?[1-9]|1[0-2]):[0-5][0-9]\s?(AM|PM)$"


# -------------------------------------------------
# Field validation
# -------------------------------------------------
def validate(field, value):
    value = value.strip()

    if field == "name":
        return bool(re.match(NAME_REGEX, value))

    if field == "email":
        return bool(re.match(EMAIL_REGEX, value))

    if field == "phone":
        return bool(re.match(PHONE_REGEX, value))

    if field == "booking_type":
        return len(value) >= 3

    if field == "date":
        return bool(re.match(DATE_REGEX, value))

    if field == "time":
        return bool(re.match(TIME_REGEX, value.upper()))

    return False


# -------------------------------------------------
# Get next missing field
# -------------------------------------------------
def get_next_field(state):
    for field in FIELDS:
        if field not in state:
            return field
    return None


# -------------------------------------------------
# Booking summary
# -------------------------------------------------
def summarize(state):
    return f"""
### 📋 Please confirm your booking:

- **Name:** {state['name']}
- **Email:** {state['email']}
- **Phone:** {state['phone']}
- **Service:** {state['booking_type']}
- **Date:** {state['date']}
- **Time:** {state['time']}

Reply **Yes** to confirm or **No** to cancel.
"""
