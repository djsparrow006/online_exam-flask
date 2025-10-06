from database import db, init_db
from models import User
from werkzeug.security import generate_password_hash
from flask import Flask

app = Flask(__name__)
init_db(app)

with app.app_context():
    admin = User(username="admin", password=generate_password_hash("admin123"), role="admin")
    db.session.add(admin)
    db.session.commit()
    print("Admin user created successfully!")
