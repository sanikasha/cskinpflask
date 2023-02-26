""" database dependencies to support sqliteDB examples """
from random import randrange
from datetime import date
import os, base64
import json

from __init__ import app, db
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash


''' Tutorial: https://www.sqlalchemy.org/library.html#tutorials, try to get into Python shell and follow along '''

# Define the Kost class to manage actions in 'kosts' table,  with a relationship to 'skintypes' table
# class Kost(db.Model):
#     __tablename__ = 'kosts'

#     # Define the Notes schema
#     id = db.Column(db.Integer, primary_key=True)
#     note = db.Column(db.Text, unique=False, nullable=False)
#     image = db.Column(db.String, unique=False)
#     # Define a relationship in Notes Schema to userID who originates the note, many-to-one (many notes to one user)
#     userID = db.Column(db.Integer, db.ForeignKey('skintypes.id')) 

#     # Constructor of a Notes object, initializes of instance variables within object
#     def __init__(self, id, note, image):
#         self.userID = id
#         self.note = note
#         self.image = image

#     # Returns a string representation of the Notes object, similar to java toString()
#     # returns string
#     def __repr__(self):
#         return "Notes(" + str(self.id) + "," + self.note + "," + str(self.userID) + ")"

#     # CRUD create, adds a new record to the Notes table
#     # returns the object added or None in case of an error
#     def create(self):
#         try:
#             # creates a Notes object from Notes(db.Model) class, passes initializers
#             db.session.add(self)  # add prepares to persist person object to Notes table
#             db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
#             return self
#         except IntegrityError:
#             db.session.remove()
#             return None

#     # CRUD read, returns dictionary representation of Notes object
#     # returns dictionary
#     def read(self):
#         # encode image
#         path = app.config['UPLOAD_FOLDER']
#         file = os.path.join(path, self.image)
#         file_text = open(file, 'rb')
#         file_read = file_text.read()
#         file_encode = base64.encodebytes(file_read)
        
#         return {
#             "id": self.id,
#             "userID": self.userID,
#             "note": self.note,
#             "image": self.image,
#             "base64": str(file_encode)
#         }


# Define the SkinType class to manage actions in the 'skintypes' table
# -- Object Relational Mapping (ORM) is the key concept of SQLAlchemy
# -- a.) db.Model is like an inner layer of the onion in ORM
# -- b.) SkinType represents data we want to store, something that is built on db.Model
# -- c.) SQLAlchemy ORM is layer on top of SQLAlchemy Core, then SQLAlchemy engine, SQL

