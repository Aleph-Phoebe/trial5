from flask import Blueprint, request, jsonify # type: ignore
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity # type: ignore
from .models import db, User, Remedy, Review
from flask_bcrypt import generate_password_hash, check_password_hash # type: ignore

main = Blueprint('main', __name__)

@main.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password']).decode('utf-8')
    new_user = User(username=data['username'], email=data['email'], password=hashed_password)

    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created successfully"}), 201

@main.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()

    if user and check_password_hash(user.password, data['password']):
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200

    return jsonify({"message": "Invalid credentials"}), 401

@main.route('/remedies', methods=['GET'])
def get_remedies():
    remedies = Remedy.query.all()
    return jsonify([{"id": r.id, "name": r.name, "advantages": r.advantages, "image": r.image} for r in remedies]), 200

@main.route('/reviews', methods=['POST'])
@jwt_required()
def add_review():
    data = request.get_json()
    user_id = get_jwt_identity()
    new_review = Review(user_id=user_id, remedy_id=data['remedy_id'], rating=data['rating'], comment=data.get('comment'))

    db.session.add(new_review)
    db.session.commit()
    return jsonify({"message": "Review added successfully"}), 201

@main.route('/favorites', methods=['POST'])
@jwt_required()
def add_favorite():
    user_id = get_jwt_identity()
    remedy_id = request.json.get('remedy_id')
    # Logic to add to favorites
    return jsonify({"message": "Favorite added successfully"}), 201
