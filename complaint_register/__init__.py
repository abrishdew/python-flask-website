from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_login import LoginManager
from flask_mail import Mail
from flask_wtf.csrf import CSRFProtect

from .config import Config

db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()
mail = Mail()
limiter = Limiter(key_func=get_remote_address)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    limiter.init_app(app)

    login_manager.login_view = 'auth_blueprint.login'



    # auth route
    from .routes.auth import auth_bp
    app.register_blueprint(auth_bp)

    from .routes.complaint import complaint_bp
    app.register_blueprint(complaint_bp)

    from .routes.admin import admin_bp
    app.register_blueprint(admin_bp)

    @app.errorhandler(429)
    def rate_limit_exceeded(e):
        # Handle rate limit exceeded error
        return render_template('error_page.html', error_message='Too Many Requests...', redirect_url=url_for('complaint_blueprint.complaint')), 429

    return app

from .models import User
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)