import datetime

from app import db
from sqlalchemy.orm import relationship
from Users_list import USERS
from Orders_list import ORDERS
from Offers_list import OFFERS



class UserRole(db.Model):
    __tablename__ = 'user_roles'

    id = db.Column(db.Integer, primary_key=True)
    role_type = db.Column(db.String(100))

    user_role = relationship('User')



class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    email = db.Column(db.String(100))
    role_id = db.Column(db.Integer, db.ForeignKey('user_roles.id'))
    phone = db.Column(db.String(100))

    role = relationship('UserRole')
    # orders = relationship('Order')

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "age": self.age,
            "email": self.email,
            "role": self.role,
            "phone": self.phone
        }


class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(300))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    address = db.Column(db.String(100))
    price = db.Column(db.Float)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    executor_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    customer = relationship('User', foreign_keys=id)
    executor = relationship('User', foreign_keys=id)

    def start_date_fix(self):
        """
        fixing start date
        """
        month_start, day_start, year_start = self.split("/")
        return datetime.date(year=int(year_start), month=int(month_start), day=int(day_start))

    def end_date_fix(self):
        """
        fixing end date
        """
        month_end, day_end, year_end = self.split("/")
        return datetime.date(year=int(year_end), month=int(month_end), day=int(day_end))

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "start_date": self.start_date_fix,
            "end_date": self.end_date_fix,
            "address": self.address,
            "price": self.price,
            "customer_id": self.customer_id,
            "executor_id": self.executor_id
        }


class Offer(db.Model):
    __tablename__ = 'offer'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    executor_id = db.Column(db.Integer, db.ForeignKey('order.executor_id'))

    order = relationship('Order', foreign_keys=order_id)
    executor = relationship('User', foreign_keys=executor_id)

    def to_dict(self):
        return {
            "id": self.id,
            "order_id": self.order_id,
            "executor_id": self.executor_id
        }


db.drop_all()
db.create_all()

for user in USERS:
    # print(user['role'])
    db.session.add(UserRole(
        id=user['id'],
        role_type=user['role']
    ))
    db.session.commit()

# for user in USERS:
#
#     print(user.to_dict())

#     db.session.add(user.to_dict())
#     db.session.commit()
#
# for order in ORDERS:
#     db.session.add(order.to_dict())
#     db.session.commit()
#
# for offer in OFFERS:
#     db.session.add(offer.to_dict())
#     db.session.commit()
