from flask import Blueprint, render_template, flash, redirect, url_for
from ..models import Complaint, User
from ..decorators import moderator_required
from ..forms import DeactivateUserForm
from .. import db

admin_bp = Blueprint('admin_blueprint', __name__)


@admin_bp.route('/admin', methods=['GET'])
@moderator_required
def admin():
    users = User.query.all()
    complaints = Complaint.query.all()
    form = DeactivateUserForm()

    return render_template('admin.html', users=[user.todict() for user in users], complaints=[complaint.todict() for complaint in complaints], form=form)


@admin_bp.route('/toggle_user_status/<string:user_id>', methods=['POST'])
@moderator_required
def toggle_user_status(user_id):
    # Retrieve the user from the database based on the user_id
    user = User.query.get(user_id)
    
    if user:
        # Toggle the user's active state
        if user.admin:
            flash('Can not deactivate admin account!')
            return redirect(url_for('admin_blueprint.admin'))
        user.is_active = not user.is_active
        db.session.commit()

    return redirect(url_for('admin_blueprint.admin'))
