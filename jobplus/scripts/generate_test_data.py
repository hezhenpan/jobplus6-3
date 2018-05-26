# -*- coding: utf-8 -*-

import json
import os
from jobplus.models import db, User, ComInfo, JobInfo
from faker import Faker


fake = Faker()

def generate_data():
    db.create_all()
    with open(os.path.join(os.path.dirname(__file__), '.', 'datas', 'data.json')) as file:
        datas = json.load(file)
    for data in datas:
        if not data['company_name']:
            data['company_name'] = fake.name()
        user = User(
                    username = data['company_name'],
                    email = fake.word() + '@163.com',
                    password = '123456789',
                    role = User.ROLE_COMPANY
                ) 

        company = ComInfo(
                    com_phone = data['phone'],
                    com_web = data['website'],
                    com_location = data['company_locate'],
                    com_logo = data['company_logo'],
                    com_desc_less = data['desc_simple'],
                    com_desc_more = data['desc_more'],
                    user = user
                )

        db.session.add(user)
        db.session.add(company)
        for key, value in data['jobs'].items():
            if not key:
                key = fake.word()
            job = JobInfo(
                title = key,
                work_place = 'not on earth',
                tags = 'one,two,three',
                company=company
            )
            db.session.add(job)

        db.session.commit()


if __name__ == '__main__':
    generate_data()
