from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Reminder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    email = db.Column(db.String(120))
    date = db.Column(db.String(50))
    time = db.Column(db.String(50))
    message = db.Column(db.Text)
    status = db.Column(db.String(20), default="Pending")
