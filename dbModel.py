from app import db

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
