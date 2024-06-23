from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
import requests

API = "http://api:5000"

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        response = requests.post(API + '/api/auth/login', json={'username': username, 'password': password})
        if response.status_code == 200:
            session['user'] = response.json()
            flash('Login successful!', 'success')
            return jsonify({'token': session['user']})
            # return redirect(url_for('main.index'))
        else:
            flash('Login failed!', 'danger')
    return render_template('login.html')

@main.route('/logout', methods=['GET'])
def logout():
    session.pop('user', None)
    return redirect(url_for('main.login'))       

@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = {
            'username': request.form['username'],
            'password': request.form['password'],
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'address': request.form['address'],
            'phone': request.form['phone'],
            'email': request.form['email'],
            'role': 'user'
        }
        response = requests.post(API + '/api/auth/register', json=data)
        if response.status_code == 201:
            flash('Registration successful!', 'success')
            return redirect(url_for('main.login'))
        else:
            flash('Registration failed!', 'danger')
    return render_template('register.html')

@main.route('/me/', methods=['GET', 'POST'])
def customer_detail():
    try:
        headers = {'x-access-token': session['user']['token']}
    except KeyError: return redirect(url_for('main.login'))
    if request.method == 'POST':
        user_data = {
            'username': request.form['username'],
            'password': request.form['password'],
        }
        customer_data = {
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'address': request.form.get('address'),
            'phone': request.form.get('phone'),
            'email': request.form.get('email')
        }
        user_response = requests.put(API + '/api/auth/edit', json=user_data, headers=headers)
        customer_response = requests.put(API + '/api/customers/update', json=customer_data, headers=headers)
        response = requests.get(API + '/api/customers/get')
        customer = response.json()
        if user_response.status_code == 200 and customer_response.status_code == 200:
            flash('Customer information updated successfully!', 'success')
        else:
            flash('Failed to update customer information!', 'danger')
        return redirect(url_for('main.customer_detail'))
    
    response = requests.get(API + '/api/customers/get', headers=headers)
    customer = response.json()
    return render_template('customers.html', customer=customer)

@main.route('/accounts', methods=['GET'])
def accounts():
    try:
        headers = {'x-access-token': session['user']['token']}
    except KeyError: return redirect(url_for('main.login'))
    response = requests.get(API + '/api/accounts/get-all-account', headers=headers)
    if response.status_code == 404:
        return redirect(url_for('main.add_account'))
    accounts = response.json()
    return render_template('accounts.html', accounts=accounts)

@main.route('/accounts/add', methods=['GET', 'POST'])
def add_account():
    try:
        headers = {'x-access-token': session['user']['token']}
    except KeyError: return redirect(url_for('main.login'))
    if request.method == 'POST':
        data = {
            'account_type': request.form['account_type'],
            'account_name': request.form['account_name']
        }
        response = requests.post(API + '/api/accounts/add', json=data, headers=headers)
        if response.status_code == 201:
            flash('Account added successfully!', 'success')
            return redirect(url_for('main.accounts'))
        else:
            flash('Failed to add account!', 'danger')
    return render_template('account_add.html')

@main.route('/accounts/<int:account_id>/transactions', methods=['GET', 'POST'])
def transactions(account_id):
    try:
        headers = {'x-access-token': session['user']['token']}
    except KeyError: return redirect(url_for('main.login'))

    if request.method == 'POST':
        dest_account = request.form['dest_account']
        amount = request.form['amount']
        data = {'dest_account': dest_account, 'amount': amount, 'account_id': account_id}
        response = requests.post(API + f'/api/transactions/', json=data, headers=headers)
        if response.status_code != 201:
            flash('Transaction Failed...')
            return redirect(url_for('main.transactions', account_id=account_id))
        flash('Transaction Success!', 'success')
        return redirect(url_for('main.transactions', account_id=account_id))
    
    response = requests.get(API + f'/api/accounts/{account_id}', headers=headers)
    account = response.json()
    return render_template('transactions.html', account=account)

@main.route('/support', methods=['GET', 'POST'])
def support():
    if request.method == 'POST':
        data = {
            'name': request.form['name'],
            'email': request.form['email'],
            'message': request.form['message']
        }
        response = requests.post(API + '/api/support/contact', json=data)
        answer = response.json()
        if response.status_code == 201:
            flash('Message sent successfully!', 'success')
        else:
            flash('Failed to send message!', 'danger')
    return render_template('support.html', answer=answer)
