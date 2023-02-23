from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource # used for REST API building
from datetime import datetime

from model.clients import Client

client_api = Blueprint('client_api', __name__,
                   url_prefix='/api/clients')

# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(client_api)

class ClientAPI:        
    class _Create(Resource):
        def post(self):
            ''' Read data for json body '''
            body = request.get_json()
            
            ''' Avoid garbage in, error checking '''
            # validate name
            product = body.get('product')
            if product is None or len(product) < 2:
                return {'message': f'Name is missing, or is less than 2 characters'}, 210


            # look for password and dob
            ingredients = body.get('ingredients')
            date = body.get('date')
            skinType = body.get('skinType')

            ''' #1: Key code block, setup USER OBJECT '''
            uo = Client(product=product, 
                        ingredients=ingredients, date=date, skinType=skinType)
            
            ''' Additional garbage error checking '''
            # set password if provided
            ''' #2: Key Code block to add user to database '''
            # create user in database
            client = uo.create()
            # success returns json of user
            if client:
                return jsonify(client.read())
            # failure returns error
            return {'message': f'Processed {product}, either a format error or User ID {skinType} is duplicate'}, 210

    class _Read(Resource):
        def get(self):
            clients = Client.query.all()    # read/extract all users from database
            json_ready = [client.read() for client in clients]  # prepare output in json
            return jsonify(json_ready)  # jsonify creates Flask response object, more specific to APIs than json.dumps

    # building RESTapi endpoint
    api.add_resource(_Create, '/create')
    api.add_resource(_Read, '/')