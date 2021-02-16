import re
from flask import Response, request, make_response, jsonify
from flask_jwt_extended import create_access_token, jwt_required,get_jwt_identity
from app.models import UserModel
from flask_restful import Resource
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, logger

class SignupAPI(Resource):
    @jwt_required
    def post(self):
        #check if the request is made by an outlet 
        outlet=UserModel.query.filter_by(id = get_jwt_identity()).first()
        if outlet.role == 'Outlet':
            #get the posted data
            post_data = request.get_json()
            
            #check if user with email already exists
            user = UserModel.query.filter_by(email = post_data.get('email')).first()
            
            if not user:
                try:
                    new_user = UserModel(
                        email = post_data.get('email'),
                        first_name = post_data.get('fName'),
                        last_name = post_data.get('lName'),
                        password = generate_password_hash(post_data.get('password')),
                        outlet_id = outlet.outlet_id,
                    )

                    #commit data to db
                    db.session.add(new_user)
                    db.session.commit()
                    
                    respObj = {
                        'status' : 'success',
                        'message' : 'User is now Registered. You can now login'
                    }
                    return make_response(jsonify(respObj)),200
                except Exception as e:
                    respObj = {
                        'status' : 'Error',
                        'message' : 'Some error occurred! Please Try again later'
                    }
                    return make_response(jsonify(respObj)), 202
            else:
                respObj = {
                    'status' : 'failed',
                    'message' : 'Oops! That user already exists.'
                }
                return make_response(jsonify(respObj)),400
        else:
            respObj = {
                'status' : 'failed',
                'message' : 'User must belong to an outlet.'
            }
            return make_response(jsonify(respObj)), 400
                
        