import os
from flask import Flask, redirect, url_for, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.debug = os.getenv("DEBUG")
app.permanent_session_lifetime = timedelta(minutes=5)

# Creating DB Object
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    user_type = db.Column(db.String(25), default="personal")
    status = db.Column(db.Integer, default=0)

    def __init__(self, name, email, password, user_type, status):
        self.name = name
        self.email = email
        self.password = password
        self.user_type = user_type
        self.status = status


@app.route("/")
def index():
    return render_template("home.html")


@app.route("/extra-info")
def extraInfo():
    return render_template("extra-info.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        email = request.form["email"]
        password = request.form["password"]

        if email == "" or password == "":
            return render_template("login", msg="Please enter required fields.")

        users = User.query.all()
        if len(users) == 0:
            return render_template(
                "login.html", msg="Username or Password incorrect. Please try again."
            )

        for user in users:
            if user.email == email and user.password == password:
                session["user_id"] = user.id
                session["name"] = user.name
                session["email"] = user.email
                session["userType"] = user.user_type

                if user.status == 0:
                    return redirect(url_for("extraInfo"))

        return redirect(url_for("index"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        userType = request.form["user_type"]

        if name == "" or email == "" or password == "" or userType == "":
            return render_template("register.html", msg="Please enter required fields.")

        if db.session.query(User).filter(User.email == email).count() != 0:
            return render_template(
                "login.html", msg="The user email already exists. Please try to login."
            )
        else:
            data = User(name, email, password, userType, 0)
            db.session.add(data)
            db.session.commit()

            # todo: Add message that user is created and try logining
            return redirect(url_for("login")) 
