from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    # MySQL connection with your credentials
    app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://root:root@localhost/online_exam1"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    with app.app_context():
        db.create_all()
