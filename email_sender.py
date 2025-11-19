import yagmail
import schedule
import time
import os
from datetime import datetime
from db import get_due_reminders


# Load secrets from environment variables (Render)
CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
REFRESH_TOKEN = os.getenv("GOOGLE_REFRESH_TOKEN")


def send_due_reminders():
    reminders = get_due_reminders()
    if not reminders:
        print("No reminders due now.")
        return

    # Setup OAuth using environment variables
    yag = yagmail.SMTP(
        oauth2_file={
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "refresh_token": REFRESH_TOKEN
        }
    )

    for r in reminders:
        email = r[1]
        title = r[2]
        message = r[3]

        try:
            yag.send(
                to=email,
                subject=f"Reminder: {title}",
                contents=message
            )
            print(f"✔ Email sent to: {email}")
        except Exception as e:
            print(f"✖ Error sending to {email}: {e}")


schedule.every(1).minutes.do(send_due_reminders)

if __name__ == "__main__":
    print("📨 Reminder service is running...")
    while True:
        schedule.run_pending()
        time.sleep(1)
