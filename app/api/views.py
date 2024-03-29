from flask import json, request, Response, url_for, render_template
from flask_jwt_extended import jwt_required, get_jwt_identity, decode_token
import requests
from werkzeug.utils import secure_filename
from app.models import BidModel, UserModel, ProductsModel,ProductCategoryModel,AccountDetailsModel,WalletModel, gen_id, CodeModel
from flask_restful import Resource
import datetime,os
from app.api.auth import restricted,g
from app import db,app
from app.services.mail_services import send_email
from jwt import ExpiredSignatureError


class ProductsAPI(Resource):
    @restricted(level='Outlet')
    def get(self):
        responseBody=[]
        try:
            category = ProductCategoryModel.query.filter_by(name = request.args.get('category')).first()
            if request.args.get('state') == 'ACTIVE':
                products = ProductsModel.query.filter_by(outlet_id = g.user.outlet_id, category_id = category.id).filter(ProductsModel.expiry_date > datetime.datetime.now()).order_by(ProductsModel.updated_on.desc())
            else:
                products = ProductsModel.query.filter_by(outlet_id = g.user.outlet_id, category_id = category.id).filter(ProductsModel.expiry_date < datetime.datetime.now()).order_by(ProductsModel.updated_on.desc())
            
            #create an obj for each result
            for product in products:
                respObj = {
                    'id' : product.id,
                    'name' : product.name,
                    'description' : product.description,
                    'image_url' : product.image_url,
                    'expiry_date':product.expiry_date.strftime("%Y:%m:%dT%H:%M:%S")
                }
                responseBody.append(respObj)
                
            return Response(json.dumps(responseBody),mimetype='application/json',status=200)
        except Exception as e:
            print (e)
            respObj = {
                'status':'failed',
                'message':'We experienced some errors.Please try again later'
            }
            return Response(json.dumps(respObj),mimetype='application/json',status=400)
        
        
                
    @staticmethod
    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.',1)[1].lower() in app.config['ALLOWED_EXTENSIONS']   
    
    @staticmethod
    def upload_image(file):
        file_name = file.filename
        
        if file_name is None:
            return ''
        
        if file and ProductsAPI.allowed_file(file_name):
            try:
                filename = secure_filename('.'.join([gen_id(10),file_name.rsplit('.',1)[1]]))
                file.save(os.path.join(app.config['UPLOAD_FOLDER']+'products',filename))
                
                image_url = '/'.join(['/images/products',filename])
        
                return image_url
            except Exception as e:
                return ''
        else:
            return ''

    @restricted(level='Outlet')
    def post(self):
        try:
            file = request.files['image']
            post_data = request.form
        
            category = ProductCategoryModel.query.filter_by(name = post_data.get('productCategory')).first()
            
            new_product = ProductsModel(
                name = post_data.get('name'),
                description = post_data.get('description'),
                buying_price = post_data.get('retailPrice'),
                state = post_data.get('state'),
                category_id = category.id,
                image_url = ProductsAPI.upload_image(file),
                outlet_id = g.user.outlet_id,
                expiry_date = post_data.get('expiryDate')
            )
            
            #commit changes
            db.session.add(new_product)
            db.session.commit()
            
            
            respObj = {
                'status':'success',
                'message' : 'New product created successifully'
            }
            return Response(json.dumps(respObj),mimetype='application/json',status=200)
        except Exception as e:
            print(e)
            respObj = {
                'status' : 'failed',
                'message' : 'Some error occured. Please Try again later'
            }
            return Response(json.dumps(respObj),mimetype='application/json',status=400)


    @restricted(level='Outlet')
    def put(self):
        post_data = request.get_json()
        try:
            product = ProductsModel.query.filter_by(id = post_data.id).first()
            
            product.name = post_data.name
            product.description = post_data.description
            product.buying_price = post_data.retailPrice
            product.state = post_data.state
            product.expiry_date = post_data.expiryDate
            
            db.session.commit()
            
            respObj = {
                'status':'success',
                'message' : 'product edited successfully'
            }
            
            return Response(json.dumps(respObj),mimetype='application/json',status=200)
        except Exception as e:
            respObj = {
                'status' : 'failed',
                'message' : 'An error occured while handling your request! Please try again later'
            }
            return Response(json.dumps(respObj),mimetype='application/json',status=200)

    
    
