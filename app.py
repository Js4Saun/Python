# Author: JS4CRT 0707476
# Date: 21/12/2021
# Objective: Emerging technologies Project 2

# Import Flask class definition from Library
from flask import Flask, request, jsonify, make_response
# Import JSON module 
import json

# Import JWT module
import jwt

from functools import wraps

# Import the datetime module
import datetime

# SQLAlchemy library
from flask_sqlalchemy import SQLAlchemy

# Marshmallow library
from flask_marshmallow import Marshmallow

# from marshmallow_sqlalchemy.schema import SQLAlchemyAutoSchema 

# This is used to instantiate app based of Flask class
app = Flask(__name__)

# SQLAlchemy config

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db' # database path
app.config['SQLALCHEMY_ECHO'] = True # echoes SQL for debug
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'WeatherAPIKey'

# SQLAlchemy before Flask-Marshmallow
db= SQLAlchemy(app)

ma = Marshmallow(app)


############################################ DB CLASSES ######################

# Create class for Weather
class Weather(db.Model):
    """class definition of the weather model"""
    # line 45 is a doc string, use help() to view
    # Class fields and their data types in parenthesis
    weather_id = db.Column(db.Integer(), primary_key=True,
    autoincrement = True)
    weather_humidity = db.Column(db.Float(), nullable=False)
    weather_region = db.Column(db.String(80), nullable=False)
    weather_wind_speed = db.Column(db.Integer(), nullable=False)
    weather_wind_direction = db.Column(db.Integer(), nullable=False)
    weather_temp = db.Column(db.Integer(), nullable=False)
    weather_rain = db.Column(db.Integer(), nullable=False)
    weather_coords = db.Column(db.String(80), nullable=False)
    
    def __repr__(self):
        return '<weather %r>' % self.weather_id


# Create class for User
class User(db.Model):
    """class definition for user model"""
    # Class fields and their data types in parenthesis
    user_id = db.Column(db.Integer(), primary_key=True, autoincrement = True)
    user_name = db.Column(db.String(80), nullable=False)
    user_password = db.Column(db.String(80), nullable=False)
    user_email = db.Column(db.String(80), nullable=False)
    
    def __repr__(self):
        return '<user %r>' % self.user_id     


################################################### AUTHENTICATION ###########


