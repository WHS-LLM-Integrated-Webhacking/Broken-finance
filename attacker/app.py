from flask import Flask, request, redirect
from flask_headers import *
app = Flask(__name__)

@app.route('/')
def index():
    url = request.args.get('url', 'http://127.0.0.1/api/customers/get')
    access_token = request.headers.get('x-access-token')
    
    if not access_token: return {"response": "Access token is missing!"}, 400
    
    response = redirect(url)
    response.headers['x-access-token'] = access_token
    return response

if __name__ == '__main__':
    app.run(debug=True, port=1337, host="0.0.0.0")
