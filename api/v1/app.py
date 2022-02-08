from os import getenv
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close(exception):
    storage.close()

@app.errorhandler(404)
def page_not_found(err):
    return jsonify({'error': 'Not found'}), 404

if __name__ == "__main__":
    apiHost = getenv("HBNB_API_HOST", default="0.0.0.0")
    apiPort = getenv("HBNB_API_PORT", default=5000)
    app.run(debug=True, host=apiHost, port=int(apiPort))
