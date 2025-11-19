from flask import Flask, render_template, request, redirect
from db import db, Reminder
from email_sender import send_due_reminders
import schedule
import time
import threading

app = Flask(__name__)

# DB CONFIG
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

# CREATE DB IF NOT EXISTS
with app.app_context():
    db.create_all()


# HOME PAGE
@app.route("/")
def home():
    return render_template("index.html")


# CREATE REMINDER
@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        title = request.form["title"]
        email = request.form["email"]
        date = request.form["date"]
        time_ = request.form["time"]
        message = request.form["message"]

        new_r = Reminder(
            title=title,
            email=email,
            date=date,
            time=time_,
            message=message
        )

        db.session.add(new_r)
        db.session.commit()

        return redirect("/success")

    return render_template("create.html")


# SUCCESS PAGE
@app.route("/success")
def success():
    return render_template("success.html")


# SHOW REMINDERS (User-specific)
@app.route("/reminders")
def reminders():
    email = request.args.get("email")  # get email from form

    if email:
        reminders = Reminder.query.filter_by(email=email).all()
    else:
        reminders = None

    return render_template("reminders.html", reminders=reminders)


# DELETE REMINDER
@app.route("/delete/<int:id>")
def delete(id):
    r = Reminder.query.get(id)
    db.session.delete(r)
    db.session.commit()
    return redirect("/reminders")


# ABOUT PAGE
@app.route("/about")
def about():
    return render_template("about.html")


# EMAIL SCHEDULER
def run_scheduler():
    with app.app_context():
        schedule.every(1).minutes.do(send_due_reminders)

        while True:
            schedule.run_pending()
            time.sleep(1)


if __name__ == "__main__":
    threading.Thread(target=run_scheduler).start()
    app.run(debug=True)
