from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from database import db

class Tasks(db.Model):
    __tablename__ = "Tasks"
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable = False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    module = db.Column(db.String(100), nullable=True, default="User Support")
    type = db.Column(db.String(15), default = "Daily") # Weekly, Monthly
    status = db.Column(db.String(50), default="Pending") # Pending, Completed
    priority = db.Column(db.String(50), default="Medium") # Low, Medium, High
    due_date = db.Column(db.Date, nullable=False, default=lambda: datetime.utcnow().date())
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True) # Stores the actual date of completion
    is_archived = db.Column(db.Boolean, default=False, index=True)
    # Relationship to easily access user info from a task
    user = db.relationship('Users', backref=db.backref('tasks', lazy=True))