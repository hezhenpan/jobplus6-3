# *_*coding:utf-8 *_*

from faker import Faker
from jobplus.models import db, User, JobInfo, ComInfo

fake = Faker


# 生成一个普通用户
def iter_users():
    yield User(
        username="xiaohe",
        email="xiaohe@jobplus.com",
        password="123456",
        role=User.ROLE_USER
    )


def iter_companies():
    user = User.query.filter_by(username="xiaohe").first()
    yield ComInfo(
        user=user,
        com_phone="13800000000",
        com_location="北京市朝阳区北辰世纪中心",
        com_logo="https://www.baidu.com/img/baidu_jgylogo3.gif",
        com_web="www.thissite.com",
        com_desc_less="this is a brief",
        com_desc_more="this is a detail desc"
    )


def iter_jobs():
    company = ComInfo.query.filter_by(com_phone="13800000000").first()
    for i in range(10):
        yield JobInfo(
            title="标题标题" + str(i),
            work_place="工作地点地点",
            tags="标签1,标签2,标签3",
            desc="这里是描述",
            high_salary=1002,
            low_salary=100,
            exp=5,
            degree="博士",
            isonline=1,
            company=company
        )


def run():
    for user in iter_users():
        db.session.add(user)

    for cmp in iter_companies():
        db.session.add(cmp)

    for job in iter_jobs():
        db.session.add(job)

    try:
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()
