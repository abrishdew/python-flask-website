from werkzeug.security import check_password_hash
import uuid

from . import db


class User(db.Model):
    user_id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String, unique=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String(100))
    is_active = db.Column(db.Boolean, default=True)
    admin = db.Column(db.Boolean, default=False)
    email_verified = db.Column(db.Boolean, default=False)
    verification_token = db.Column(db.String)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def get_id(self):
        return str(self.user_id)

    def is_authenticated(self):
        return self.is_active

    def todict(self):
        return {
            "user_id": self.user_id,
            "username": self.username,
            "is_active": self.is_active,
            "email": self.email
        }


class Complaint(db.Model):
    complaint_id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String, db.ForeignKey('user.user_id'))
    complaint = db.Column(db.Text)
    file_path = db.Column(db.String(120))

    def todict(self):
        user = User.query.get(self.user_id).todict()
        return {
            "user_id": self.user_id,
            "username": user['username'],
            "email": user['email'],
            "complaint": self.complaint,
            "complaint_id": self.complaint_id,
            "file_path": self.file_path
        }