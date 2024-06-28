from flask import Blueprint, request, jsonify
from db import get_db
from auth.decorators import token_required, admin_required

accounts_bp = Blueprint('accounts', __name__)

@accounts_bp.route('/add', methods=['POST'])
@token_required
def add_account(current_user):
    data = request.get_json()
    db = get_db()
    cursor = db.cursor()
    cursor.execute('INSERT INTO Accounts (user_id, account_type, account_name, balance) VALUES (%s, %s, %s, %s)', 
                   (current_user[0], data['account_type'], data['account_name'], 0))
    db.commit()
    return jsonify({'account_id': cursor.lastrowid}), 201

@accounts_bp.route('/admin-add', methods=['POST'])
@admin_required
def admin_add_account(current_user):
    data = request.get_json()
    db = get_db()
    cursor = db.cursor()
    cursor.execute('INSERT INTO Accounts (user_id, account_type, account_name, balance) VALUES (%s, %s, %s, %s)', 
                   (data['user_id'], data['account_type'], data['account_name'], 0))
    db.commit()
    return jsonify({'account_id': cursor.lastrowid}), 201

@accounts_bp.route('/get-all-account', methods=['GET'])
@token_required
def get_all_account(current_user):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM Accounts WHERE user_id = %s', (current_user[0],))
    accounts = cursor.fetchall()
    if not accounts:
        return jsonify({'error': 'Account not found'}), 404
    return jsonify([{
            "account_id": i[0],
            "user_id": i[1],
            "account_name": i[2],
            "account_type": i[3],
            "balance": i[4],
            "created_at": i[5]
        } for i in accounts])

@accounts_bp.route('/<int:account_id>/<int:user_id>/check', methods=['GET'])
@admin_required
def check_account_id(current_user, account_id, user_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT 1 FROM Accounts WHERE account_id = %s AND user_id = %s', (account_id, user_id))
    is_valid_account = cursor.fetchone()[0]
    if is_valid_account: return jsonify({'message': 'Account id checked!'}), 201
    return jsonify({'message': 'Valid account id.'}), 401

@accounts_bp.route('/<int:account_id>', methods=['GET'])
@token_required
def get_account(current_user, account_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM Accounts WHERE account_id = %s', (account_id,))
    account = cursor.fetchone()
    if account:
        return jsonify({
            'account_id': account[0],
            'user_id': account[1],
            'account_type': account[2],
            'account_name': account[3],
            'balance': account[4],
            'created_at': account[5],
        })
    else:
        return jsonify({'error': 'Account not found'}), 401

@accounts_bp.route('/<int:account_id>/balance', methods=['GET'])
@token_required
def get_balance(current_user, account_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT balance FROM Accounts WHERE account_id = %s', (account_id,))
    balance = cursor.fetchone()
    if balance:
        return jsonify({'balance': balance[0]})
    else:
        return jsonify({'error': 'Account not found'}), 404