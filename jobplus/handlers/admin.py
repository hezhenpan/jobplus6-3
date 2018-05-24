from flask import Blueprint, render_template, request, current_app, redirect, url_for, flash
from jobplus.decorators import admin_required
from jobplus.models import User
from jobplus.forms import db, UserForm, RegisterForm

admin = Blueprint('admin', __name__, url_prefix='/admin')


@admin.route('/')
@admin_required
def index():
    return render_template('admin/admin_base.html')


@admin.route('/users')
@admin_required
def users():
    page = request.args.get('page', default=1, type=int)
    pagination = User.query.paginate(
        page=page,
        per_page=current_app.config['ADMIN_PER_PAGE'],
        error_out=False
    )
    return render_template('admin/admin_user.html', pagination=pagination)


@admin.route('/users/create', methods=['GET', 'POST'])
@admin_required
def create_user():
    form = RegisterForm()
    if form.validate_on_submit():
        form.create_user()
        flash('用户创建成功', 'success')
        return redirect(url_for('admin.users'))
    return render_template('admin/create_user.html', form=form)


@admin.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    form = UserForm(obj=user)
    if form.validate_on_submit():
        form.set_info(user)
        flash('用户更新成功', 'success')
        return redirect(url_for('admin.users'))
    return render_template('admin/edit_user.html', form=form, user=user)


@admin.route('/users/<int:user_id>/delete')
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('用户删除成功', 'success')
    return redirect(url_for('admin.users'))
