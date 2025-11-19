import yagmail
import os
from datetime import datetime
from db import db, Reminder

# Load secrets from environment variables (Render)
CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
REFRESH_TOKEN = os.getenv("GOOGLE_REFRESH_TOKEN")


def get_due_reminders():
    now_date = datetime.now().strftime("%Y-%m-%d")
    now_time = datetime.now().strftime("%H:%M")

    return Reminder.query.filter_by(
        date=now_date,
        time=now_time,
        status="Pending"
    ).all()


def send_due_reminders():
    reminders = get_due_reminders()
    if not reminders:
        print("No reminders due now.")
        return

    yag = yagmail.SMTP(
        oauth2_file={
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "refresh_token": REFRESH_TOKEN
        }
    )

    for r in reminders:
        try:
            yag.send(
                to=r.email,
                subject=f"Reminder: {r.title}",
                contents=r.message
            )
            print(f"✔ Sent to {r.email}")

            r.status = "Sent"
            db.session.commit()

        except Exception as e:
            print(f"✖ Error sending to {r.email}: {e}")