class AccountDetailsAPI(Resource):
    @jwt_required()
    def get(self):
        
        try:
            current_user = AccountDetailsModel.query.filter_by(user_id = get_jwt_identity()).first()
            
            respObj = {
                'id' : current_user.id,
                'name': current_user.user.first_name +" "+current_user.user.last_name,
                'username' : current_user.user.email,
                'uId' : current_user.user.id,
                'email' : current_user.user.email,
                'role' : current_user.user.role,
                'outletId' :current_user.user.outlet_id,
                'nickname' : current_user.nickname,
                'phoneNumber' : current_user.phone_number,
                'idNumber' : current_user.id_number,
                'gender' : current_user.gender,
                'dob' : current_user.dob,
                'ProfilePic' : current_user.profile_pic_url,
                'emailConfirmed' : current_user.is_email_verified,
                'phoneNumberConfirmed' : current_user.is_phone_verified, 
            }
            return Response(json.dumps(respObj),mimetype='application/json', status=200) 
        except Exception as e:
            print(e)
            respObj = {
                'status':'failed',
                'message':'We experinced an Error!Please try again later'
            }
            return Response(json.dumps(respObj),mimetype='application/json', status=400)
        
        
    @jwt_required()
    def put(self):
        post_data= request.get_json()
        try:
            current_user = AccountDetailsModel.query.filter_by(user_id = get_jwt_identity()).first()
            
            current_user.nickname = post_data.get('nickName')
            current_user.middle_name = post_data.get('middleName')
            current_user.phone_number = post_data.get('phoneNumber')
            current_user.id_number = post_data.get('idNumber')
            current_user.dob = post_data.get('dob')
            current_user.gender = post_data.get('gender')
            
            db.session.commit()
            
            respObj = {
                'status' : 'success',
                'message' : 'details registered successfully.'
            }
            
            return Response(json.dumps(respObj),mimetype='application/json',status=200)
            
        except Exception as e:
            respObj = {
                'status' : 'failed',
                'message' : 'An error occured while handling your request! Please try again later'
            }
            return Response(json.dumps(respObj),mimetype='application/json',status=200)
                
class WalletDetailsAPI(Resource):
    @restricted(level='Customer')
    def post(self):
        #for topup and staff
        return
    
    @restricted(level='Customer')
    def get(self):
        try:
            wallet = WalletModel.query.filter_by(user_id = g.user.id).first()
            
            respObj = {
                'id' : wallet.id,
                'balance' : wallet.balance,
                'bonus' : wallet.bonus
            }
            
            return Response(json.dumps(respObj), mimetype='application/json', status =200)
        except Exception as e:
            print(e)
            respObj = {
                'status' : 'failed',
                'message' : 'We experinced some error while handling the request! Please try again later.'
            }
            
            return Response(json.dumps(respObj), mimetype='application/json',status=400)
  
class UploadImageAPI(Resource):    
    @jwt_required()
    def post(self):
        image = request.files['image']
        
        file_name = image.filename
        
        if file_name is None:
            respObj = {
                'status':'failed',
                'message' : 'No selected file'
            }
            return Response(json.dumps(respObj), mimetype='application/json',status=400)
        
        if image and ProductsAPI.allowed_file(file_name):
            try:
                filename = secure_filename('.'.join([gen_id(7),file_name.rsplit('.',1)[1]]))
                image.save(os.path.join(app.config['UPLOAD_FOLDER']+'profile_pic',filename))
                
                profile_pic_url = '/'.join(['/images/profile_pic',filename])
                
                current_user_account = AccountDetailsModel.query.filter_by(user_id = get_jwt_identity()).first()
                current_user_account.profile_pic_url = profile_pic_url
                
                db.session.commit()
                
                respObj = {
                    'status' : 'success',
                    'message' : 'Profile Pic uploaded successfully'
                }
                return Response(json.dumps(respObj), mimetype='application/json',status=200)
            except Exception as e:
                respObj = {
                    'status' : 'failed',
                    'message' : 'some error occured while handling the request. Please try again later'
                }
                return Response(json.dumps(respObj), mimetype='application/json',status=400)
        else:
            respObj = {
                'status' : 'failed',
                'message' : 'not a valid file to upload'
            }
            return Response(json.dumps(respObj), mimetype='application/json',status=400)

