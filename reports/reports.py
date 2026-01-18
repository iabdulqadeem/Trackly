from sqlite3 import Date
from sqlalchemy import case, func, cast, Date
from flask import Blueprint, render_template,request, flash, redirect, url_for, make_response
from flask_login import login_user, logout_user, current_user, login_required, UserMixin, LoginManager
from models.users import Users
from models.tasks import Tasks
from database import db, login_manager
import pytz
from datetime import date, datetime
from weasyprint import HTML


reports = Blueprint("reports", __name__, template_folder="templates")

@reports.route("/generate_pdf", methods = ["GET", "POST"])
@login_required
def generate_pdf():
    if request.method == "POST":
        start = request.form.get("start_date")
        end = request.form.get("end_date")

        generated_on = datetime.now().strftime("%d-%b-%Y %H:%M:%S")

        # Convert strings to actual date objects
        start_date = datetime.strptime(start, '%Y-%m-%d').date()
        end_date = datetime.strptime(end, '%Y-%m-%d').date()

        # UPDATED QUERY: 
        # We cast the database column to Date to ignore the time part
        # tasks = Tasks.query.filter(
        #     Tasks.user_id == current_user.id,
        #     cast(Tasks.created_at, Date) >= start_date,
        #     cast(Tasks.created_at, Date) <= end_date
        # ).order_by(Tasks.created_at.asc()).all()

        # 1. Define the custom sort order
        # This assigns 1 to Monthly, 2 to Weekly, 3 to Daily
        type_order = case({"Monthly": 1, "Weekly": 2, "Daily": 3}, value=Tasks.type)

        # 2. Query with the custom sort order first
        tasks = Tasks.query.filter(Tasks.user_id == current_user.id, cast(Tasks.created_at, Date) >= start_date, cast(Tasks.created_at, Date) <= end_date).order_by(type_order,Tasks.created_at.asc()).all()                 # First priority: Task Type
      #  tasks = Tasks.query.filter(Tasks.user_id == current_user.id, Tasks.created_at >= start, Tasks.created_at <= end).order_by(Tasks.created_at.asc()).all()    
        # Summary statistics for the report header
        stats = {
            "total": len(tasks),
            "completed": len([t for t in tasks if t.status == 'Completed']),
            "pending": len([t for t in tasks if t.status == 'Pending']),
            "in_progress": len([t for t in tasks if t.status == 'In Progress']),
            "start": start,
            "end": end
        }

        # Render HTML to PDF
        html_string = render_template("pdf_template.html", user = current_user, tasks=tasks, stats=stats, generated_on = generated_on)
        pdf = HTML(string=html_string).write_pdf()

        # Create response
        response = make_response(pdf)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = f'attachment; filename=Report_{start}_to_{end}.pdf'
        return response


    return render_template("reports.html")