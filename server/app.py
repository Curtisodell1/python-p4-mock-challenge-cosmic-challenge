#!/usr/bin/env python3

from models import db, Scientist, Mission, Planet
from flask_restful import Api, Resource
from flask_migrate import Migrate
from flask import Flask, make_response, jsonify, request
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)


@app.route('/')
def home():
    return ''

@app.route('/scientists', methods=["GET", "POST"])
def scientists():
    if request.method == "GET":
        all_scientists = [scientist.to_dict(rules = ("-missions",)) for scientist in Scientist.query.all()]
        return make_response(all_scientists, 200)
    elif request.method == "POST":
        try:
            data = request.get_json()
            new_scientist = Scientist(
                name = data["name"],
                field_of_study = data["field_of_study"]
            )
            db.session.add(new_scientist)
            db.session.commit()
            return make_response(new_scientist.to_dict(), 201)
        except ValueError:
            return make_response({"errors": ["validation errors"]}, 400)

        
        #get info they are giving us
        #create object with the information 
        #return this info 



    
    
    #what is it asking for - all scientists 
    #what is the return value - JSON Formatted
    #how does it need to be packaged  - response 



@app.route("/scientists/<int:id>", methods=["GET"])
def get_scientist_by_id(id):
    scientist_by_id = Scientist.query.filter(Scientist.id == id).first()
    if scientist_by_id is None:
        return make_response({'error': 'Scientist not found'}, 404)
    else:
        return make_response(scientist_by_id.to_dict(rules = ("-field_of_study", "-missions.planets")), 200)
    


if __name__ == '__main__':
    app.run(port=5555, debug=True)
