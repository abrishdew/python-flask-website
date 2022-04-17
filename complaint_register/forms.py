from flask import current_app
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FileField, SubmitField, HiddenField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, ValidationError, Regexp
from flask_wtf.file import FileAllowed
from flask_wtf.recaptcha import RecaptchaField
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename

import os
import uuid

from complaint_register.mails import send_verification_email
from complaint_register import db
from .models import User, Complaint
from .mails import generate_verification_token


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

    def validate_username(self, field):
        user = User.query.filter_by(username=field.data).first()
        if not user:
            raise ValidationError('Invalid credentials!')

    def validate_password(self, field):
        user = User.query.filter_by(username=self.username.data).first()
        if user and not user.check_password(field.data):
            raise ValidationError('Invalid credentials!')

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    honeypot = StringField('HoneyPot')
    captcha = RecaptchaField()
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6), Regexp(
        r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9]).*$',
        message="Password must contain at least one uppercase letter, one lowercase letter, and one digit"
    )])

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already taken.')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def create_user(self):
        token = generate_verification_token()
        user = User(
            username=self.username.data,
            email=self.email.data,
            password=generate_password_hash(self.password.data),
            verification_token=token
        )
        db.session.add(user)
        db.session.commit()
        try:
            send_verification_email(user)
        except Exception as e:
            raise Exception(e)

class ComplaintForm(FlaskForm):
    complaint_id = HiddenField('Complaint ID')
    user_id = StringField('User ID', render_kw={'readonly': True})
    username = StringField('Name', render_kw={'readonly': True})
    email = StringField('Email', render_kw={'readonly': True})
    complaint = TextAreaField('Complaint', validators=[DataRequired()])
    file = FileField(label='File (PDF)', validators=[FileAllowed(['pdf'])])
    captcha = RecaptchaField()

    def validate_file(self, file):
        max_size = 5 * 1024 * 1024  # 5 MB
        if file.data and file.data.content_length > max_size:
            raise ValidationError('File size exceeds the allowed limit.')

    def post_complaint(self):
        new_complaint = Complaint(
            user_id=self.user_id.data,
            complaint=self.complaint.data,
        )

        if self.file.data:
            filename = str(uuid.uuid4()) + '_' + \
                secure_filename(self.file.data.filename)
            file_path = os.path.join(
                current_app.config['UPLOAD_FOLDER'], filename)
            self.file.data.save(file_path)
            new_complaint.file_path = file_path

        db.session.add(new_complaint)
        db.session.commit()
    
    def edit_complaint(self, complaint_id):
        complaint = Complaint.query.get(complaint_id)
        
        complaint.complaint = self.complaint.data
        if self.file.data:
            filename = str(uuid.uuid4()) + '_' + \
                secure_filename(self.file.data.filename)
            file_path = os.path.join(
                current_app.config['UPLOAD_FOLDER'], filename)
            self.file.data.save(file_path)
            complaint.file_path = file_path
        
        db.session.commit()

class DeactivateUserForm(FlaskForm):
    submit = SubmitField('Deactivate')
