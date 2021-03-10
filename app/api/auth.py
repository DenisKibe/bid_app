from flask import request, g, Response, json
from flask_jwt_extended import create_access_token, jwt_required,get_jwt_identity
from flask_jwt_extended.view_decorators import verify_jwt_in_request
from app.models import AccountDetailsModel, UserModel, WalletModel
from flask_restful import Resource
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
import datetime
from functools import wraps


#flask decorator to control privilages
def restricted(level):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            g.user = UserModel.query.filter_by(id = get_jwt_identity()).first()
            if not g.user.role == level:
                respObj = {
                    'status': 'failed',
                    'message' : 'Only {} allowed to make this request.'.format(level)
                }
            
                return Response(json.dumps(respObj),mimetype='application/json',status=403)
            return func(*args, **kwargs)
        return wrapper
    return decorator

class SignupAPI(Resource):
    @restricted(level='Outlet')
    def post(self):
        #check if the request is made by an outlet 
        
        print('here')
        #get the posted data
        post_data = request.get_json()
        print(post_data)
        #check if user with email already exists
        user = UserModel.query.filter_by(email = post_data.get('email')).first()
        
        if not user:
            print('here1')
            try:
                new_user = UserModel(
                    email = post_data.get('email'),
                    first_name = post_data.get('fName'),
                    last_name = post_data.get('lName'),
                    password = generate_password_hash(post_data.get('password')),
                    outlet_id = g.user.outlet_id,
                )

                #commit data to db
                db.session.add(new_user)
                db.session.commit()
                user=UserModel.query.filter_by(email = post_data.get('email')).first()
                
                new_details = AccountDetailsModel(
                    user_id = user.id,
                    nickname= None,
                    middle_name=None,
                    phone_number=None,
                    id_number=None,
                    dob=None,
                    gender=None,
                    profile_pic_url=None
                    
                )
                
                new_wallet = WalletModel(
                    user_id = user.id
                )
                db.session.add(new_details)
                db.session.add(new_wallet)
                db.session.commit()
                
                respObj = {
                    'status' : 'success',
                    'message' : 'User is now Registered. You can now login'
                }
                return Response(json.dumps(respObj), mimetype='application/json', status=200)
            except Exception as e:
                print(e)
                respObj = {
                    'status' : 'Error',
                    'message' : 'Some error occurred! Please Try again later'
                }
                return Response(json.dumps(respObj),mimetype='application/json',status=202)
        else:
            respObj = {
                'status' : 'failed',
                'message' : 'Oops! That user already exists.'
            }
            return Response(json.dumps(respObj), mimetype='application/json',status=400)
       
        
        
class GetTokenAPI(Resource):
    def post(self):
        #get the posted data
        post_data = request.get_json()
        try:
            #fetch the user data
            user_email =UserModel.query.filter_by(email=post_data.get('email')).first()
            if user_email:
                if check_password_hash(user_email.password, post_data.get('password')):
                    expires = datetime.timedelta(hours=2)
                    expires_in = 2 * 3600
                    access_token = create_access_token(identity= str(user_email.id), expires_delta = expires)
                    respObj = {
                        'access_token': access_token,
                        'expires_in' : expires_in,
                        'token_type' : 'Bearer'
                    }
                    print(respObj)
                    
                    return Response(json.dumps(respObj), mimetype='application/json',status=200)
                else:
                    respObj = {
                        'status':'failed',
                        'message':'Incorrect password!'
                    }
                    return Response(json.dumps(respObj), mimetype='application/json', status=400)
            else:
                respObj = {
                    'status':'failed',
                    'message':'Invalid User!'
                }
               
                return Response(json.dumps(respObj), mimetype='application/json', status=400)
        except Exception as e:
            respObj = {
                'status':'failed',
                'message':'An error occurred! Please Try again later'
            }
           
            return Response(json.dumps(respObj), mimetype='application/json', status=403)
        
class ResetPasswordAPI(Resource):
    @jwt_required
    def post(self):
        #something will go here
        return #something
    
class ForgetPasswordAPI(Resource):
    def post(self):
        #something goes here
        return #something
    
class EmailVerificationAPI(Resource):
    def post(self):
        #something goes here
        return #something
    
class PhoneVerificationAPI(Resource):
    def post(self):
        #somthing goes here
        return #something
    

    
                
        