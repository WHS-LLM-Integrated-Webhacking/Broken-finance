from flask import Blueprint, request, jsonify
from auth.decorators import token_required
from .llmwebretriever import llm_web_retriever

support_bp = Blueprint('support', __name__)

@support_bp.route('/chatbot', methods=['POST'])
@token_required
def contact_support(current_user):
    data = request.get_json()
    name = current_user[1]
    message = data['message']
    # return jsonify({'response': llm_web_retriever(name, message)}), 201
    return jsonify(llm_web_retriever(name, message, current_user[0])), 201