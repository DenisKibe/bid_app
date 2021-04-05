from flask import request, g, Response, json, render_template
from flask_jwt_extended import create_access_token, jwt_required,get_jwt_identity
from flask_jwt_extended.view_decorators import verify_jwt_in_request
from app.models import AccountDetailsModel, UserModel, WalletModel, CodeModel
from flask_restful import Resource
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
import datetime
from functools import wraps
from app.email.mail_services import send_email


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
    @jwt_required()
    def put(self):
        post_data = request.get_json()
        
        try:
            user = UserModel.query.filter_by(id = get_jwt_identity()).first()
            
            if check_password_hash(user.password,post_data.get('oldPassword')):
                user.password = generate_password_hash(post_data.get('newPassword'))
                db.session.commit()
                
                send_email("Account Password Reset Activity",
                        sender = 'noreply@test.com',
                        recipients=[user.email],
                        text_body=render_template('resetpassword_email.txt', name = user.first_name +" "+user.last_name, newpassword = post_data.get('newPassword')),
                        html_body=render_template('resetpassword_email.html', name = user.first_name +" "+user.last_name, newpassword = post_data.get('newPassword'))
                        )
                
                respObj = {
                    'status' : 'success',
                    'message' : 'Your password has been reset successfully.'
                }
                return Response(json.dumps(respObj), mimetype='application/json', status=200)
            else:
                respObj = {
                    'status':'failed',
                    'message' : 'Incorrect Old Password.'
                }
                return Response(json.dumps(respObj), mimetype='application/json', status=400)
       
        except Exception as e:
            respObj = {
                'status' : 'failed',
                'message' : 'An error occured while processing the request. Please try again later.'
            }
            return Response(json.dumps(respObj), mimetype='application/json', status=400)
    
class ForgetPasswordAPI(Resource):
    @jwt_required()
    def post(self):
        post_data = request.get_json()
        
        try:
            user = UserModel.query.filter_by(email = post_data.get('email')).first()
            code = CodeModel.query.filter_by(user_id = user.id, field = "Password").filter(CodeModel.expiry_time > datetime.datetime.now()).first()
            
            if not code:
                new_code = CodeModel(
                    user_id= user.id,
                    field = 'Password',
                    expiry_time= (datetime.datetime.now() + datetime.timedelta(minutes=15))
                )
                
                #commit changes
                db.session.add(new_code)
                db.session.commit()
                
                #get ud from the database
                code = CodeModel.query.filter_by(user_id = user.id, field = "Password").filter(CodeModel.expiry_time > datetime.datetime.now()).first()
                ud = code.code
                
                #create xc (access token)
                expires = datetime.timedelta(minutes=15)
                xc = create_access_token(identity= str(user.id), expires_delta = expires)
                
                send_email("",
                        sender = 'noreply@test.com',
                        recipients=[g.user.email],
                        text_body=render_template('confirm_email.txt', name=g.user.first_name +" "+g.user.last_name,appName=post_data.get('appName'),url = post_data.get('confirmationEndpoint')+"?ud="+ud+"&xc="+xc),
                        html_body=render_template('confirm_email.html', name=g.user.first_name +" "+g.user.last_name,appName=post_data.get('appName'),url = post_data.get('confirmationEndpoint')+"?ud="+ud+"&xc="+xc)
                        )
                
                respObj = {
                    'status' : 'success',
                    'message' : 'Email verification code sent to you Email. Kindly follow the Email to confirm your account.'
                }
                return Response(json.dumps(respObj), mimetype='application/json',status=200)
            else:
                respObj = {
                    'status' : 'success',
                    'message' : 'Verification link already sent to your Email.'
                }
                return Response(json.dumps(respObj), mimetype='application/json',status=200)

        return #something
    
class EmailVerificationAPI(Resource):
    @restricted(level = 'Customer')
    def post(self):
        post_data = request.get_json()
        
        try:
            code = CodeModel.query.filter_by(user_id = g.user.id, field = "Email").filter(CodeModel.expiry_time > datetime.datetime.now()).first()
            
            if not code:
                new_code = CodeModel(
                    user_id= g.user.id,
                    field = 'Email',
                    expiry_time= (datetime.datetime.now() + datetime.timedelta(minutes=15))
                )
                
                #commit changes
                db.session.add(new_code)
                db.session.commit()
                
                #get ud from the database
                code = CodeModel.query.filter_by(user_id = g.user.id, field = "Email").filter(CodeModel.expiry_time > datetime.datetime.now()).first()
                ud = code.code
                
                #create xc (access token)
                expires = datetime.timedelta(minutes=15)
                xc = create_access_token(identity= str(g.user.id), expires_delta = expires)
                
                send_email("Welcome to Bid App",
                        sender = 'noreply@test.com',
                        recipients=[g.user.email],
                        text_body=render_template('confirm_email.txt', name=g.user.first_name +" "+g.user.last_name,appName=post_data.get('appName'),url = post_data.get('confirmationEndpoint')+"?ud="+ud+"&xc="+xc),
                        html_body=render_template('confirm_email.html', name=g.user.first_name +" "+g.user.last_name,appName=post_data.get('appName'),url = post_data.get('confirmationEndpoint')+"?ud="+ud+"&xc="+xc)
                        )
                
                respObj = {
                    'status' : 'success',
                    'message' : 'Email verification code sent to you Email. Kindly follow the Email to confirm your account.'
                }
                return Response(json.dumps(respObj), mimetype='application/json',status=200)
            else:
                respObj = {
                    'status' : 'success',
                    'message' : 'Verification link already sent to your Email.'
                }
                return Response(json.dumps(respObj), mimetype='application/json',status=200)
        except Exception as e:
            print(e)
            respObj = {
                'status' : 'failed',
                'message' : 'An error occured while handling this request. Please try again later.'
            }
            return Response(json.dumps(respObj), mimetype='application/json',status=400)
    
class PhoneVerificationAPI(Resource):
    def post(self):
        #somthing goes here
        return #something
    

    
                
        