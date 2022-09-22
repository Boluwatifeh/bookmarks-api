from flask import Blueprint, jsonify, request
from markupsafe import re
import validators
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint("auth", __name__ , url_prefix="/api/v1/auth")

@auth.post("/register")
def register():
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']
    
    if len(username) < 4:
        return jsonify({"message": 
                        "username is too short! Try again"}), 400
    if len(password) < 6:
        return jsonify({"message": 
                        "password is too short! Try again"}), 400

    if not validators.email():
        return jsonify({"message": 
                        "email is invalid! Try again"}), 400
                        


@auth.get("/me")
def me():
    return jsonify({"user": "me"})