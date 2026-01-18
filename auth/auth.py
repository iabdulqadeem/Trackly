from flask import Blueprint, render_template,request, flash, redirect, url_for
from flask_login import login_user, logout_user, current_user, login_required, UserMixin, LoginManager
from models.users import Users
from database import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
import pytz
from datetime import datetime





auth = Blueprint("auth", __name__, template_folder="templates")

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

@auth.route("/login", methods = ["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('user_dashboard.dashboard'))

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = Users.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            pk_timezone = pytz.timezone("Asia/Karachi")
            user.last_login_at = datetime.now(pk_timezone)

            db.session.commit()

            flash('Welcome back!', 'success')
            return redirect(url_for("user_dashboard.dashboard"))

        flash('Invalid email or password.', 'danger')
    
    return render_template("login.html")

@auth.route("/logout")
@login_required
def logout():
    logout_user()  # This destroys the session
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login')) # Redirect back to login page



@auth.route("/signup", methods = ["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('user_dashboard.dashboard'))
    
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")

        if Users.query.filter_by(email = email).first():
            flash('Email already exists.', 'danger')
            return redirect(url_for("auth.signup"))
    
        hashed_password = generate_password_hash(password)
        new_user = Users(name = name, email = email, password = hashed_password)
        

        db.session.add(new_user)
        db.session.commit()

        flash('Account created! Please login.', 'success')

        return redirect(url_for("auth.login"))
    return render_template("signup.html")