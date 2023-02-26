from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource # used for REST API building
from datetime import datetime

from model.skintypes import SkinType

skintype_api = Blueprint('skintype_api', __name__,
                   url_prefix='/api/skintype')

# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(skintype_api)

#Create new class to bundle the following data and preform specific methods to it later
class SkinTypeAPI:        
    class _Create(Resource):
        def post(self):
            ''' Read data for json body '''
            body = request.get_json()
            
            ''' Avoid garbage in, error checking '''
            # validate Skin type
            skin_type = body.get('skin_type')
            if skin_type is None or len(skin_type) < 2:
                return {'message': f'Skin type is missing, or is less than 2 characters'}, 210
            # validate moisturizer
            moisturizer = body.get('moisturizer')
            if moisturizer is None or len(moisturizer) < 2:
                return {'message': f'Moisturizer is missing, or is less than 2 characters'}, 210
            # validate Face cleanser
            face_cleanser = body.get('face_cleanser')
            if face_cleanser is None or len(face_cleanser) < 2:
                return {'message': f'Face cleanser is missing, or is less than 2 characters'}, 210
            # validate Serum
            serum = body.get('serum')
            if serum is None or len(serum) < 2:
                return {'message': f'Serum is missing, or is less than 2 characters'}, 210
            # validate Sunscreen
            sunscreen = body.get('sunscreen')
            if sunscreen is None or len(sunscreen) < 2:
                return {'message': f'Sunscreen is missing, or is less than 2 characters'}, 210

            ''' #1: Key code block, setup SkinType OBJECT '''
            skin_type_output = SkinType(skin_type=skin_type, 
                      moisturizer=moisturizer, face_cleanser=face_cleanser, serum=serum, sunscreen=sunscreen)
            
            ''' Additional garbage error checking '''
            # set skin_type if provided
            if skin_type_output is not None:
                skin_type_output.SkinType.setter(skin_type)
            
            ''' #2: Key Code block to add SkinType to database '''
            # create SkinType in database
            skin_type_output = SkinType.create()
            # success returns json of SkinType
            if skin_type_output:
                return jsonify(skin_type_output.read())
            # failure returns error
            return {'message': f'Processed {skin_type}, either a format error or User ID {moisturizer} is duplicate'}, 210

    class _Read(Resource):
        def get(self):
            skintypes = SkinType.query.all()    # read/extract all skin types from database
            json_ready = [skintype.read() for skintype in skintypes]  # prepare output in json
            return jsonify(json_ready)  # jsonify creates Flask response object, more specific to APIs than json.dumps

    # building RESTapi endpoint
    api.add_resource(_Create, '/create')
    api.add_resource(_Read, '/')