# athentication function
@app.get('/login')
def login():
    """endpoint for authentication"""
    auth=request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('could not verify', 401, {'Authentication':
        'login required"'})
    
    # creates var called users and searches user class for username
    user = User.query.filter_by(user_name=auth.username).first()  
    if (user.user_password == auth.password):
        # creates a token at the current time interval that expires in 30 mins
        token = jwt.encode({'user_id' : user.user_id, 'exp' : 
        datetime.datetime.utcnow()
        + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'], "HS256")
 
        return jsonify({'token' : token})
 
    return make_response('could not verify',  401, {'Authentication':
    '"login required"'})           


############################################ SCHEMAS #########################


# class def for Marshmallow for user schema
class UserSchema(ma.SQLAlchemyAutoSchema):
    """Definition used by serialization library based on user model"""
    class Meta:
        fields = ("user_id", "user_name", "user_password", "user_email")
# class def for Marshmallow for weather schema
class WeatherSchema(ma.SQLAlchemyAutoSchema):
    """Def used by library based on weather model"""
    class Meta:
        fields = ("weather_id", "weather_humidity",
        "weather_region", "weather_wind_speed",
        "weather_wind_direction", "weather_temp",
        "weather_rain", "weather_coords")

# instanitate objs based on Marshmallow schemas
weather_schema = WeatherSchema()
weathers_schema = WeatherSchema(many=True)
user_schema = UserSchema()
users_schema = UserSchema(many=True)


#################################### TOKEN FUNCTION ##########################


#This function creates a custom python decorator with the code required to,
#create and validate tokens.   
def token(f):
    # decorator that finds the library called functools
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        # Here JWT is passed in the request header
        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']
        # A 401 is hit if the token is not passed 
        if not token:
            return jsonify({'message': 'a valid token is missing'}), 401

        try:
            # this decodes the payload and retrieves details stored
            data = jwt.decode(token, app.config['SECRET_KEY'], 
            algorithms=["HS256"])

        except:
            return jsonify({'message': 'token is invalid'}), 401  
        # return the current logged in users contex to the routes
        return f( *args, **kwargs)
    return decorator                    


# used to trigger function based on HTTP GET method sent to app
@app.get("/")
def Weather_app():
    return "Welcome to Weather app"


########################################### POST REQUESTS ####################


# used to add a new weather record to the db
@app.post("/weather/add-weather")
@token # this means that an authentication token is required to execute
def weather_add_json():
    """this uses json to add Weather record to DB"""
    json_data = request.get_json() # access json sent
    print(json.dumps(json_data, indent=4)) # for debugging use

    new_weather = Weather (
        weather_id = json_data['weather_id'],
        weather_humidity = json_data['weather_humidity'],
        weather_region = json_data['weather_region'],
        weather_wind_speed = json_data['weather_wind_speed'],
        weather_wind_direction = json_data['weather_wind_direction'],
        weather_temp = json_data['weather_temp'],
        weather_rain = json_data['weather_rain'],
        weather_coords = json_data['weather_coords']        
    )
    db.session.add(new_weather)
    db.session.commit()

    print("Weather record added:")
    print (json.dumps(json_data, indent=4))
    return weather_schema.jsonify(new_weather)


# used to add a new user record to the db
@app.post('/users/add-users')
@token
def users_add_json():
    """this uses json to add User record to DB"""
    json_data = request.get_json()
    print(json.dumps(json_data, indent =4))
    # if json_data['user_admin'] == "True":
    #     admin = True
    #     print("User is an admin")
    # else:
    #     admin = False
    #     print("User is not admin")

    new_user = User (
        user_id = json_data['user_id'],
        user_name = json_data['user_name'],
        user_password = json_data['user_password'],
        user_email = json_data['user_email']
        
    )
    db.session.add(new_user)
    db.session.commit()

    print("User record added:")
    print (json.dumps(json_data, indent=4))
    return user_schema.jsonify(new_user)


####################################### GET REQUESTS #########################


# used to return all user records from the db
@app.get('/users/')
@token
def users():
    res_users = User.query.all()
    return users_schema.jsonify(res_users)    

# used to return all weather records from the db
@app.get('/weathers/')
@token
def weathers():
    res_weathers = Weather.query.all()
    return weathers_schema.jsonify(res_weathers)


# used to return a weather record from the db via id
@app.get('/weathers/get-one-weather/<weather_id>')
@token
def get_one_weather_route(weather_id):
    """endpoint uses route parameters to determine weathers 
    to be queried from db"""
    weather = Weather.query.filter_by(weather_id=weather_id).first()
    if not weather:
        return{"message" : "Weather record not in database"}, 404
    return weather_schema.jsonify(weather)
    

# used to return a weather record from the db via region
@app.get('/weathers/get-all-weather-region/<weather_region>')
@token
def get_all_weather_region(weather_region):
    """endpoint uses route parameters to determine weathers 
    to be queried from db"""
    weather = Weather.query.filter_by(weather_region=weather_region).all()
    if not weather:
        return{"message" : "Weather record not in database"}, 404
    return weathers_schema.jsonify(weather)


# used to return a user record from the db via id
@app.get('/users/get-one-users/<user_id>')
@token
def get_one_user_route(user_id):
    """endpoint uses route parameters to determine 
    users to be queried from db"""
    user = User.query.filter_by(user_id=user_id).first()
    if not user:
        return{"message" : "User record not in database"}, 404
    return user_schema.jsonify(user)


# used to return a user record from the db via email
@app.get('/users/get-one-users-email/<user_email>')
@token
def get_one_user_email(user_email):
    """endpoint uses route parameters to determine 
    users to be queried from db"""
    user = User.query.filter_by(user_email=user_email).first()
    if not user:
        return{"message" : "user record not in database"}, 404
    return user_schema.jsonify(user)      


########################################### DELETE REQUESTS ##################


# used to delete a weather record from the db via id   
@app.delete('/weathers/delete-one-weather/<weather_id>')
@token
def delete_one_weather_route(weather_id):
    """function that deletes weather by id"""
    weather = Weather.query.filter_by(weather_id=weather_id)
    if not weather:
        return{"message" : "Weather record not in database"}, 404
    else:
        weather.delete()
        db.session.commit()  
        return {"Weather deleted" : f"weather_id: {weather_id}"}, 200


# used to remove a user record from the db via id
@app.delete('/users/delete-one-user/<user_id>')
@token
def delete_one_user_route(user_id):
    """function that deletes user by id"""
    user = User.query.filter_by(user_id=user_id)
    if not user:
        return{"message" : "user record not in database"}, 404
    else:    
        user.delete()
        db.session.commit()
        return {"User deleted" : f"user_id: {user_id}"}, 200


############################################ PUT REQUESTS ####################


# used to update a weather record from the db via id
@app.put("/weathers/update-weathers")
@token
def weathers_update_json():
    """function that updates all fields in existing weathers in db via id"""
    json_data = request.get_json()
    print(json.dumps(json_data, indent=4))

    weather = Weather.query.filter_by(weather_id=json_data['weather_id']).update(
        dict
        (
            weather_humidity = json_data['weather_humidity'],
            weather_region = json_data['weather_region'],
            weather_wind_speed = json_data['weather_wind_speed'],
            weather_wind_direction = json_data['weather_wind_direction'],
            weather_temp = json_data['weather_temp'],
            weather_rain = json_data['weather_rain'],
            weather_coords = json_data['weather_coords'] 
        )
    )
    if not weather:
        return{"message" : "Weather record not in database"}, 404
    else:    
        db.session.commit()
        return{"message": "weather updated"}, 200


# used to update a user record from the db via id
@app.put("/users/update-users")
@token
def users_update_json():
    """function that updates all fields for existing users in db via id"""
    json_data = request.get_json()
    print(json.dumps(json_data, indent=4))

    user = User.query.filter_by(user_id=json_data['user_id']).update(
        dict
        (
            user_name = json_data['user_name'],
            user_password = json_data['user_password'],
            user_email = json_data['user_email'] 
        )
    )
    if not user:
        return{"message" : "User record not in database"}, 404
    else: 
        db.session.commit()
        return{"message": "user updated"}, 200


############################################# PATCH REQUESTS FOR USER ########


# Patch requests update a specific field of a user object in db via id
# patch request to update username
@app.patch("/users/update-users-username")
@token
def users_update_username():
    """function that updates username of a user"""
    json_data = request.get_json()
    print(json.dumps(json_data, indent=4))

    User.query.filter_by(user_id=json_data['user_id']).update(
        dict
        (
            user_name = json_data['user_name']
        )
    )
    db.session.commit()
    return{"message": "account username updated"}, 200


# patch request to update password 
@app.patch("/users/update-users-password")
@token
def users_update_password():
    """function that updates perms of a user"""
    json_data = request.get_json()
    print(json.dumps(json_data, indent=4))

    User.query.filter_by(user_id=json_data['user_id']).update(
        dict
        (
            user_password = json_data['user_password']
        )
    )
    db.session.commit()
    return{"message": "account password updated"}, 200


######################################### PATCH REQUESTS FOR WEATHER #########


# patch request to update humidity 
@app.patch("/weathers/update-weather-humidity")
@token
def weathers_update_humidity():
    """function that updates humidity of a weather record"""
    json_data = request.get_json()
    print(json.dumps(json_data, indent=4))

    Weather.query.filter_by(weather_id=json_data['weather_id']).update(
        dict
        (
            weather_humidity = json_data['weather_humidity']
        )
    )
    db.session.commit()
    return{"message": "Humitidy level updated"}, 200


# patch request to update windspeed
@app.patch("/weathers/update-weather-windspeed")
@token
def weathers_update_windspeed():
    """function that updates windspeed of a weather record"""
    json_data = request.get_json()
    print(json.dumps(json_data, indent=4))

    Weather.query.filter_by(weather_id=json_data['weather_id']).update(
        dict
        (
            weather_wind_speed = json_data['weather_wind_speed']
        )
    )
    db.session.commit()
    return{"message": "Wind speed updated"}, 200


# patch request to update wind direction
@app.patch("/weathers/update-weather-wind-direction")
@token
def weathers_update_wind_direction():
    """function that updates wind direction of a weather record"""
    json_data = request.get_json()
    print(json.dumps(json_data, indent=4))

    Weather.query.filter_by(weather_id=json_data['weather_id']).update(
        dict
        (
            weather_wind_direction = json_data['weather_wind_direction']
        )
    )
    db.session.commit()
    return{"message": "Wind direction updated"}, 200


# patch request to update weather temp
@app.patch("/weathers/update-weather-temp")
@token
def weathers_update_temp():
    """function that updates temperature of a weather record"""
    json_data = request.get_json()
    print(json.dumps(json_data, indent=4))

    Weather.query.filter_by(weather_id=json_data['weather_id']).update(
        dict
        (
            weather_temp = json_data['weather_temp']
        )
    )
    db.session.commit()
    return{"message": "Weather temperature updated"}, 200


# patch request to update weather rain
@app.patch("/weathers/update-weather-percipitation")
@token
def weathers_update_rain():
    """function that updates percipitation of a weather record"""
    json_data = request.get_json()
    print(json.dumps(json_data, indent=4))

    Weather.query.filter_by(weather_id=json_data['weather_id']).update(
        dict
        (
            weather_rain = json_data['weather_rain']
        )
    )
    db.session.commit()
    return{"message": "Percipitation level updated"}, 200


################################################ PATCH ALL WEATHER ###########


# Alternative way to patch, these functions can pass all fields in one, 
# function rather than having multiple different ones 

# patch request to update weather
@app.patch("/weathers/update-weather-patch")
@token
def weathers_patch():
    """function that patches a weather record, can pass all fields"""
    json_data = request.get_json()
    print(json.dumps(json_data, indent=4))
    weather = Weather.query.filter_by(weather_id=json_data['weather_id']).first()
    print(weather)
    try:
        # patch condition for humidity
        if json_data ['weather_humidity']:
            weather.weather_humidity=json_data['weather_humidity']
            db.session.commit()
            return{"message": "Humidity level updated"}, 200
    except:
        try:
            # patch condition for wind speed
            if json_data ['weather_wind_speed']:
                weather.weather_wind_speed=json_data['weather_wind_speed']
                db.session.commit()
                return{"message": "Wind velocity updated"}, 200
        except:
            try:
                # patch condition for wind direction
                if json_data ['weather_wind_direction']:
                    weather.weather_wind_direction=json_data['weather_wind_direction']
                    db.session.commit()
                    return{"message": "Wind direction updated"}, 200
            except:
                try:
                    # patch condition for temperature
                    if json_data ['weather_temp']:
                        weather.weather_temp=json_data['weather_temp']
                        db.session.commit()
                        return{"message": "Temperature updated"}, 200
                except:
                    try:
                        # patch condition for percipitation
                        if json_data ['weather_rain']:
                            weather.weather_rain=json_data['weather_rain']
                            db.session.commit()
                            return{"message": "Percipitation level updated"}, 200
                    except:
                            # excecutes if request is invalid
                            return{"message": "invalid argument"}, 400


########################################## PATCH ALL USER ####################


# patch request to update user
@app.patch("/users/update-user-patch")
@token
def users_patch():
    """function that patches a users record, can pass all fields"""
    json_data = request.get_json()
    print(json.dumps(json_data, indent=4))
    user = User.query.filter_by(user_id=json_data['user_id']).first()
    print(user)
    try:
        # patch condition for username
        if json_data ['user_name']:
            user.user_name=json_data['user_name']
            db.session.commit()
            return{"message": "Username for user record updated"}, 200
    except:
        try:
            # patch condition for password
            if json_data ['user_password']:
                user.user_password=json_data['user_password']
                db.session.commit()
                return{"message": "Password for user record updated"}, 200
        except:
                # excecutes if request invalid
                return{"message": "invalid argument"}, 400   