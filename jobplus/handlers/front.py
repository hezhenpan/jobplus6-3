from flask import Blueprint, render_template, url_for, flash, redirect
from jobplus.forms import LoginForm, RegisterForm

front = Blueprint('front', __name__)

# 首页路由函数
@front.route('/')
def index():
    return render_template('index.html')


# 登录视图函数
@front.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', form=form)


# 注册视图函数
@front.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        form.create_user()
        flash('注册成功，请登录！', 'success')
        return redirect(url_for('.login'))
    return render_template('register.html', form=form)
