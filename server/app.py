#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

# create a RESTful home page
class Home(Resource):

    def get(self):

        response_dict = {
            "message": "Welcome to the Plant RESTful API",
        }

        response = make_response(
            response_dict,
            200
        )

        return response

api.add_resource(Home, '/')

# Your API should have the following routes as well as the associated controller actions that return the appropriate JSON data:


class Plants(Resource):

    # Index Route
    # GET /plants
    # Response Body
    # -------
    # [
    #   {
    #     "id": 1,
    #     "name": "Aloe",
    #     "image": "./images/aloe.jpg",
    #     "price": 11.50
    #   },
    #   {
    #     "id": 2,
    #     "name": "ZZ Plant",
    #     "image": "./images/zz-plant.jpg",
    #     "price": 25.98
    #   }
    # ]
    def get(self):

        plants = [p.to_dict() for p in Plant.query.all()]

        return make_response(jsonify(plants), 200)
    

    # Create Route
    # POST /plants


    # Headers
    # -------
    # Content-Type: application/json


    # Request Body
    # ------
    # {
    # "name": "Aloe",
    # "image": "./images/aloe.jpg",
    # "price": 11.50
    # }


    # Response Body
    # -------
    # {
    # "id": 1,
    # "name": "Aloe",
    # "image": "./images/aloe.jpg",
    # "price": 11.50
    # }
    def post(self):
        data = request.get_json()

        new_plant = Plant(
            name=data['name'],
            image=data['image'],
            price=data['price'],
        )
        
        db.session.add(new_plant)
        db.session.commit()
        return make_response(new_plant.to_dict(), 201)
api.add_resource(Plants, '/plants')
# Show Route
# GET /plants/:id


# Response Body
# ------
# {
#   "id": 1,
#   "name": "Aloe",
#   "image": "./images/aloe.jpg",
#   "price": 11.50
# }
class PlantByID(Resource):
    def get(self, id):
        plant = Plant.query.filter_by(id=id).first().to_dict()
        return make_response(jsonify(plant), 200)
    
api.add_resource(PlantByID, '/plants/<int:id>')
    
        

if __name__ == '__main__':
    app.run(port=5555, debug=True)
