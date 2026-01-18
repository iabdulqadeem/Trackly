from flask_sqlalchemy import SQLAlchemy
from database import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import pytz
from flask_login import UserMixin


class Users(db.Model, UserMixin):
    __tablename__ = "Users"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(155), nullable = False)
    email = db.Column(db.String(155), nullable = False)
    password = db.Column(db.Text, nullable = False)
    role = db.Column(db.String(20), default = "user")
    is_active = db.Column(db.Boolean, default = True )
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login_at = db.Column(db.DateTime, nullable = True)