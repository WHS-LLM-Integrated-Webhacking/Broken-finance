
from flask import Flask, jsonify
from customers.routes import customers_bp
from accounts.routes import accounts_bp
from transactions.routes import transactions_bp
from auth.routes import auth_bp
from support.routes import support_bp
from db import init_db, close_db

import os

def create_app():
    app = Flask(__name__)

    # Configuration
    app.config['SECRET_KEY'] = os.urandom(8)  # Needed for JWT

    # Register Blueprints
    app.register_blueprint(customers_bp, url_prefix='/api/customers')
    app.register_blueprint(accounts_bp, url_prefix='/api/accounts')
    app.register_blueprint(transactions_bp, url_prefix='/api/transactions')
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(support_bp, url_prefix='/api/support')

    # Initialize the database
    with app.app_context():
        init_db()

    # Error Handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not found'}), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error'}), 500

    @app.teardown_appcontext
    def teardown_db(exception):
        close_db(exception)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)
