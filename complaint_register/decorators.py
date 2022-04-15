from functools import wraps
from flask import abort, render_template, url_for
from flask_login import current_user

def moderator_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.admin:
            return render_template('error_page.html', error_message='Unauthorized Access!', redirect_url=url_for('auth_blueprint.login'))
        return f(*args, **kwargs)
    return decorated_function

def user_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.email_verified:
            return render_template('error_page.html', error_message='Unauthorized and unverified access!', redirect_url=url_for('auth_blueprint.login'))
        return f(*args, **kwargs)
    return decorated_function
