from flask import Flask, jsonify, redirect
import os
from src.auth import auth
from src.bookmarks import bookmarks
from src.database import Bookmark, db
from flask_jwt_extended import JWTManager

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:

        app.config.from_mapping(
            SECRET_KEY=os.environ.get("SECRET_KEY"),
            SQLALCHEMY_DATABASE_URI=os.environ.get('SQLALCHEMY_DATABASE_URI'),
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            JWT_SECRET_KEY=os.environ.get('JWT_SECRET_KEY')
        ) 
    
    else:
        app.config.from_mapping(test_config)

    db.app = app 
    db.init_app(app)
    #db.create_all()
    JWTManager(app)

    app.register_blueprint(auth)
    app.register_blueprint(bookmarks)
    
    @app.route("/")
    def index():
        return jsonify({"message": "Hello World"})

    @app.get("/<short_url>")
    def redirect_url(short_url):
        bookmark = Bookmark.query.filter_by(short_url=short_url).first_or_404()

        if bookmark: 
            bookmark.visits = bookmark.visits+1
            db.session.commit()
            print(bookmark.url)
            return redirect(bookmark.url)

    @app.errorhandler(404)
    def page_not_found(error):
        return jsonify({
            "error" : "Page not found"
        })


    
    return app 