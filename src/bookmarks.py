import validators
from http import HTTPStatus
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
            }), HTTPStatus.BAD_REQUEST
        
        if Bookmark.query.filter_by(url=url).first():
            return jsonify({
                "error" : "Url already exists."
            }), HTTPStatus.CONFLICT
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

        }), HTTPStatus.CREATED
    
    else:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)

        bookmarks = Bookmark.query.filter_by(user_id=current_user).paginate(page=page, per_page=per_page)
        data = []

        for bookmark in bookmarks.items:
            data.append({
                "id": bookmark.id,
                "body": bookmark.body,
                "url": bookmark.url,
                "short_url": bookmark.short_url,
                "visits": bookmark.visits,
                "created_at": bookmark.created_at,
                "updated_at": bookmark.updated_at
            })
        
        metadata = {
            "page": bookmarks.page,
            "pages": bookmarks.pages,
            "total_count" : bookmarks.total,
            "next_page" : bookmarks.next_num,
            "prev_page" : bookmarks.prev_num,
            "has_next" : bookmarks.has_next,
            "has_prev" : bookmarks.has_prev,
        }

        return jsonify({
            "data": data,
             "meta" : metadata
        }), HTTPStatus.OK
        

@bookmarks.route("/<int:id>")
@jwt_required()
def get_bookmark(id):
    current_user = get_jwt_identity()

    bookmark = Bookmark.query.filter_by(user_id=current_user, id=id).first()

    if not bookmark:
        return jsonify({
            "error" : "data not found"
        }), HTTPStatus.NOT_FOUND

    return jsonify({
                "id": bookmark.id,
                "body": bookmark.body,
                "url": bookmark.url,
                "short_url": bookmark.short_url,
                "visits": bookmark.visits,
                "created_at": bookmark.created_at,
                "updated_at": bookmark.updated_at
            }), HTTPStatus.OK

@bookmarks.put("/<int:id>")
@bookmarks.patch("/<int:id>")
@jwt_required()
def edit_bookmark(id):
    current_user = get_jwt_identity()

    bookmark = Bookmark.query.filter_by(user_id=current_user, id=id).first()

    if not bookmark:
        return jsonify({
            "error" : "data not found"
        }), HTTPStatus.NOT_FOUND
    body = request.get_json().get('body', "")
    url = request.get_json().get('url', "")

    if not validators.url(url):
            return jsonify({
                "error": "invalid url, try again!"
            }), HTTPStatus.BAD_REQUEST
    
    bookmark.body = body
    bookmark.url = url

    db.session.commit()

    return jsonify({
                "id": bookmark.id,
                "body": bookmark.body,
                "url": bookmark.url,
                "short_url": bookmark.short_url,
                "visits": bookmark.visits,
                "created_at": bookmark.created_at,
                "updated_at": bookmark.updated_at
            }), HTTPStatus.OK

    
@bookmarks.delete("/<int:id>")
@jwt_required()
def delete_bookmark(id):
    current_user = get_jwt_identity()

    bookmark = Bookmark.query.filter_by(user_id=current_user, id=id).first()

    if not bookmark:
        return jsonify({
            "error" : "data not found"
        }), HTTPStatus.NOT_FOUND

    db.session.delete(bookmark)
    db.session.commit()

    return jsonify({}), HTTPStatus.NO_CONTENT


@bookmarks.get("/stats")
@jwt_required()
def get_stats():
    current_user = get_jwt_identity()

    data = []

    bookmarks = Bookmark.query.filter_by(user_id=current_user).all()

    for bookmark in bookmarks:
        new_data = {
            "id": bookmark.id,
            "visits": bookmark.visits,
            "url" : bookmark.url,
            "short_url" : bookmark.short_url
        }
    
        data.append(new_data)
    
    return jsonify({"data": data}), HTTPStatus.OK