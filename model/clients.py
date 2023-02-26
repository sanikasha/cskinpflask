""" database dependencies to support sqliteDB examples """
from random import randrange
from datetime import date
import os, base64
import json

from __init__ import app, db
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash

''' Tutorial: https://www.sqlalchemy.org/library.html#tutorials, try to get into Python shell and follow along '''

# Define the Post class to manage actions in 'posts' table,  with a relationship to 'users' table
class Tost(db.Model):
    __tablename__ = 'tosts'

    # Define the Notes schema
    id = db.Column(db.Integer, primary_key=True)
    note = db.Column(db.Text, unique=False, nullable=False)
    image = db.Column(db.String, unique=False)
    # Define a relationship in Notes Schema to userID who originates the note, many-to-one (many notes to one user)
    userID = db.Column(db.Integer, db.ForeignKey('clients.id'))

    # Constructor of a Notes object, initializes of instance variables within object
    def __init__(self, id, note, image):
        self.userID = id
        self.note = note
        self.image = image

    # Returns a string representation of the Notes object, similar to java toString()
    # returns string
    def __repr__(self):
        return "Notes(" + str(self.id) + "," + self.note + "," + str(self.userID) + ")"

    # CRUD create, adds a new record to the Notes table
    # returns the object added or None in case of an error
    def create(self):
        try:
            # creates a Notes object from Notes(db.Model) class, passes initializers
            db.session.add(self)  # add prepares to persist person object to Notes table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        except IntegrityError:
            db.session.remove()
            return None

    # CRUD read, returns dictionary representation of Notes object
    # returns dictionary
    def read(self):
        # encode image
        path = app.config['UPLOAD_FOLDER']
        file = os.path.join(path, self.image)
        file_text = open(file, 'rb')
        file_read = file_text.read()
        file_encode = base64.encodebytes(file_read)
        
        return {
            "id": self.id,
            "userID": self.userID,
            "note": self.note,
            "image": self.image,
            "base64": str(file_encode)
        }

