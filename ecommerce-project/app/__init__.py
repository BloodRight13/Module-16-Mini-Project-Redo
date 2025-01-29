from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint
import os

def create_app():
    app = Flask(__name__)

    #Swagger Configuration
    SWAGGER_URL = '/swagger'
    API_URL = '/static/swagger.json'

    SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "E-commerce API"
        }
    )
    app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)

    #Register routes from the routes module
    from app import routes
    routes.init_app(app)

    @app.route("/static/swagger.json")
    def swagger_static():
        return app.send_static_file("swagger.json")

    return app
