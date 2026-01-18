from waitress import serve
# Change this line:
from app import app 
from database import db, login_manager


if __name__ == '__main__':
    print("🚀 Trackly is starting on the local network...")
    print("Tell your coworkers to visit: http://10.1.0.52:5000") # Put your IP here
    # host='0.0.0.0' makes it available to everyone on the LAN/Wi-Fi
    with app.app_context():
        #This creates the tables in Postgres based on models.py
        #db.drop_all()
        db.create_all()
    serve(app, host='0.0.0.0', port=5000)