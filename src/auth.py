from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, create_access_token, create_refresh_token, get_jwt_identity
import validators 
from werkzeug.security import generate_password_hash, check_password_hash
from src.database import User, db

auth = Blueprint("auth", __name__ , url_prefix="/api/v1/auth")

@auth.post("/register")
@jwt_required()
def register():
    username = request.json.get('username')
    email = request.json.get('email')
    password = request.json.get('password')
    
    if len(username) < 4:
        return jsonify({"error": 
                        "username is too short, Try again!"}), 400
    if not username.isalnum() or " " in username:
        return jsonify({"error": 
                        "username should be alphanumeric and not contain whitespaces, Try again!"}), 400
    if len(password) < 6:
        return jsonify({"error": 
                        "password is too short, Try again!"}), 400

    if not validators.email(email):
        return jsonify({"error": 
                        "email is invalid, Try again!"}), 4000

    if User.query.filter_by(email=email).first() is not None:
        return jsonify({"error": 
                        "email is taken, Try again!"}), 409
    if User.query.filter_by(username=username).first() is not None:
        return jsonify({"error": 
                        "username is taken, Try again!"}), 409
    
    hashed_pwd = generate_password_hash(password)
    user = User(username=username, password=hashed_pwd, email=email )

    db.session.add(user)
    db.session.commit()

    return jsonify({
                        "message": "User created",
                        "user": {
                            "username": username,
                            "email": email}
                        }), 201


@auth.post("/login")
def login():
    email = request.json.get("email")
    password = request.json.get("password")

    user = User.query.filter_by(email=email).first()

    if user:
        pass_correct = check_password_hash(user.password, password)

        if pass_correct:
            refresh = create_refresh_token(identity=user.id)
            access = create_access_token(identity=user.id)

            return jsonify({
                'user' : {
                    'refresh' : refresh,
                    'access'  : access,
                    'username' : user.email,
                    'email' : user.email
                }, 
            }), 200
    return jsonify({
        'error' : "wrong credentials"
    }), 401

@auth.get("/me")
@jwt_required()
def me():
    user_id = get_jwt_identity()

    user = User.query.filter_by(id=user_id).first()
    
    return jsonify({
        "username": user.username,
        "email" : user.email
        }), 200

@auth.get("/token/refresh")
@jwt_required(refresh=True)
def refresh_user_token():
   id =  get_jwt_identity()
   access = create_access_token(identity=id)

   return jsonify({
       "access_token" : access
   }), 200