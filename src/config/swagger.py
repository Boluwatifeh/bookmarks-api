template = {
    "swagger": "3.0",
    "info": {
        "title" : "Bookmarks API",
        "description" : "An Api for Bookmarks",
        "contact" : {
            "name": "Bookmarks API Support",
            "url": "http://www.twitter.com/tife_easypeasy",
            "email": "tifeasypeasy@gmail.com"
        }, 
        "license" : {
                "name": "Apache 2.0",
                "url": "https://www.apache.org/licenses/LICENSE-2.0.html"
        }, 
        "version" : "1.0"
    },
    "basePath": "/api/v1",
    "schemes": [
        "https",
        "http"
    ],
 
    "securitySchemes": {
        "bearerAuth": {
            "type" : "http",
            "scheme" : "bearer",
            "name" : "Authorization",
            "bearerFormat" : "JWT"
                }
        }
    }


swagger_config = {
    "headers": [
    ],
    "specs": [
        {
            "endpoint": 'apispec',
            "route": '/apispec.json',
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],
    "static_url_path": "/flasgger_static",
    # "static_folder": "static",  # must be set by user
    "swagger_ui": True,
    "specs_route": "/"
}