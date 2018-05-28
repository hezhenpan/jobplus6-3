# *_* coding: utf-8 *_*

from flask import abort
from flask_login import current_user
from functools import wraps
from jobplus.models import User

def role_required(role):
    """
        带参数的装饰器，用它来保护路由函数只被特定的用户访问
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not current_user.is_authenticated or current_user.role < role:
                abort(404)
            return func(*args, **kwargs)
        return wrapper
    return decorator


# 企业用户装饰器
company_required = role_required(User.ROLE_COMPANY)
# 超级管理员才具有对user的操作权限
super_admin_required = role_required(User.ROLE_ADMIN)

