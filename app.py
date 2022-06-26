import json
from datetime import datetime

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

from models import User, Order, Offer

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///base.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
db = SQLAlchemy(app)


@app.route('/users', methods=['GET', 'POST'])
def get_users():
    if request.method == 'GET':
        user_list = []
        for user in User.query.all():
            user_list.append(user)
        return jsonify(user_list)

    if request.method == 'POST':
        user = json.loads(request.data)
        additional_user = User(
            id=user['id'],
            first_name=user['first_name'],
            last_name=user['last_name'],
            age=user['age'],
            email=user['email'],
            role_id=user['role_id'],
            phone=user['phone']
        )
        db.session.add(additional_user)
        db.session.commit()
        db.session.close()
        return "Пользователь добавлен"


@app.route('/orders', methods=['GET', 'POST'])
def get_orders():
    if request.method == 'GET':
        order_list = []
        for order in Order.query.all():
            order_list.append(order.to_dict())
        return jsonify(order_list)

    if request.method == 'POST':
        order = json.loads(request.data)

        additional_order = Order(
            id=order['id'],
            name=order['name'],
            description=order['description'],
            start_date=datetime.strptime(order['start_date'], '%m/%d/%Y'),
            end_date=datetime.strptime(order['end_date'], '%m/%d/%Y'),
            address=order['address'],
            price=order['price'],
            customer_id=order['customer_id'],
            executor_id=order['executor_id']
        )
        db.session.add(additional_order)
        db.session.commit()
        db.session.close()
        return "Заказ добавлен в базу данных"


@app.route('/users/<int:user_id>', methods=['GET', 'PUT', 'DELETE'])
def get_user(user_id):
    if request.method == 'GET':
        user = User.query.get(user_id)

        if user is None:
            return "Пользователь не найден"

        return jsonify(user)
    if request.method == 'PUT':
        user_data = json.loads(request.data)
        user = db.session.query(User).get(user_id)

        if user is None:
            return "Пользователь не найден"

        user.first_name = user_data['first_name']
        user.last_name = user_data['last_name']
        user.age = user_data['age']
        user.email = user_data['email']
        user.role_id = user_data['role_id']
        user.phone = user_data['phone']
        db.session.add(user)
        db.session.commit()

        return f"Пользователь с id {user_id} изменен"
    if request.method == 'DELETE':
        user = db.session.query(User).get(user_id)

        if user is None:
            return "Пользователь не найден"

        db.session.delete(user)
        db.session.commit()
        db.session.close()
        return f"Пользователь с id {user_id} удален"


@app.route('/orders/<int:order_id>', methods=['GET', 'PUT', 'DELETE'])
def get_order(order_id):
    if request.method == 'GET':
        order = Order.query.get(order_id)

        if order is None:
            return "Заказ не найден"

        else:
            return jsonify(order.to_dict())
    if request.method == 'PUT':
        order_data = json.loads(request.data)
        order = db.session.query(Order).get(order_id)

        if order is None:
            return "Заказ не найден"

        order.name = order_data['name']
        order.description = order_data['description']
        order.start_date = datetime.strptime(order['start_date'], '%m/%d/%Y'),
        order.end_date = datetime.strptime(order['end_date'], '%m/%d/%Y'),
        order.address = order_data['address']
        order.price = order_data['price']
        order.customer_id = order_data['customer_id']
        order.executor_id = order_data['executor_id']

        db.session.add(order)
        db.session.commit()
        db.session.close()
        return f"Заказа с номером id {order_id} изменен"

    if request.method == 'DELETE':
        order = db.session.query(Order).get(order_id)

        if order is None:
            return "Заказ не найден"

        db.session.delete(order)
        db.session.commit()
        db.session.close()

        return f"Заказ с id {order_id} удален"


@app.route('/offers', methods=['GET', 'POST'])
def get_offers():
    if request.method == 'GET':
        offer_list = []
        for offer in Offer.query.all():
            offer_list.append(offer.to_dict())
        return jsonify(offer_list)
    if request.method == 'POST':
        offer = json.loads(request.data)
        new_offer_obj = Offer(
            id=offer['id'],
            order_id=offer['order_id'],
            executor_id=offer['executor_id']
        )
        db.session.add(new_offer_obj)
        db.session.commit()
        db.session.close()
        return "Предложение добавлено в базу данных"


@app.route('/offers/<int:offer_id>', methods=['GET', 'PUT', 'DELETE'])
def get_offer(offer_id):
    if request.method == 'GET':
        offer = Offer.query.get(offer_id)

        if offer is None:
            return "Предложение не найдено"

        else:
            return jsonify(offer.to_dict())
    if request.method == 'PUT':
        offer_data = json.loads(request.data)
        offer = db.session.query(Offer).get(offer_id)

        if offer is None:
            return "Предложение не найден"

        offer.order_id = offer_data['order_id']
        offer.executor_id = offer_data['executor_id']

        db.session.add(offer)
        db.session.commit()
        return f"Предложение с номером id {offer_id} изменено"

    if request.method == 'DELETE':
        offer = db.session.query(Offer).get(offer_id)

        if offer is None:
            return "Предложение не найдено"

        db.session.delete(offer)
        db.session.commit()
        db.session.close()

        return f"Предложение с id {offer_id} удалено"


if __name__ == '__main__':
    app.run()
