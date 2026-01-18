from flask import Blueprint, render_template,request, flash, redirect, url_for
from flask_login import login_user, logout_user, current_user, login_required, UserMixin, LoginManager
from sqlalchemy import case, func
from models.users import Users
from models.tasks import Tasks
from flask_sqlalchemy import SQLAlchemy
from database import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
import pytz
from datetime import date, datetime

user_dashboard = Blueprint("user_dashboard", __name__, template_folder="templates")

@user_dashboard.route("/dashboard")
@login_required
def dashboard():

    archive_old_tasks(current_user.id)

    today = date.today()
    
    # 1. Define Sort Orders
    type_order = case({"Monthly": 1, "Weekly": 2, "Daily": 3}, value=Tasks.type)
    priority_order = case({"High": 1, "Medium": 2, "Low": 3}, value=Tasks.priority)

    # 2. Fetch ALL Active (Non-Archived) Tasks
    # This single query gets everything we need for the table and the counts
    active_tasks = Tasks.query.filter_by(user_id=current_user.id, is_archived=False).order_by(type_order).order_by(priority_order).order_by(Tasks.created_at.desc()).all()

    # 3. Calculate Counts from the active_tasks list (Saves database hits)
    # Since we already have the 'active_tasks' list, we can count in Python 
    # instead of sending 4 more separate queries to the DB.
    total_tasks = len(active_tasks)
    completed_tasks = len([t for t in active_tasks if t.status == "Completed"])
    pending_tasks = len([t for t in active_tasks if t.status == "Pending"])
    in_progress_tasks = len([t for t in active_tasks if t.status == "In Progress"])

    # 4. Modules Count (Keep this as a DB query for distinct efficiency)
    working_modules = db.session.query(func.count(Tasks.module.distinct()))\
        .filter(Tasks.user_id == current_user.id, Tasks.is_archived == False).scalar()

    return render_template(
        "userdashboard.html", 
        today=today, 
        user=current_user, 
        tasks=active_tasks, 
        completed_tasks=completed_tasks, 
        pending_tasks=pending_tasks, 
        total_tasks=total_tasks, 
        working_modules=working_modules, 
        in_progress_tasks=in_progress_tasks
    )



def archive_old_tasks(user_id):
    today = datetime.now()
    # Logic: If it's Jan 14, anything created before Jan 1 (day=1) is "old"
    old_tasks = Tasks.query.filter(
        Tasks.user_id == user_id,
        Tasks.status == 'Completed',
        Tasks.is_archived == False,
        Tasks.created_at < today.replace(day=1, hour=0, minute=0, second=0)
    ).all()

    if old_tasks:
        for task in old_tasks:
            task.is_archived = True
        db.session.commit()



@user_dashboard.route("/archive")
@login_required
def archive():

    archived_tasks = Tasks.query.filter_by(user_id=current_user.id, is_archived=True).all()
    return render_template("archive.html", tasks=archived_tasks)


