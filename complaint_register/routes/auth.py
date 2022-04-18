from flask import Blueprint, render_template, url_for, redirect, flash, request
from flask_login import login_user, current_user, logout_user
from werkzeug.security import check_password_hash

from .. import db, limiter
from ..models import User
from ..forms import LoginForm, RegistrationForm
from ..decorators import moderator_required

auth_bp = Blueprint('auth_blueprint', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
@limiter.limit('5/minute')
def login():
    form = LoginForm()
    if form.validate_on_submit():
        try:
            user = User.query.filter_by(username=form.username.data).first()
            if user and check_password_hash(user.password, form.password.data):
                if not user.email_verified:
                    flash('Please verify your email before logging in.', 'warning')
                    return redirect(url_for('auth_blueprint.login'))
                login_user(user)
                if user.admin == True:
                    return redirect(url_for('admin_blueprint.admin'))
                if not user.is_active:
                    flash('User has been deactivated! Contact moderator')
                    return redirect(url_for('auth_blueprint.login'))
                return redirect(url_for('complaint_blueprint.complaint'))
        except AssertionError as e:
            return render_template('error_page.html', error_message=e, redirect_url=url_for('auth_blueprint.login'))

    return render_template('login.html', form=form)

@auth_bp.route('/verify_email/<token>', methods=['GET'])
def verify_email(token):
    user = User.query.filter_by(verification_token=token).first()

    if user:
        user.email_verified = True
        db.session.commit()
        flash('Email verified successfully!', 'success')
        return redirect(url_for('auth_blueprint.login'))
    else:
        flash('Invalid verification token.', 'danger')
        return redirect(url_for('auth_blueprint.signup'))

@auth_bp.route('/signup', methods=['GET', 'POST'])
@limiter.limit('5/minute')
def signup():
    form = RegistrationForm()
    try:
        if request.method == 'POST':
            if form.validate_on_submit():
                # potential threat
                if form.honeypot.data:
                    flash('Potential Threat Detected!')
                    return redirect(url_for('auth_blueprint.login'))
                form.create_user()

                flash('Account created successfully. Please check your email for verification instructions.', 'success')
                return redirect(url_for('auth_blueprint.login'))
    except ValueError as e:
        return render_template('error_page.html', error_message=e, redirect_url=url_for('auth_blueprint.signup'))
    
    return render_template('signup.html', form=form)

@auth_bp.route('/logout')
def logout():
    if current_user.is_authenticated:
        if current_user.admin:
            logout_moderator()
        else:
            logout_user()
    
    flash('User not logged in!')
    return redirect(url_for('auth_blueprint.login'))

@moderator_required
def logout_moderator():
    flash('Moderator logged out', 'info')
    logout_user()