class BidAPI(Resource):
    @restricted(level='Customer')
    def post(self):
        post_data = request.get_json()
        
        try:
            
            new_bid = BidModel(
                user_id = g.user.id,
                product_id = post_data.auctionId,
                bid_amount = post_data.amount
            )
            
            db.session.add(new_bid)
            db.session.commit()
            
            respObj = {
                'status' : 'success',
                'message' : 'bid placed successfully'
            }
            
            return Response(json.dumps(respObj), mimetype='application/json',status=200)
        except Exception as e:
            respObj = {
                'status' : 'failed',
                'message' : 'some error occured while handling the request. Please try again later'
            }
            return Response(json.dumps(respObj), mimetype='application/json',status=400)
        
    @restricted(level='Customer')
    def put(self):
        post_data = request.get_json()
        
        try:
            bid = BidModel.query.filter_by(id = post_data.id).first()
            
            bid.bid_amount = bid.bid_amount * post_data.times
            
            db.session.commit()
            
            respObj = {
                'status' : 'success',
                'message' : 'bid successfully promoted'
            }
            
            return Response(json.dumps(respObj), mimetype='application/json',status=200)
        except Exception as e:
            respObj = {
                'status' : 'Error',
                'message' : 'An error occured while handling the request. Please try again later.'
            }
            
            return Response(json.dumps(respObj), mimetype='application/json',status=400)
        
    @restricted(level='Outlet')
    def get(self):
        try:
            bids = BidModel.query.filter_by(product_id = request.args.get('auctionId')).order_by(BidModel.bid_amount.desc()).limit(5)
            responseBody=[]
            pos=0
            for bid in bids:
                pos +=1
                respObj = {
                    'postion' : pos,
                    'url' : bid.account_detail.profile_pic_url,
                    'userName' : bid.user.account_detail.nickname,
                    'totalBids' : bid.total_amount
                }
                responseBody.append(respObj)
                
            return Response(json.dumps(responseBody), mimetype='application/json',status=200)
        except Exception as e:
            respObj = {
                'status' : 'failed',
                'message' : 'Some error occured while handling this request. Try again later.'
            }
            
            return Response(json.dumps(respObj), mimetype='application/json',status=400)
        
class AccountExtrasAPI(Resource):
    @restricted(level = 'Customer')
    def post(self):
        post_data = request.get_json()
        
        try:
            bids = BidModel.query.filter_by(product_id = post_data.auctionId, user_id = g.user.id).all()
            
            responseBody = []
            for bid in bids:
                respObjs = {
                    'id' : bid.id,
                    'amount' : bid.bid_amount
                }
                responseBody.append(respObjs)
                
            respObj = {
                'userName' : g.user.first_name + ' '+g.user.last_name,
                'totalBids' : bids.count(),
                'bids' : responseBody
            }
            print(respObj)
            
            return Response(json.dumps(respObj), mimetype='application/json',status=200)
        except Exception as e:
            print(e)
            respObj = {
                'status' : 'failed',
                'message' : 'Some error occured while handling the request. Please try again later.'
            }
            
            return Response(json.dumps(respObj), mimetype='application/json',status=400)
    
    @restricted(level = 'Outlet')
    def get(self):
            return Response(json.dumps({}), mimetype='application/json',status=200)
        
