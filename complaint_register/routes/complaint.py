from flask import Blueprint, flash, render_template, redirect, url_for, request, send_file, current_app
from flask_login import current_user
from wtforms.validators import ValidationError

import os

from ..decorators import user_login_required
from ..forms import ComplaintForm
from ..models import Complaint
from .. import db

complaint_bp = Blueprint('complaint_blueprint', __name__)


@complaint_bp.route('/', methods=['GET', 'POST'])
@user_login_required
def complaint():
    form = ComplaintForm()
    form.user_id.data = current_user.user_id
    form.email.data = current_user.email
    form.username.data = current_user.username
    complaints = Complaint.query.filter_by(user_id=current_user.user_id)
    
    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                form.post_complaint()
                flash('Complaint has been successfully posted!', 'success')
                return redirect(url_for('complaint_blueprint.complaint'))
            except ValidationError as e:
                return render_template('error_page.html', error_message=e, redirect_url=url_for('complaint_blueprint.complaint'))
    

    return render_template('submit_complaint.html', form=form, complaints=[complaint.todict() for complaint in complaints])

@complaint_bp.route('/<complaint_id>', methods=['GET', 'POST'])
@user_login_required
def edit(complaint_id):
    complaint = Complaint.query.get(complaint_id).todict()
    form = ComplaintForm(obj=Complaint.query.get(complaint_id))
    form.user_id.data = complaint['user_id']
    form.email.data = complaint['email']
    form.username.data = complaint['username']
    form.file.data = complaint['file_path']

    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                form.edit_complaint(complaint_id)
                flash('Complaint has been successfully edited!', 'success')
                return redirect(url_for('complaint_blueprint.complaint'))
            except ValidationError as e:
                return render_template('error_page.html', error_message=e, redirect_url=url_for('complaint_blueprint.edit'))
    
    return render_template('edit_complaint.html', form=form, complaint=Complaint.query.get(complaint_id).todict())

@complaint_bp.route('/view_file/<complaint_id>', methods=['GET'])
@user_login_required
def view_file(complaint_id):
    complaint = Complaint.query.get(complaint_id)
    if current_user.user_id != complaint.user_id:
        return render_template('error_page.html', error_message='You are not authorized to view this file!', redirect_url=url_for('complaint_blueprint.complaint'))
    return send_file(os.path.join(current_app.config['UPLOAD_FOLDER'], complaint.file_path), as_attachment=True)

@complaint_bp.route('/delete_file/<complaint_id>', methods=['GET'])
def delete_file(complaint_id):
    complaint = Complaint.query.get(complaint_id)
    if current_user.user_id != complaint.user_id:
        return render_template('error_page.html', error_message='You are not authorized to delete this file!', redirect_url=url_for('complaint_blueprint.complaint'))
    if complaint.file_path:
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], complaint.file_path)
        if os.path.exists(file_path):
            os.remove(file_path)
        complaint.file_path = None
        db.session.commit()
    flash('File Successfully Deleted!')
    return redirect(url_for('complaint_blueprint.edit', complaint_id=complaint_id))