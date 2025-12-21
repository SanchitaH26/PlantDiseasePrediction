from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
import bcrypt


app = Flask(__name__)
CORS(app)


# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client.plant_app
users = db.users


# -------- REGISTER USER --------
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    role = data.get('role') # farmer / admin


    if not username or not password or role not in ['farmer', 'admin']:
        return jsonify({'error': 'Invalid input'}), 400


    if users.find_one({'username': username}):
        return jsonify({'error': 'User already exists'}), 400


# SHA‑256‑level hashing with salt
    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


    users.insert_one({
        'username': username,
        'password': hashed_pw,
        'role': role
    })


    return jsonify({'message': 'User registered successfully'})




# -------- LOGIN USER --------
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')


    user = users.find_one({'username': username})
    if not user:
        return jsonify({'error': 'Invalid credentials'}), 401


    if not bcrypt.checkpw(password.encode('utf-8'), user['password']):
        return jsonify({'error': 'Invalid credentials'}), 401


    return jsonify({
        'message': 'Login successful',
        'role': user['role']
    })




if __name__ == '__main__':
    app.run(port=5001, debug=True)