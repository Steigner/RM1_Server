# UserMixin provide main features as if login user is autenticated etc ...
from flask_login import UserMixin
from . import db


# Database class:
#   input: UserMixin flask login, database model
#   return: stringify session token for eneable only 1 user
# Note: Architecture of sqlite databse of users, get whole structure of datas
class User(UserMixin, db.Model):
    __bind_key__ = "db_users"
    __tablename__ = "medic"
    id = db.Column("id", db.Integer, primary_key=True)
    email = db.Column("email", db.String(40), unique=True)
    username = db.Column("name", db.String(20))
    surname = db.Column("surname", db.String(20))
    department = db.Column("department", db.String(10))
    title = db.Column("title", db.String(5))
    password = db.Column("password", db.String(200), unique=True)
    session_token = db.Column("session_token", db.String(40), unique=True, index=True)

    role = db.Column("role", db.String(5))

    def get_id(self):
        return str(self.session_token)


# Database class:
#   input: database model
#   return: none
# Note: Architecture of db2 databse of users, get whole structure of datas
class Patient(db.Model):
    __bind_key__ = "db_patients"
    __tablename__ = "patients"
    id = db.Column("id", db.Integer, primary_key=True)
    pid = db.Column("PID", db.String(20), unique=True)
    name = db.Column("name", db.String(20))
    surname = db.Column("surname", db.String(20))
    adress = db.Column("adress", db.String(100))
    dob = db.Column("DOB", db.Date)
    contact = db.Column("contact", db.String(30))
    blood = db.Column("blood", db.String(2))
    photo = db.Column("photo", db.LargeBinary)
