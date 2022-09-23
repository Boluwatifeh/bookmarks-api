from tabnanny import check
from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, create_refresh_token
from itsdangerous import json
from markupsafe import re
import validators
from werkzeug.security import generate_password_hash, check_password_hash
from src.database import User, db

auth = Blueprint("auth", __name__ , url_prefix="/api/v1/auth")

@auth.post("/register")
def register():
    username = request.json.get('username')
    email = request.json.get('email')
    password = request.json.get('password')
    
    if len(username) < 4:
        return jsonify({"error": 
                        "username is too short, Try again!"}), 400
    if not username.isalnum() or " " in username:
        return jsonify({"error": 
                        "username should be alphanumeric and not contain whitespaces ! Try again"}), 400
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
                }
            })
    return 

@auth.get("/me")
def me():
    return jsonify({"user": "me"})
