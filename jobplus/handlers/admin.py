from flask import Blueprint, render_template, request, current_app, redirect, url_for, flash
from jobplus.decorators import super_admin_required
from jobplus.models import User, ComInfo, JobInfo
from jobplus.forms import db, UserForm, Add_UserForm, Add_ComForm, CompanyForm

admin = Blueprint('admin', __name__, url_prefix='/admin')


@admin.route('/')
@super_admin_required
def index():
    return render_template('admin/admin_base.html')


@admin.route('/jobs')
@super_admin_required
def jobs():
    page = request.args.get('page', default=1, type=int)
    pagination = JobInfo.query.paginate(
        page=page,
        per_page=current_app.config['ADMIN_PER_PAGE'],
        error_out=False
    )
    return render_template('admin/jobs.html', pagination=pagination)


@admin.route('/jobs/<int:job_id>/update')
@super_admin_required
def reverse_job_status(job_id):
    job = JobInfo.query.get_or_404(job_id)
    job.change_status()
    db.session.add(job)
    db.session.commit()
    flash('操作成功', 'success')
    return redirect(url_for('admin.jobs'))


@admin.route('/users')
@super_admin_required
def users():
    page = request.args.get('page', default=1, type=int)
    pagination = User.query.paginate(
        page=page,
        per_page=current_app.config['ADMIN_PER_PAGE'],
        error_out=False
    )
    return render_template('admin/admin_user.html', pagination=pagination)


@admin.route('/users/create', methods=['GET', 'POST'])
@super_admin_required
def create_user():
    form = Add_UserForm()
    if form.validate_on_submit():
        form.create_user()
        flash('用户创建成功', 'success')
        return redirect(url_for('admin.users'))
    return render_template('admin/create_user.html', form=form)


@admin.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
@super_admin_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    form = UserForm(obj=user)
    if form.validate_on_submit():
        form.set_info(user)
        flash('用户更新成功', 'success')
        return redirect(url_for('admin.users'))
    form.realname.data = user.username
    form.email.data = user.email
    form.phone.data = user.phone
    form.exp.data = user.exp
    form.resume.data = user.resume
    return render_template('admin/edit_user.html', form=form, user=user)


@admin.route('/users/<int:user_id>/update')
@super_admin_required
def reverse_user_status(user_id):
    user = User.query.get_or_404(user_id)
    user.status = not user.status
    db.session.add(user)
    db.session.commit()
    flash('操作成功', 'success')
    return redirect(url_for('admin.users'))


@admin.route('/comps/addcompany', methods=['GET', 'POST'])
@super_admin_required
def add_company():
    form = Add_ComForm()
    if form.validate_on_submit():
        form.create_company()
        flash('公司创建成功', 'success')
        return redirect(url_for('admin.users'))
    return render_template('admin/create_company.html', form=form)


@admin.route('/comps/<int:com_id>/edit', methods=['GET', 'POST'])
@super_admin_required
def edit_company(com_id):
    comp = ComInfo.query.get_or_404(com_id)
    user = User.query.get_or_404(com_id)
    form = CompanyForm(obj=comp)
    if form.validate_on_submit():
        form.set_details(comp.user, comp)
        flash('企业更新成功', 'success')
        return redirect(url_for('admin.users'))
    form.com_name.data = user.username
    form.com_email.data = user.email
    return render_template('admin/edit_company.html', form=form, comp=comp)

