"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
import datetime
#from models import User
from models import db, User
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

# import dependencies for password security
from bcrypt import gensalt
from flask_bcrypt import generate_password_hash, check_password_hash

app = Flask(__name__)
app.url_map.strict_slashes = False

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
jwt = JWTManager(app)



db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/register', methods=['POST'])
def handle_registration():

    data = request.json
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    #Check that the data is complete
    check_data = [username, email, password]
    if None in check_data:
        return jsonify({
                "msg": "Incomplete data"
            }), 400

    #Query of username and email to verify the uniqueness of both email and username
    username_query = User.query.filter_by(username=username).one_or_none()
    email_query = User.query.filter_by(email=email).one_or_none()

    if username_query:
        return jsonify({
                "msg": "Username already taken"
            }), 400
    
    if email_query:
        return jsonify({
                "msg": "email already registered"
            }), 400


    #Once the request has passed all the verifications 
    #we can proceed to generate the salt and hash the password
    salt = str(gensalt(), encoding="utf-8")
    password_hash = str(generate_password_hash(password + salt), encoding="utf-8")
    
    #Create the instance of the new user
    new_user = User(
        username = username,
        email = email.lower(),
        salt = salt,
        password_hash = password_hash,
    )

    #save in the database
    try:
        db.session.add(new_user)
        db.session.commit()
    except Exception as error:
        print(error)
        db.session.rollback()
        return jsonify({
            "msg": "An error has ocurred with the database"
        }), 500

    return jsonify({}), 201


#Route to generate the JWT and login the user
@app.route('/login', methods=['POST'])
def handle_login():
    
    data = request.json
    email = data.get("email").lower()
    password = data.get("password")

    #Check that the data is complete
    check_data = [email, password]
    if None in check_data:
        return jsonify({
            "msg": "Incomplete data"
        }), 400

    #check that the email exists in the database
    user = User.query.filter_by(email = email).one_or_none()
    if user is None:
        return jsonify({
            "msg": "Email does not exists in the database"
        }), 404

    #Check that the password is correct
    password_is_correct = check_password_hash(
        user.password_hash,
        password + user.salt
    )

    if not password_is_correct:
        return jsonify({
            "msg": "Incorrect password"
        }), 400

    #Create the JWT if the user has passed al the validations and return the token
    if password_is_correct:
        token = create_access_token(identity = user.id )
        return jsonify(token), 201

@app.route('/user', methods=['GET', 'PUT', 'DELETE'])
@jwt_required()
def handle_user():
    
    #check that the user exists
    user_id = get_jwt_identity()
    user = User.query.filter_by(id = user_id).one_or_none()
    if not user:
        return jsonify({
            "msg": "User not found"
        }), 404
    
    #GET method
    #Serialize the user and return the information
    if request.method == 'GET':
        return jsonify(user.serialize()), 200
    
    #PUT method
    #Modify the user information with the incoming data
    if request.method == 'PUT':
        data = request.json
        email = data.get("email")
        username = data.get("username")
        
        if data.get("email"):
            user.email = email.lower()
        
        if data.get("username"):
            user.username = username.lower()
        
        #save the modified data in the database 
        try:
            db.session.commit()
        except Exception as error:
            db.session.rollback()
            return jsonify({
                "msg": "An error has ocurred with the database"
            }), 500
        
        return jsonify({}), 200
    
    #DELETE method
    #Modify the user information with the incoming data
    if request.method == 'DELETE':
        try:
            db.session.delete(user)
            db.session.commit()
        except Exception as error:
            db.session.rollback()
            return jsonify({
                "msg": "An error has ocurred with the database"
            }), 500
        
        return jsonify({}), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
