from datetime import datetime
from database import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)  # ✅ NEW
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.Enum('manager','employee', name='user_roles'), nullable=False)

class Feedback(db.Model):
    __tablename__ = 'feedbacks'
    id = db.Column(db.Integer, primary_key=True)
    manager_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    strengths = db.Column(db.Text, nullable=False)
    improvements = db.Column(db.Text, nullable=False)
    sentiment = db.Column(db.Enum('positive','neutral','negative', name='sentiments'), nullable=False)
    tags = db.Column(db.ARRAY(db.String), nullable=True)
    anonymous = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    acknowledged = db.Column(db.Boolean, default=False)
    employee_comments = db.Column(db.Text, nullable=True)

    manager = db.relationship('User', foreign_keys=[manager_id])
    employee = db.relationship('User', foreign_keys=[employee_id])