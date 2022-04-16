from complaint_register import db, create_app

app = create_app()
app.app_context().push()

db.create_all()

import os
from dotenv import load_dotenv
load_dotenv()

user_name = os.environ.get('ADMIN_USER_NAME')
password = os.environ.get('ADMIN_PASSWORD')
email = os.environ.get('ADMIN_EMAIL')

from complaint_register.models import User
from werkzeug.security import generate_password_hash

admin = User(username=user_name, password=generate_password_hash(password), email=email, is_active=True, admin=True, email_verified=True)

db.session.add(admin)
db.session.commit()