# ==============================================================================
# @Name: myapp
# @Description: Creating a REST API with python.  Postman or any API testing
# tool is required.
# ==============================================================================

# import
import os
from flask import Flask
from flask_restful import Api, Resource, reqparse
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)
api = Api(app)
# Importing “Flask” , “Api” and “Resource” with capital letter initials,
# it signifies that a class is being imported. reqparse is Flask-RESTful request
# parsing interface which will be used later on. Then creating an app using
# “Flask” class, “__name__” is a Python special variable which gives Python file
# a unique name, in this case, telling the app to run in this specific place.

# ==============================================================================
# swagger specific:
# In the below code, a URI is created at the /swagger endpoint, and it returns a
# file called /swagger.json which will be parsed inside a self hosted Swagger-UI
# front end.
# ==============================================================================
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "My-Python-Flask-API-App"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)

# ==============================================================================
# This method is used for testing and is focusing on creating an API, but in
# actual condition, the data store is usually a database.
# ==============================================================================
users = [
    {
        "name" : "Luke Skywalker",
        "profession" : "Master Jedi",
        "quote" : "I Am A Jedi, Like My Father Before Me."
    },
    {
        "name" : "Tony Stark",
        "profession" : "Ironman",
        "quote" : "I am Ironman"
    },
    {
        "name" : "Jon Snow",
        "profession" : "Lord Commander",
        "quote" : "Winter is coming"
    }
]
# ==============================================================================
# One of the good qualities of a REST API is that it follows standard HTTP
# method to indicate the intended action to be performed.
# ==============================================================================
class User(Resource):

# The get method is used to retrieve a particular user details by specifying the
# name:
    def get(self, name):
        for user in users:
            if(name == user["name"]):
                return user, 200
        return "User not found", 400
# Traverse through the users list to search for the user, if the name
# specified matched with one of the user in users list, it wo;; return the user,
# along with 200 OK, else return a user not found message with 404 Not Found.
# Another characteristic of a well designed REST API is that it uses standard
# HTTP response status code to indicate whether a request is being processed
# successfully or not.

# The post method is used to create a new user:
    def post(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument("profession")
        parser.add_argument("quote")
        args = parser.parse_args()

        for user in users:
            if(name == user["name"]):
                return "User with name {} already exists".formate(name), 400

        user = {
            "name": name,
            "profession": args["profession"],
            "quote": args["quote"]
        }
        users.append(user)
        return user, 201
# Create a parser by using reqparse we imported earlier, add the age and
# occupation arguments to the parser, then store the parsed arguments in a
# variable, args (the arguments will come from request body in the form of
# form-data, JSON or XML). If a user with same name already exists, the API will
# return a message along with 400 Bad Request, else we will create the user by
# appending it to users list and return the user along with 201 Created.

# The put method is used to update details of user, or create a new one if it is
# not existed yet.
    def put(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument("profession")
        parser.add_argument("quote")
        args = parser.parse_args()

        for user in users:
            if(name == user["name"]):
                user["profession"]= args["profession"]
                user["quote"]= args["quote"]
                return user, 200

        user = {
            "name": name,
            "profession": args["profession"],
            "quote": quote["quote"]
        }
        users.append(user)
        return user, 201
# If the user already exist, it will update the details with the parsed
# arguments and return the user along with 200 OK, else it create &
# return the user along with 201 Created.

# The delete method is used to delete user that is no longer relevant:
    def delete(self, name):
        global users
        users = [user for user in users if user["name"] != name]
        return "{} is deleted.".format(name), 200
# By specifying users as a variable in global scope, we update the users
# list using list comprehension to create a list without the name specified
# (simulating delete), then return a message along with 200 OK.

# ==============================================================================
# Main()
# Add the resource to the API and specify its route, then run the Flask
# application:
# ==============================================================================
if __name__ == "__main__":
    api.add_resource(User, "/user/<string:name>")
    port = int(os.getenv("PORT", 8080))
    app.run(debug=True, port=port)
