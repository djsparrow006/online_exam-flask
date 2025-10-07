from database import db
from models import User
from werkzeug.security import generate_password_hash
from flask import Flask
import os

app = Flask(__name__)

# Set your Render database URL here
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", "postgresql+psycopg://danis_9mb2_user:zyaJq3666CoBF9auRtBp1lAFWOIpsVjc@dpg-d3ht8sggjchc73apb1vg-a:5432/danis_9mb2")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    # Check if admin already exists
    if User.query.filter_by(username="admin").first():
        print("Admin already exists.")
    else:
        # Create admin user
        admin = User(
            username="admin",
            password=generate_password_hash("nannallavan"),
            role="admin"
        )
        db.session.add(admin)
        db.session.commit()
        print("Admin created successfully!")
