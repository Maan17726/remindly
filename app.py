from flask import Flask, render_template, request, redirect
from db import db, Reminder

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


# SHOW REMINDERS
@app.route("/reminders")
def reminders():
    email = request.args.get("email")
    reminders = Reminder.query.filter_by(email=email).all() if email else None
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


if __name__ == "__main__":
    app.run(debug=True)
