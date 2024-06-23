from flask import Blueprint, request, jsonify
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from db import get_db
import jwt
import datetime
from functools import wraps
from flask import current_app

auth_bp = Blueprint('auth', __name__)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('x-access-token')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            db = get_db()
            cursor = db.cursor()
            cursor.execute('SELECT * FROM Users WHERE user_id = %s', (data['user_id'],))
            current_user = cursor.fetchone()
        except:
            return jsonify({'message': 'Token is invalid!'}), 401
        return f(current_user, *args, **kwargs)
    return decorated

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')
    db = get_db()
    cursor = db.cursor()
    cursor.execute('INSERT INTO Users (username, password_hash, role) VALUES (%s, %s, %s)', 
                   (data['username'], hashed_password, data.get('role', 'user')))
    cursor.execute('SELECT user_id FROM Users WHERE username = %s AND password_hash = %s',
                   (data['username'], hashed_password))
    user = cursor.fetchone()[0]
    cursor.execute('INSERT INTO Customers (user_id, first_name, last_name, address, phone, email) VALUES (%s, %s, %s, %s, %s, %s)', 
                   (int(user), data['first_name'], data['last_name'], data['address'], data['phone'], data['email']))
    db.commit()
    return jsonify({'message': 'User registered successfully!'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM Users WHERE username = %s', (data['username'],))
    user = cursor.fetchone()
    if not user or not check_password_hash(user[2], data['password']):
        return jsonify({'message': 'Login failed!'}), 401
    
    token = jwt.encode({
        'user_id': user[0],
        'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=24)
    }, current_app.config['SECRET_KEY'], algorithm="HS256")

    return jsonify({'token': token})

@auth_bp.route('/edit', methods=['POST'])
@token_required
def edit(current_user):
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='pdkdf2:sha256')
    db = get_db()
    cursor = db.cursor()
    cursor.execute('UPDATE Users SET username = %s, password_hash = %s WHERE user_id = %s',
                   (data['username'], hashed_password, current_user[0]))
    db.commit()
    return jsonify({'message': 'User edited successfully!'}), 201

@auth_bp.route('/role', methods=['GET'])
@token_required
def get_user_role(current_user):
    return jsonify({'role': current_user[3]})