#Create new class to save information in a table 
class SkinType(db.Model):
    __tablename__ = 'skintypes'  # table name is plural, class name is singular

    # Define the SkinType schema with "vars" from object
    id = db.Column(db.Integer, primary_key=True)
    _skin_type = db.Column(db.String(255), unique=False, nullable=False)
    _moisturizer = db.Column(db.String(255), unique=False, nullable=False)
    _face_cleanser = db.Column(db.String(255), unique=False, nullable=False)
    _serum = db.Column(db.String(255), unique=False, nullable=False)
    _sunscreen = db.Column(db.String(255), unique=False, nullable=False)

    # Defines a relationship between SkinType record and Notes table, one-to-many (one SkinType to many notes)
    #kosts = db.relationship("Kost", cascade='all, delete', backref='skintypes', lazy=True)

    # constructor of a SkinType object, initializes the instance variables within object (self)
    def __init__(self, skin_type, moisturizer, face_cleanser, serum, sunscreen):
        self._skin_type = skin_type    # variables with self prefix become part of the object, 
        self._moisturizer = moisturizer
        self._face_cleanser = face_cleanser
        self._serum = serum
        self._sunscreen = sunscreen

    # a skin type getter method, extracts skin type from object
    @property
    def skin_type(self):
        return self._skin_type
    
    # a setter function, allows skin type to be updated after initial object creation
    @skin_type.setter
    def skin_type(self, skin_type):
        self._skin_type = skin_type
    
    # check if skin_type parameter matches _skin_type in object, return boolean
    def is_skin_type(self, skin_type):
        return self._skin_type == skin_type

    # a getter method, extracts moisturizer from object
    @property
    def moisturizer(self):
        return self._moisturizer
    
    # a setter function, allows moisturizer to be updated after initial object creation
    @moisturizer.setter
    def moisturizer(self, moisturizer):
        self._moisturizer = moisturizer

    # a getter method, extracts face cleanser from object
    @property
    def face_cleanser(self):
        return self._face_cleanser
    
    # a setter function, allows face_cleanser to be updated after initial object creation
    @face_cleanser.setter
    def face_cleanser(self, face_cleanser):
        self._face_cleanser = face_cleanser
    
    # a getter method, extracts serum from object
    @property
    def serum(self):
        return self._serum
    
    # a setter function, allows serum to be updated after initial object creation
    @serum.setter
    def serum(self, serum):
        self._serum = serum

    # a getter method, extracts sunscreen from object
    @property
    def sunscreen(self):
        return self._sunscreen
    
    # a setter function, allows sunscreen to be updated after initial object creation
    @sunscreen.setter
    def sunscreen(self, sunscreen):
        self._sunscreen = sunscreen

    # output content using str(object) in human readable form, uses getter
    # output content using json dumps, this is ready for API response
    def __str__(self):
        return json.dumps(self.read())

    # CRUD create/add a new record to the table
    # returns self or None on error
    def create(self):
        try:
            # creates a person object from SkinType(db.Model) class, passes initializers
            db.session.add(self)  # add prepares to persist person object to skin_types table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        except IntegrityError:
            db.session.remove()
            return None

    # CRUD read converts self to dictionary
    # returns dictionary
    def read(self):
        return {
            "id": self.id,
            "skin_type": self._skin_type,
            "moisturizer": self._moisturizer,
            "face_cleanser": self._face_cleanser,
            "serum": self._serum,
            "sunscreen": self._sunscreen,
            #"kosts": [kost.read() for kost in self.kosts]
        }

    # CRUD update: updates skin_type and matching skin products
    # returns self
    def update(self, skin_type="", moisturizer="", face_cleanser="", serum="", sunscreen=""):
        """only updates values with length"""
        if len(skin_type) > 0:
            self._skin_type = skin_type
        if len(moisturizer) > 0:
            self._moisturizer = moisturizer
        if len(face_cleanser) > 0:
            self._face_cleanser = face_cleanser
        if len(serum) > 0:
            self._serum = serum
        if len(sunscreen) > 0:
            self._sunscreen = sunscreen
        db.session.commit()
        return self

    # CRUD delete: remove self
    # None
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None


"""Database Creation and Testing """


# Builds working data for testing
def initSkinTypes():
    with app.app_context():
        """Create database and tables"""
        db.create_all()
        """Tester data for table"""
        st1 = SkinType(skin_type='oily',      moisturizer='SkinCeuticals Daily Moisture',           face_cleanser='CeraVe Acne Foaming Cream Cleanser',                               serum='The Ordinary Niacinamide 10% + Zinc 1% Serum', sunscreen='Regaliz Truderma Sunscreen Gel SPF 50')
        st2 = SkinType(skin_type='dry',       moisturizer='Neutrogena Hydro Boost Gel Moisturizer', face_cleanser='Paula\'s Choice Perfectly Balanced Foaming Cleanser',              serum='Simple Booster Serum - 3% Hyaluronic Acid',    sunscreen='Laneige Watery Sun Cream')
        st3 = SkinType(skin_type='sensitive', moisturizer='Plum Hello Aloe Caring Day Moisturizer', face_cleanser='Bioderma Sensibio Gentle Soothing Micellar Cleansing Foaming Gel', serum='Simple Booster Serum - 10% Niacinamide',       sunscreen='Elta MD Skin Care UV Glow SPF 36')
        st4 = SkinType(skin_type='normal',    moisturizer='Good Vibes Gel Moisturizer',             face_cleanser='La Roche-Posay Toleriane Hydrating Gentle Cleanser',               serum='Jovees Herbal Vitamin C Face Serum',           sunscreen='Cetaphil Daily Oil Free Facial Moisturizer with SPF 35')

        skintypes = [st1, st2, st3, st4]

        """Builds sample skin type/note(s) data"""
        for skintype in skintypes:
            try:
                '''add a few 1 to 4 notes per skin type'''
                for num in range(randrange(1, 4)):
                    note = "#### " + skintype.skin_type + " note " + str(num) + ". \n Generated by test data."
                    #skintype.kosts.append(Kost(id=skintype.id, note=note, image='ncs_logo.png'))
                    #'''add skin type/kost data to table'''
                    skintype.create()
            except IntegrityError:
                '''fails with bad or duplicate data'''
                db.session.remove()
                print(f"Records exist, duplicate email, or error: {skintype.skin_type}")
            