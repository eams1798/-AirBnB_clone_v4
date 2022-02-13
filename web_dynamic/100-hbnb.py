#!/usr/bin/python3
"""12. HBNB is alive!"""


from flask import Flask, render_template
from models import storage
from markupsafe import escape
from datetime import datetime
import uuid
from os import getenv

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.teardown_appcontext
def close(exception):
    """closes the current session"""
    storage.close()


@app.route("/")
@app.route("/100-hbnb")
def hbnb():
    """Shows a styled page showing all required objects"""
    return render_template("100-hbnb.html",
                           states=storage.all('State'),
                           amenities=storage.all('Amenity'),
                           places=storage.all('Place'),
                           users=storage.all('User'),
                           cache_id=uuid.uuid4())

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
