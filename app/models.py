from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(15), nullable=False)
    queue_position = db.Column(db.Integer, nullable=False)
    order_placed_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(15), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # Rating (1-5)
    comments = db.Column(db.String(500), nullable=True)  # Optional feedback comments
    written_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)