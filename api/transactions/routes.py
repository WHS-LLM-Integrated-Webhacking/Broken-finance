from flask import Blueprint, request, jsonify
from db import get_db
from auth.decorators import token_required

transactions_bp = Blueprint('transactions', __name__)

@transactions_bp.route('/', methods=['POST'])
@token_required
def transactions(current_user):
    data = request.get_json()
    user_id = current_user[0]
    account_id = data['account_id']
    dest_account_id = data['dest_account']
    amount = data['amount']
    db = get_db()
    cursor = db.cursor()
    if user_id == 1: # is admin
        cursor.execute('SELECT balance FROM Accounts WHERE account_id = %s', (account_id,))
        current_balance = cursor.fetchone()
        if not current_balance or current_balance[0] <= 0:
            return jsonify({'message': 'Transaction Failed'}), 401
        cursor.execute('UPDATE Accounts SET balance = balance + %s WHERE account_id = %s', (amount, dest_account_id))
        cursor.execute('UPDATE Accounts SET balance = balance - %s WHERE account_id = %s', (amount, account_id))
        cursor.execute('INSERT INTO Transactions (user_id, account_id, dest_account_id, transaction_type, amount) VALUES (%s, %s, %s, %s, %s)',
                       (user_id, account_id, dest_account_id, 'AccountTransaction', amount))
        db.commit()
        return jsonify({'message': 'Transaction successfully complete'}), 201

    cursor.execute('SELECT balance FROM Accounts WHERE account_id = %s AND user_id = %s', (account_id, user_id))
    current_balance = cursor.fetchone()
    if not current_balance or current_balance[0] <= 0:
        return jsonify({'message': 'Transaction Failed'}), 401
    cursor.execute('UPDATE Accounts SET balance = balance + %s WHERE account_id = %s', (amount, dest_account_id))
    cursor.execute('UPDATE Accounts SET balance = balance - %s WHERE account_id = %s AND user_id = %s', (amount, account_id, user_id))
    cursor.execute('INSERT INTO Transactions (user_id, account_id, dest_account_id, transaction_type, amount) VALUES (%s, %s, %s, %s, %s)',
                   (user_id, account_id, dest_account_id, 'AccountTransaction', amount))
    db.commit()
    return jsonify({'message': 'Transaction successfully complete'}), 201

@transactions_bp.route('/<int:account_id>', methods=['GET'])
@token_required
def get_transactions(current_user, account_id):
    user_id = current_user[0]
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM Transactions WHERE account_id = %s AND user_id = %s', (account_id, user_id))
    transactions = cursor.fetchall()
    return jsonify([{
        'transaction_id': t[0],
        'account_id': t[1],
        'transaction_type': t[2],
        'amount': t[3],
        'transaction_date': t[4]
    } for t in transactions])