from operator import methodcaller
import validators
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from src.database import Bookmark
from src.database import db

bookmarks = Blueprint("bookmarks", __name__ , url_prefix="/api/v1/bookmarks")


@bookmarks.route("/", methods=['POST', 'GET'])
@jwt_required()
def get_bookmarks():
    
    current_user = get_jwt_identity()

    if request.method == 'POST':
        body = request.get_json().get('body', "")
        url = request.get_json().get('url', "")
        

        if not validators.url(url):
            return jsonify({
                "error": "invalid url, try again!"
            }), 400
        
        if Bookmark.query.filter_by(url=url).first():
            return jsonify({
                "error" : "Url already exists."
            }), 409
        bookmark = Bookmark(url=url, body=body, user_id=current_user)
        db.session.add(bookmark)
        db.session.commit()

        return jsonify({
            "id": bookmark.id,
            "body": bookmark.body,
            "url": bookmark.url,
            "short_url": bookmark.short_url,
            "visits": bookmark.visits,
            "created_at": bookmark.created_at,
            "updated_at": bookmark.updated_at

        }), 201
    
    else:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('page', 1, type=int)

        bookmarks = Bookmark.query.filter_by(user_id=current_user).paginate(page=page, per_page=per_page)
        
        data = []

        for bookmark in bookmarks:
            data.append({
                "id": bookmark.id,
                "body": bookmark.body,
                "url": bookmark.url,
                "short_url": bookmark.short_url,
                "visits": bookmark.visits,
                "created_at": bookmark.created_at,
                "updated_at": bookmark.updated_at
            })

        return jsonify({
            "data": data
        }), 200
        