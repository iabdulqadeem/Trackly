# Trackly
Trackly is a task tracking application built using Flask and Bootstrap. It has multi-user support and can help users generate reports in PDF and present to the assigning authority in a Structured format.

# Trackly | Professional Task Management System

Trackly is a robust, Object-Oriented Task Management application built with **Python** and **Flask**, utilizing a **PostgreSQL** database for high-performance data persistence. 

## 🚀 Key Features
* **Dynamic Task Dashboard:** Real-time tracking of Pending, In-Progress, and Completed tasks.
* **Intelligent Sorting:** Custom priority logic (Monthly > Weekly > Daily) using SQLAlchemy CASE statements.
* **Automated Maintenance:** Background logic to archive completed tasks at the start of each month, ensuring a clutter-free UI.
* **Professional Reporting:** Generates custom PDF reports for specific date ranges using **WeasyPrint**.
* **Secure Authentication:** User-specific data isolation and secure password hashing.

## 🛠️ Technical Stack
* **Backend:** Python / Flask
* **Database:** PostgreSQL (with SQLAlchemy ORM)
* **Migrations:** Flask-Migrate (Alembic)
* **PDF Engine:** WeasyPrint
* **Frontend:** Bootstrap 5 / Jinja2 Templates

## 📂 Project Structure (OOP Design)
The project follows the **Factory Pattern** and **Blueprint** architecture for scalability:
- `/blueprints`: Modularized route handling.
- `/models`: Database schemas using OOP classes.
- `/static`: CSS, JS, and Image assets.
- `/templates`: Dynamic Jinja2 HTML templates.

## ⚙️ Installation
1. Clone the repo: `git clone https://github.com/YOUR_USERNAME/Trackly.git`
2. Create venv: `python -m venv venv`
3. Install dependencies: `pip install -r requirements.txt`
4. Initialize Database: `flask db upgrade`
5. Run: `python run_server.py`
