# import json
import json
from datetime import datetime

from models import *

from Orders_list import ORDERS
from Users_list import USERS
from Offers_list import OFFERS
from UsersRole_list import USERSROLE


# def add_role_id():
#     USERS_with_id=[]
#     for user in USERS:
#         user['role_id'] = user['id']
#         USERS_with_id.append(user)
#     with open('Users_list.py', 'w') as outfile:
#         json.dump(USERS_with_id, outfile, indent=4)

#
# add_role_id()


def upload_user_table():
    for user_r in USERSROLE:
        db.session.add(UserRole(
            id=user_r['id'],
            role_type=user_r['role_type'])
        )
        db.session.commit()

    for user in USERS:
        db.session.add(User(
            id=user['id'],
            first_name=user['first_name'],
            last_name=user['last_name'],
            age=user['age'],
            email=user['email'],
            role_id=user['role_id'],
            phone=user['phone'])
        )
        db.session.commit()

    for order in ORDERS:
        db.session.add(Order(
            id=order['id'],
            name=order['name'],
            description=order['description'],
            start_date=datetime.strptime(order['start_date'], '%m/%d/%Y'),
            end_date=datetime.strptime(order['end_date'], '%m/%d/%Y'),
            address=order['address'],
            price=order['price'],
            customer_id=order['customer_id'],
            executor_id=order['executor_id']
        ))
        db.session.commit()

    for offer in OFFERS:
        db.session.add(Offer(
            id=offer['id'],
            order_id=offer['order_id'],
            executor_id=offer['executor_id']
        ))

        db.session.commit()
    db.session.close()


upload_user_table()

#  primaryjoin


# def start_date_fix(order):
#     """
#     fixing start date
#     """
#     month_start, day_start, year_start = order['start_date'].split("/")
#     return datetime.date(year=int(year_start), month=int(month_start), day=int(day_start))
#
#
# def end_date_fix(order):
#     """
#     fixing end date
#     """
#     month_end, day_end, year_end = order['end_date'].split("/")
#     return datetime.date(year=int(year_end), month=int(month_end), day=int(day_end))
#
#
# def add_orders_to_db(self):
#     pass

#
# def create_users_role():
#     user_role_list = []
#     for user in USERS:
#         user_role_list.append({'id': user['id'], 'role_type': user['role']})
#
#     with open('UsersRole_list.py', 'w') as outfile:
#         json.dump(UserRole, outfile)

