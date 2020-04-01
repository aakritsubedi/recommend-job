import os
from flask import Flask, redirect, url_for, render_template, request, session
import json
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from datetime import timedelta
from werkzeug.utils import secure_filename

load_dotenv()


app = Flask(__name__)

PIC_FOLDER = "static/uploads/profile/"
CV_FOLDER = "static/uploads/cv/"
app.config["PIC_FOLDER"] = PIC_FOLDER
app.config["CV_FOLDER"] = CV_FOLDER
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


class ExtraInfo(db.Model):
    __tablename__ = "extra-info"
    id = db.Column(db.Integer, primary_key=True)
    photo = db.Column(db.String(100), default="defaultUser.png")
    bio = db.Column(db.Text())
    cv = db.Column(db.String(100))
    skillsset = db.Column(db.Text())
    education = db.Column(db.Text())
    jobs = db.Column(db.Text())
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship("User", backref=db.backref("users", uselist=False))
    status = db.Column(db.Integer)

    def __init__(self, photo, bio, cv, skillsset, education, jobs, user_id, status):
        self.photo = photo
        self.bio = bio
        self.cv = cv
        self.skillsset = skillsset
        self.education = education
        self.jobs = jobs
        self.user_id = user_id
        self.status = status


@app.route("/")
def index():
    return render_template("home.html")


@app.route("/extra-info", methods=["GET", "POST"])
def extraInfo():
    if request.method == "GET":
        return render_template("extra-info.html")
    else:
        profilePic = request.files["profile_pic"]
        photo = secure_filename(profilePic.filename)
        profilePic.save(os.path.join(app.config["PIC_FOLDER"], photo))
        bio = request.form["bio"]
        fileCV = request.files["cv"]
        cv = secure_filename(fileCV.filename)
        fileCV.save(os.path.join(app.config["CV_FOLDER"], cv))
        skillsset = request.form["skillsset"]
        schools = request.form.getlist("school[]")
        degrees = request.form.getlist("degree[]")
        edu = []
        for (school, degree) in zip(schools, degrees):
            edu.append({"school": school, "degree": degree})
        edu=json.dumps(edu)
        offices = request.form.getlist("office[]")
        descs = request.form.getlist("desc[]")
        jobs = []
        for (office, desc) in zip(offices, descs):
            jobs.append({"office": office, "desc": desc})
        jobs=json.dumps(jobs)
        user_id = session.get("user_id")

        data = ExtraInfo(photo, bio, cv, skillsset, edu, jobs, user_id, 1)
        db.session.add(data)
        db.session.commit()

        return redirect(url_for("index"))


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
