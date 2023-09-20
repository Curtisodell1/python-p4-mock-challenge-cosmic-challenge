from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata)


class Planet(db.Model, SerializerMixin):
    __tablename__ = 'planets'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    distance_from_earth = db.Column(db.Integer)
    nearest_star = db.Column(db.String)
    # Add relationship
    missions = db.relationship("Mission", backref="planets", cascade="all, delete-orphan")
    # Add serialization rules
    serialize_rules = ("-missions.planets",)

class Scientist(db.Model, SerializerMixin):
    __tablename__ = 'scientists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    field_of_study = db.Column(db.String)
    # Add relationship
    missions = db.relationship("Mission", backref="scientists", cascade="all, delete-orphan")
    # Add serialization rules
    serialize_rules = ("-missions.scientists",)
    # Add validation
    @validates("name", "field_of_study")
    def validate_name(self, key, prop):
        if key == "name":
            if not prop or len(prop) < 1:
                raise ValueError("must have a prop")
        if key == "field_of_study":
            if not prop or len(prop) < 1:
                raise ValueError("must have a prop")
        return prop
    
    validation_errors = []

    def to_scientist_dict(self):
        scientist = {
            "id": self.id,
            "name": self.name,
            "field_of_study": self.field_of_study,
            "missions": [mission.to_dict() for mission in Mission.query.filter(self.id == Mission.scientist_id)]
            }
        return scientist
    
    
        # missions will be an array with each mission entry as a dict entry
        # we'll use scientist id that matches within missions to return a list of missions for that scientist



class Mission(db.Model, SerializerMixin):
    __tablename__ = 'missions'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    # Add relationships
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'))
    scientist_id = db.Column(db.Integer, db.ForeignKey('scientists.id'))
    # Add serialization rules
    serialize_rules = ("-scientists.missions", "-planets.missions")
    # mission is the joiner model. Recursive loop happens on joiner model
    # mission joins a scientist and a planet. 
    # Whenever we have a has many model the serialize_rule is going to be the joiner and self
    # Add validation
    @validates("name", "scientist_id", "planet_id")
    def validate_name(self, key, prop):
        if key == "name":
            if not prop or len(prop) < 1:
                raise ValueError("must have a name")
        if key == "scientist_id":
            if not prop:
                raise ValueError("must have a scientist id")
        if key == "planet_id":
            if not prop:
                raise ValueError("must have a planet id")
        return prop


# add any models you may need.
