from flask import Blueprint, request, jsonify

support_bp = Blueprint('support', __name__)

@support_bp.route('/contact', methods=['POST'])
def contact_support():
    # Dummy response for contact support
    data = request.get_json()
    
    return jsonify({'message': 'Your inquiry has been received. Our support team will contact you soon.'}), 201