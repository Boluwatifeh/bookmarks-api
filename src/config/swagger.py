template = {
    "openapi": "3.0.0",
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
      "servers": [
        {
          "url": "http://127.0.0.1:{port}",
          "description": "The production API server",
          "variables": {
            "port": {
              "enum": [
                "5000",
                "80"
              ],
              "default": "5000"
            },
            "basePath": {
              "default": "api/v1"
            }
          }
        }
      ],
    
    "schemes": [
        "https",
        "http"
    ],
    
    "components" : {
    "securitySchemes": {
        "bearerAuth": {
            "type" : "http",
            "scheme" : "bearer",
            "name" : "Authorization",
            "in" :  "header",
            "bearerFormat" : "JWT",
            "description" : "JWT Authorization header using the bearer scheme. Example : \"Authorization: Bearer {token}\""
                }
        }
    }
}


swagger_config = {
    "headers": [
    ],
    "specs": [
        {
            "endpoint": 'apispec_1',
            "route": '/apispec_1.json',
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],
    "static_url_path": "/flasgger_static",
    # "static_folder": "static",  # must be set by user
    "swagger_ui": True,
    "specs_route": "/"
}