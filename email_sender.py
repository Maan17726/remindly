import yagmail
import schedule
import time
import os
from db import db, Reminder
from flask import Flask
from datetime import datetime

# Create temporary flask app for DB access in worker
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

# Load secrets from environment variables (Render)
CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
REFRESH_TOKEN = os.getenv("GOOGLE_REFRESH_TOKEN")


def get_due_reminders():
    with app.app_context():
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

    with app.app_context():
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


schedule.every(1).minutes.do(send_due_reminders)

if __name__ == "__main__":
    print("📨 Email worker is running...")
    while True:
        schedule.run_pending()
        time.sleep(1)
