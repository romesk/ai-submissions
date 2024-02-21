
import datetime
from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, db

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password, password):
        access_token = create_access_token(identity=user.id, expires_delta=datetime.timedelta(days=1))
        return jsonify(message='Successfully logged in.', access_token=access_token), 200
    else:
        return jsonify({'message': 'Invalid username or password'}), 401

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    fullname = data.get('fullname')

    if not username or not password or not fullname:
        return jsonify({'message': 'Missing username, password, or fullname'}), 400

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({'message': 'Username already exists'}), 409

    hashed_password = generate_password_hash(password)
    new_user = User(username=username, fullname=fullname, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User created successfully'}), 201