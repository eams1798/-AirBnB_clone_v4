#!/usr/bin/python3
"""This module controlls all the api resources"""
from os import getenv
from flask import Flask, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
from flasgger import Swagger
from flasgger.utils import swag_from

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.register_blueprint(app_views)

cors = CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

app.config['SWAGGER'] = {
    'title': 'AirBnB clone Restful API',
    'uiversion': 3
}
Swagger(app)

@app.teardown_appcontext
def close(exception):
    """Close and reload storage"""
    storage.close()


@app.errorhandler(404)
def page_not_found(err):
    """ 404 Error
    ---
    responses:
      404:
        description: a resource was not found
    """
    return jsonify({'error': 'Not found'}), 404


if __name__ == "__main__":
    apiHost = getenv("HBNB_API_HOST", default="0.0.0.0")
    apiPort = getenv("HBNB_API_PORT", default=5000)
    app.run(debug=True, host=apiHost, port=int(apiPort), threaded=True)
