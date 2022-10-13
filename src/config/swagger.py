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
    "components": {
        
        "securitySchemes": {
            "bearerAuth": {
                "type" : "http",
                "scheme" : "bearer",
                "name" : "Authorization",
                "in"   : "header",
                "bearerFormat" : "JWT"
                  }

             }

    }

}