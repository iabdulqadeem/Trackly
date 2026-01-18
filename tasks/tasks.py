from flask import Blueprint, render_template,request, flash, redirect, url_for
from flask_login import login_user, logout_user, current_user, login_required, UserMixin, LoginManager
from models.users import Users
from models.tasks import Tasks
from database import db, login_manager
import pytz
from datetime import date, datetime

tasks = Blueprint("tasks", __name__, template_folder="templates")

@tasks.route("/add", methods = ["GET", "POST"])
@login_required
def add_task():
    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        module = request.form.get("module")
        priority = request.form.get("priority")
        category = request.form.get("type")
        status = request.form.get("status")
        deadline_raw = request.form.get("deadline")

        # 1. Convert string date to Python date object
        deadline = None
        if deadline_raw:
            deadline = datetime.strptime(deadline_raw, '%Y-%m-%d').date()

        new_task = Tasks(title = title, description = description, module = module, priority = priority, type = category, status = status, due_date = deadline, user_id = current_user.id)
        db.session.add(new_task)
        db.session.commit()

        flash("Task Added Successfully!", "success")
        # 3. Always redirect after a successful POST
        return redirect(url_for("user_dashboard.dashboard"))


    return render_template("addtask.html")


@tasks.route("/view/<int:task_id>", methods=["GET"])
@login_required
def view_task(task_id):
    # Fetch the task or return a 404 error if it doesn't exist
    task = Tasks.query.get_or_404(task_id)
    
    # Security: Ensure the user can only view their own tasks
    if task.user_id != current_user.id:
        flash("You do not have permission to view this task.", "danger")
        return redirect(url_for('user_dashboard.dashboard'))
        
    return render_template("viewtask.html", task=task)


@tasks.route("/mark_done/<int:task_id>")
@login_required
def mark_done(task_id):
    task = Tasks.query.get_or_404(task_id)

    # Security: Ensure the user owns the task
    if task.user_id != current_user.id:
        flash("Unauthorized action.", "danger")
        return redirect(url_for('user_dashboard.dashboard'))

    # Update status
    task.status = "Completed"
    task.completed_at = datetime.now()
    db.session.commit()
    
    flash(f"Task '{task.title}' marked as completed!", "success")
    return redirect(url_for('user_dashboard.dashboard'))

@tasks.route("/delete/<int:task_id>", methods=["GET", "POST"])
@login_required
def delete_task(task_id):
    task = Tasks.query.get_or_404(task_id)

    # Security: Prevent users from deleting tasks they don't own
    if task.user_id != current_user.id:
        flash("Unauthorized access.", "danger")
        return redirect(url_for('user_dashboard.dashboard'))

    db.session.delete(task)
    db.session.commit()
    
    flash("Task deleted successfully.", "info")
    return redirect(url_for('user_dashboard.dashboard'))


@tasks.route("/edit/<int:task_id>", methods=["GET", "POST"])
@login_required
def edit_task(task_id):
    task = Tasks.query.get_or_404(task_id)

    # Security: Prevent users from deleting tasks they don't own
    if task.user_id != current_user.id:
        flash("Unauthorized access.", "danger")
        return redirect(url_for('user_dashboard.dashboard'))

    if request.method == "POST":
        task.title = request.form.get("edit_title")
        task.description = request.form.get("edit_description")
        task.module = request.form.get("edit_module")
        task.type = request.form.get("edit_type")
        task.status = request.form.get("edit_status")
        task.priority = request.form.get("edit_priority")
        task.due_date = request.form.get("edit_deadline")

        flash("Task edited successfully.", "info")
        db.session.commit() 
        return redirect(url_for('user_dashboard.dashboard'))
        
    return render_template("edittask.html", task = task)