# Define the User class to manage actions in the 'users' table
# -- Object Relational Mapping (ORM) is the key concept of SQLAlchemy
# -- a.) db.Model is like an inner layer of the onion in ORM
# -- b.) User represents data we want to store, something that is built on db.Model
# -- c.) SQLAlchemy ORM is layer on top of SQLAlchemy Core, then SQLAlchemy engine, SQL
class Client(db.Model):
    __tablename__ = 'clients'  # table name is plural, class name is singular

    # Define the User schema with "vars" from object
    id = db.Column(db.Integer, primary_key=True)
    _product = db.Column(db.String(255), unique=False, nullable=False)
    _ingredients = db.Column(db.String(255), unique=False, nullable=False)
    _skinType = db.Column(db.String(255), unique=False, nullable=False)
    _date = db.Column(db.String(255), unique=False, nullable=False)

    # Defines a relationship between User record and Notes table, one-to-many (one user to many notes)
    tosts = db.relationship("Tost", cascade='all, delete', backref='clients', lazy=True)

    def __init__(self, product, ingredients, date, skinType):
        self._product = product    # variables with self prefix become part of the object, 
        self._ingredients = ingredients
        self._date = date
        self._skinType = skinType


    # a name getter method, extracts name from object
    @property
    def product(self):
        return self._product
    
    # a setter function, allows name to be updated after initial object creation
    @product.setter
    def product(self, product):
        self._product = product

        # a getter method, extracts email from object
    @property
    def ingredients(self):
        return self._ingredients
    
    # a setter function, allows name to be updated after initial object creation
    @ingredients.setter
    def ingredients(self, ingredients):
        self._ingredients = ingredients

            # a getter method, extracts email from object
    @property
    def skinType(self):
        return self._skinType
    
    # a setter function, allows name to be updated after initial object creation
    @skinType.setter
    def skinType(self, skinType):
        self._skinType = skinType

    # a getter method, extracts email from object
    @property
    def date(self):
        return self._date
    
    # a setter function, allows name to be updated after initial object creation
    @date.setter
    def date(self, date):
        self._date = date
    
    # output content using str(object) in human readable form, uses getter
    # output content using json dumps, this is ready for API response
    def __str__(self):
        return json.dumps(self.read())

    # CRUD create/add a new record to the table
    # returns self or None on error
    def create(self):
        try:
            # creates a person object from User(db.Model) class, passes initializers
            db.session.add(self)  # add prepares to persist person object to Users table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        except IntegrityError:
            db.session.remove()
            return None

    # CRUD read converts self to dictionary
    # returns dictionary
    def read(self):
        return {
            "product": self._product,
            "ingredients": self._ingredients,
            "date": self._date,
            "skinType": self._skinType,
            "tosts": [tost.read() for tost in self.tosts],
        }

    # CRUD update: updates user name, password, phone
    # returns self
    def update(self, product=""):
        """only updates values with length"""
        if len(product) > 0:
            self.product = product
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
def initClients():
    """Create database and tables"""
    #db.create_all()
    """Tester data for table"""
    u1 = Client(product='Cetaphil Gentle Skin Cleanser', skinType='dry', ingredients='Water, Glycerin, Cocamidopropyl Betaine, Disodium Laureth Sulfosuccinate, Sodium Cocoamphoacetate, Panthenol, Niacinamide, Pantolactone, Acrylates/C10-30 Alkyl Acrylate Crosspolymer, Sodium Benzoate, Masking Fragrance, Sodium Chloride, Citric Acid', date='2023')
    u2 = Client(product='Alaffia Everyday Coconut Face Toner', skinType='dry', ingredients='Azadirachta indica (neem) leaf aqueous extract, Carica Papaya (Papaya) Leaf Aqueous Extract, Cocos Nucifera (Coconut) Water, Glycerin, Lavandula Hybrida (Lavender) Oil, Phenoxyethanol, Potassium Sorbate, Ascorbic Acid, Cocos Nucifera (Coconut) Extract', date='2023')
    u3 = Client(product='Laurel Skin Deep Clarity Oil Cleanser', skinType='combination', ingredients='Safflower Seed Oil, Sunflower Seed Oil, Sesame Seed Oil, Tamanu Oil, Black Cumin Seed Oil, Whole Plant Extracts of Rosemary, Calendula, Turmeric, Essential Oils of Green Mandarin, Ylang Ylang, Neroli, Rosemary', date='2023')
    u4 = Client(product='Glow Recipe Avocado Ceramide Redness Relief Serum', skinType='combination', ingredients='Water/Aqua/Eau, Glycerin, Jojoba Esters, Persea Gratissima (Avocado) Oil, Persea Gratissima (Avocado) Fruit Extract, Niacinamide, Ceramide NP, Ceramide NS, Ceramide AP, Ceramide EOP, Ceramide EOS, Hydrolyzed Rice Protein, Allantoin, Oryza Sativa (Rice) Bran Oil, Bisabolol, Zingiber Officinale (Ginger) Root Extract, Curcuma Longa (Turmeric) Root Extract, Tocopherol, Palmitoyl Tripeptide-8, Vitis Vinifera (Grape) Fruit Extract, Potassium Palmitoyl Hydrolyzed Wheat Protein, Boswellia Serrata Extract, Populus Tremuloides Bark Extract, Caprylic/Capric Triglyceride, Sodium Phytate, Cetyl Alcohol, Melia Azadirachta Flower Extract, Melia Azadirachta Leaf Extract, Ocimum Sanctum Leaf Extract, Behenic Acid, Cholesterol, Ethylhexylglycerin, Ocimum Basilicum (Basil) Flower/Leaf Extract, Elettaria Cardamomum Seed Extract, Jasminum Officinale (Jasmine) Flower/Leaf Extract, Corallina Officinalis Extract, Sodium Carbonate, Sodium Chloride, Chlorophyllin-Copper Complex (CI 75810), Camellia Sinensis Leaf Extract, Cananga Odorata Flower Extract, Caprooyl Phytosphingosine, Caprooyl Sphingosine, Cucumis Melo (Melon) Fruit Extract, Cucumis Sativus (Cucumber) Fruit Extract, Pyrus Malus (Apple) Fruit Extract, Rose Extract, Rubus Idaeus (Raspberry) Leaf Extract, Ascorbyl Palmitate, Dextran, Hydroxyacetophenone, Xanthan Gum, Butylene Glycol, Carbomer, Cetearyl Olivate, Sorbitan Olivate, 1,2-Hexanediol, Caprylyl Glycol, Hydrogenated Vegetable Oil, Lavandula Angustifolia (Lavender) Flower/Leaf/Stem Extract, Santalum Album (Sandalwood) Wood Extract, Tocopheryl Acetate, Ceteareth-25, Sodium Hydroxide, Phenoxyethanol, Sodium Benzoate', date='2023')
    u5 = Client(product='Paula’s Choice Pore-Reducing Toner', skinType='oily', ingredients='Water, Glycerin, Butylene Glycol, Niacinamide, Adenosine Triphosphate, Anthemis Nobilis (Chamomile) Flower Extract (anti-irritant), Arctium Lappa (Burdock) Root Extract, Hydrolyzed Jojoba Esters, Hydrolyzed Vegetable Protein, Sodium PCA, Panthenol, Sodium Hyaluronate, Sodium Chondroitin Sulfate, Ceramide 3, Ceramide 6 II, Ceramide 1, Phytosphingosine, Cholesterol, Tetrahexyldecyl Ascorbate, Oleth-10, DEA-Oleth-10 Phosphate, Sodium Lauroyl Lactylate, Polysorbate-20, Caprylyl Glycol, Hexylene Glycol, Sodium Citrate, Xanthan Gum, Trisodium EDTA, Phenoxyethanol', date='2023')
    u6 = Client(product='Drunk Elephant Beste No. 9 Jelly Cleanser', skinType='oily',ingredients='Water/Aqua/Eau, Glycerin, Cocamidopropyl Betaine, Coco-Glucoside, Sodium Lauroyl Methyl Isethionate, Cocamidopropyl Hydroxysultaine, Sodium Methyl Oleoyl Taurate, Propanediol, Aloe Barbadensis Leaf Extract, Glycolipids, Linoleic Acid, Linolenic Acid, Lauryl Glucoside, Cucumis Melo Cantalupensis Fruit Extract, Sclerocarya Birrea Seed Oil, Dipotassium Glycyrrhizate, Tocopherol, Citric Acid, Phenoxyethanol, Sodium Hydroxide, Sodium Benzoate, Sodium Chloride, Polylysine', date='2023')

    clients = [u1, u2, u3, u4, u5, u6]

    """Builds sample user/note(s) data"""
    for client in clients:
        try:
            '''add a few 1 to 4 notes per user'''
            for num in range(randrange(1, 4)):
                note = "#### " + client.product + " note " + str(num) + ". \n Generated by test data."
                client.tosts.append(Tost(id=client.id, note=note, image='ncs_logo.png'))
            '''add user/post data to table'''
            client.create()
        except IntegrityError:
            '''fails with bad or duplicate data'''
            db.session.remove()
            print(f"Records exist, duplicate email, or error: {client.uid}")



