from flask import Flask, redirect, render_template, url_for
from flask_login import current_user
from auth.auth import auth
from reports.reports import reports
from tasks.tasks import tasks
from dashboard.dashboard import user_dashboard
from config import Config
from database import db, login_manager

app = Flask(__name__)
app.config.from_object(Config)

# Initialize the db with the app
db.init_app(app)
login_manager.init_app(app)

app.register_blueprint(auth)
app.register_blueprint(user_dashboard)
app.register_blueprint(tasks)
app.register_blueprint(reports)


@app.route("/")
def index():
    if current_user.is_authenticated:
        # If they are already logged in, skip the marketing page
        return redirect(url_for('user_dashboard.dashboard'))
    return render_template("home.html")


@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    with app.app_context():
        #This creates the tables in Postgres based on models.py
        #db.drop_all()
        db.create_all()
    app.run(debug=True)