class SendEmaiLAPI(Resource):
    @restricted(level = 'Outlet')
    def post(self):
        try:
            post_data = request.get_json()
           
            send_email(post_data.get('subject'),
                       sender='noreply@test.com',
                       recipients=[post_data.get('emailAddress')],
                       text_body=render_template('support_email.txt', message=post_data.get('emailBody')),
                       html_body=render_template('support_email.html', message=post_data.get('emailBody'))
                    )
            respObj = {
                'status' : 'success',
                'message' : 'Email sent successifully. Check your Email for further communications.'
            }
            return Response(json.dumps(respObj), mimetype='application/json',status=200)
        except Exception as e:
            
            respObj = {
                'status' : 'failed',
                'message' : 'An error occured while handling this request. Please try again later.'
            }
            
            return Response(json.dumps(respObj), mimetype='application/json',status=400)
        
class VerifyEmailAPI(Resource):
    @restricted(level = 'Outlet')
    def get(self):
        try:
            payload = decode_token(request.args.get('xc'))
            
            code = CodeModel.query.filter_by(user_id = payload['sub'], code = request.args.get('ud'), field = 'Email').filter(CodeModel.expiry_time > datetime.datetime.now()).first()
            if not code:
                raise ExpiredSignatureError
            
            account = AccountDetailsModel.query.filter_by(user_id = payload['sub']).first()
            account.is_email_verified = True
            db.session.commit()
            
            respObj = {
                'status' : 'success',
                'message' : 'Email verified successfully'
            }
            
            return Response(json.dumps(respObj), mimetype='application/json',status=200)
        except ExpiredSignatureError:
            respObj = {
                'status' : 'failed',
                'message' : 'Activation link has expired. Please get a new Link'
            }
            return Response(json.dumps(respObj), mimetype='application/json',status=401)
        except Exception as e:
            
            respObj = {
                'status' : 'failed',
                'message' : 'An Error occured while processing this request. Please try again later.'
            }
            return Response(json.dumps(respObj), mimetype='application/json',status=400)

class ResetForgotPasswordAPI(Resource):
    @restricted(level = 'Outlet')
    def post(self):
        post_data = request.get_json()

        try:
            user = UserModel.query.filter_by(email = post_data.get('email')).first()
            if not user:
                raise NameError

            code = CodeModel.query.filter_by(user_id = user.id, code = post_data.get('code'), field = 'Password').filter(CodeModel.expiry_time > datetime.datetime.now()).first()
            if not code:
                raise ExpiredSignatureError

            user.password = post_data.password

            db.session.commit()

            respObj = {
                'status' : 'Success',
                'message' : 'Password change successfully, You can now login.'
            }
            return Response(json.dumps(respObj), mimetype='application/json',status=200)
        except NameError:
            respObj ={
                'status':'failed',
                'message' : 'Invalid email'
            }
            return Response(json.dumps(respObj), mimetype='application/json',status=400)

        except ExpiredSignatureError:
            respObj ={
                'status':'failed',
                'message' : 'verification code expired.'
            }
            return Response(json.dumps(respObj), mimetype='application/json',status=403)

        except Exception as e:
            
            respObj = {
                'status' : 'failed',
                'message' : 'An Error occured while processing this request. Please try again later.'
            }
            return Response(json.dumps(respObj), mimetype='application/json',status=400)

class VerifySmsCode(Resource):
    @restricted(level = 'Customer')
    def post(self):
        post_data = request.get_json()

        try:
            code = CodeModel.query.filter_by(user_id = g.user.id, code = post_data.get('code'), field = 'Phonenumber').filter(CodeModel.expiry_time > datetime.datetime.now()).first()

            if not code:
                raise ExpiredSignatureError

            user_account = AccountDetailsModel.query.filter(user_id = g.user.id).first()
            user_account.is_phone_verified = True

            db.session.commit()

            respObj = {
                'status' : 'success',
                'message' : 'Your phone number verification is successful.'
            }

            return Response(json.dumps(respObj), mimetype='application/json',status=200)

        except ExpiredSignatureError:
            respObj = {
                'status' : 'failed',
                'message' : 'The verification code is expired.'
            }

            return Response(json.dumps(respObj), mimetype='application/json',status=400)

        except Exception as e:
            respObj = {
                'status' : 'failed',
                'message' : 'An Error occured while processing this request. Please try again later.'
            }
            return Response(json.dumps(respObj), mimetype='application/json',status=400)



            