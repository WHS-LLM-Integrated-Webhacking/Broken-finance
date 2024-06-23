from flask import Blueprint, request, jsonify
from db import get_db
from auth.decorators import token_required

customers_bp = Blueprint('customers', __name__)

@customers_bp.route('/add', methods=['POST'])
@token_required
def add_customer(current_user):
    data = request.get_json()
    db = get_db()
    cursor = db.cursor()
    cursor.execute('INSERT INTO Customers (first_name, last_name, address, phone, email) VALUES (%s, %s, %s, %s, %s)', 
                   (data['first_name'], data['last_name'], data['address'], data['phone'], data['email']))
    db.commit()
    return jsonify({'customer_id': cursor.lastrowid}), 201

@customers_bp.route('/get', methods=['GET'])
@token_required
def get_customer(current_user):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM Customers WHERE user_id = %s', (current_user[0],))
    customer = cursor.fetchone()
    if customer:
        return jsonify({
            'customer_id': customer[0],
            'first_name': customer[1],
            'last_name': customer[2],
            'address': customer[3],
            'phone': customer[4],
            'email': customer[5]
        })
    else:
        return jsonify({'error': 'Customer not found'}), 404

@customers_bp.route('/update', methods=['PUT'])
@token_required
def update_customer(current_user):
    data = request.get_json()
    db = get_db()
    cursor = db.cursor()
    cursor.execute('UPDATE Customers SET first_name = %s, last_name = %s, address = %s, phone = %s, email = %s WHERE user_id = %s',
                   (data['first_name'], data['last_name'], data.get('address'), data.get('phone'), data.get('email'), current_user[0]))
    db.commit()
    return jsonify({'message': 'Customer updated successfully'}), 200

@customers_bp.route('/delete', methods=['DELETE'])
@token_required
def delete_customer(current_user):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('DELETE FROM Customers WHERE customer_id = %s', (current_user[0],))
    db.commit()
    return jsonify({'message': 'Customer deleted successfully'}), 200