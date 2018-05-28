import re
from flask import Blueprint, render_template, url_for, flash, redirect, current_app
from jobplus.forms import LoginForm, RegisterForm, RegisterComForm
from flask_login import login_user, logout_user, login_required
from jobplus.models import User, ComInfo
from jobplus.models import JobInfo as Job


front = Blueprint('front', __name__)


# 首页路由函数
@front.route('/')
def index():
    pagination = Job.query.order_by(Job.created_at.desc()).paginate(
        page=1,
        per_page=current_app.config['INDEX_PER_PAGE'],
        error_out=False
    )

    com_pagination = ComInfo.query.order_by(ComInfo.created_at.desc()).paginate(
        page=1,
        per_page=current_app.config['COMINFO_PER_PAGE'],
        error_out=False
    )
    return render_template('index.html', pagination=pagination, com_pagination=com_pagination, active='jobs')


# 登录视图函数
@front.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    pattern = '\w[-\w.+]*@([A-Za-z0-9][-A-Za-z0-9]+.)+[A-Za-z]{2,14}'
    if form.validate_on_submit():
        if re.match(pattern, form.username_or_email.data):
            user = User.query.filter_by(email=form.username_or_email.data).first()
        else:
            user = User.query.filter_by(username=form.username_or_email.data).first()
        login_user(user, form.remember_me.data)
        if user.status:
            flash('登录成功', 'success')
            return redirect(url_for('.index'))
        else:
            flash('用户被禁用', 'danger')
    return render_template('login.html', form=form)


@front.route('/logout')
@login_required
def logout():
    logout_user()
    flash('您已经退出登录', 'success')
    return redirect(url_for('.index'))


# 注册视图函数
@front.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        form.create_user()
        flash('注册成功，请登录！', 'success')
        return redirect(url_for('.login'))
    return render_template('register.html', form=form)


# 企业注册函数
@front.route('/registercom', methods=['GET', 'POST'])
def register_com():
    form = RegisterComForm()
    if form.validate_on_submit():
        form.create_company()
        flash('注册成功，请登录！', 'success')
        return redirect(url_for('front.login'))
    return render_template('register_com.html', form=form)
