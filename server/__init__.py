import os, traceback

from flask               import Flask, make_response, jsonify
from flask_sqlalchemy    import SQLAlchemy
from flask_login         import LoginManager
from flask_bcrypt        import Bcrypt
from jsonschema          import ValidationError
from werkzeug.exceptions import HTTPException

# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config.from_object('server.config.Config')

db = SQLAlchemy  (app) # flask-sqlalchemy
bc = Bcrypt      (app) # flask-bcrypt

lm = LoginManager() # flask-loginmanager
lm.init_app(app)    # init the login manager

# Import routing, models and Start the App
from server import fixIndexHTML, routes, models, seed

@app.errorhandler(400)
def bad_request(error):
    if isinstance(error.description, ValidationError):
        original_error = error.description
        return make_response(jsonify({ 'error': original_error.message }), 400)
    return make_response(jsonify({ 'error': str(error) }), 400)

@app.errorhandler(Exception)
def handle_error(e):
    code = 500
    if isinstance(e, HTTPException):
        code = e.code
    return jsonify({ 'error': str(e), 'stack': traceback.format_exc().split("\n") }), code

db.create_all()
fixIndexHTML.fixIndexHTMLdoc()
