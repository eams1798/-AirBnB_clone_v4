from os import getenv
from flask import Flask
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close(exception):
    storage.close()


if __name__ == "__main__":
    apiHost = getenv("HBNB_API_HOST", default="0.0.0.0")
    apiPort = getenv("HBNB_API_PORT", default=5000)
    app.run(host=apiHost, port=int(apiPort))
