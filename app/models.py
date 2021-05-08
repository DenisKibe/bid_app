from enum import unique
import random, string
from app import db
from sqlalchemy import text, ForeignKey
from sqlalchemy.orm import relationship

def gen_id(x):
    return ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(x))

class OutletModel(db.Model):
    __tablename__='outlet'
    
    id = db.Column(db.String(20), primary_key=True, nullable=False, unique=True, autoincrement=False, default=gen_id(16))
    name =db.Column(db.String(50), nullable=False,unique=True)
    description = db.Column(db.Text)
    created_on = db.Column(db.DateTime, server_default=text("CURRENT_TIMESTAMP")) 
    producter=relationship("ProductsModel",backref='outlet')
    users=relationship("UserModel",backref='outlet')
    
    def __init__(self,name,description):
        self.name = name
        self.description = description
        
    def __repr__(self):
        return self.id
    
class ProductsModel(db.Model):
    __tablename__='product'
    
    id = db.Column(db.String(20), primary_key=True, nullable=False,unique=True, autoincrement=False,default=gen_id(16))
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    buying_price = db.Column(db.Integer,nullable=False)
    state = db.Column(db.String(10),nullable=False)
    category_id = db.Column(db.String(20),ForeignKey('product_category.id'),nullable=False)
    image_url = db.Column(db.String(100),nullable=False)
    outlet_id = db.Column(db.String(20),ForeignKey('outlet.id'),nullable=False)
    expiry_date = db.Column(db.DateTime)
    created_on = db.Column(db.DateTime, server_default=text("CURRENT_TIMESTAMP"))
    updated_on = db.Column(db.DateTime,server_default=text("CURRENT_TIMESTAMP"),server_onupdate=text("CURRENT_TIMESTAMP"))
    bidder=relationship("BidModel",backref='product')
    
    def __init__(self,name,description,buying_price,state,category_id,image_url,outlet_id,expiry_date):
        self.name = name
        self.description = description
        self.buying_price = buying_price
        self.state = state
        self.category_id = category_id
        self.image_url = image_url
        self.outlet_id = outlet_id
        self.expiry_date = expiry_date
        
    def _repr__(self):
        return self.id
    
class ProductCategoryModel(db.Model):
    __tablename__='product_category'
    
    id = db.Column(db.String(20),primary_key=True,nullable=False,unique=True,autoincrement=False,default=gen_id(16))
    name = db.Column(db.String(50),nullable=False)
    description = db.Column(db.Text)
    created_on =  db.Column(db.DateTime, server_default=text("CURRENT_TIMESTAMP"))
    relationship("ProductsModel", backref='product_category')
    
    def __init__(self,name,description):
        self.name = name
        self.description = description
        
    def __repr__(self):
        return self.id
    
class UserModel(db.Model):
    __tablename__='user'
    
    id = db.Column(db.String(20), primary_key=True, nullable=False,unique=True,autoincrement=False,default=gen_id(16))
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(200),nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    role = db.Column(db.String(10), nullable=False, server_default='Customer')
    outlet_id = db.Column(db.String(20),ForeignKey('outlet.id'),nullable=False)
    created_on = db.Column(db.DateTime, server_default=text("CURRENT_TIMESTAMP"))
    updated_on = db.Column(db.DateTime,server_default=text("CURRENT_TIMESTAMP"), server_onupdate=text("CURRENT_TIMESTAMP"))
    acconter=relationship("AccountDetailsModel",backref='user')
    wallets=relationship("WalletModel",backref='user')
    bidder=relationship("BidModel",backref='user')
    coder=relationship("CodeModel",backref='user')
    
    def __init__(self,first_name,last_name,password,email,outlet_id):
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.email = email
        self.outlet_id = outlet_id
        
    def __repr__(self):
        return self.id
    
    
class AccountDetailsModel(db.Model):
    __tablename__='account_detail'
    id = db.Column(db.String(20), primary_key=True, nullable=False,unique=True,autoincrement=False,default=gen_id(16))
    user_id = db.Column(db.String(20),ForeignKey('user.id'),nullable=False)
    nickname = db.Column(db.String(50),nullable=True)
    middle_name = db.Column(db.String(50),nullable=True)
    phone_number = db.Column(db.String(15),nullable=True)
    id_number = db.Column(db.String(10),nullable=True)
    dob = db.Column(db.DateTime,nullable=True)
    gender = db.Column(db.String(10),nullable=True)
    profile_pic_url = db.Column(db.String(100),nullable=True)
    created_on = db.Column(db.DateTime, server_default=text("CURRENT_TIMESTAMP"))
    updated_on = db.Column(db.DateTime, server_default=text("CURRENT_TIMESTAMP"), server_onupdate=text("CURRENT_TIMESTAMP"))
    is_email_verified = db.Column(db.Boolean,default='False')
    is_phone_verified = db.Column(db.Boolean,default='False')
    
    def __init__(self,user_id,nickname,middle_name,phone_number,id_number,dob,gender,profile_pic_url):
        self.user_id =  user_id
        self.nickname = nickname
        self.middle_name = middle_name
        self.phone_number = phone_number
        self.id_number = id_number
        self.dob = dob
        self.gender = gender
        self.profile_pic_url = profile_pic_url
        
        
    def __repr__(self):
        return self.id
    
class WalletModel(db.Model):
    __tablename__='wallet'
    
    id = db.Column(db.String(20), primary_key=True, nullable=False,unique=True,autoincrement=False,default=gen_id(16))
    user_id = db.Column(db.String(20),ForeignKey('user.id'),nullable=False)
    balance = db.Column(db.Integer,default='0')
    bonus = db.Column(db.Integer,default='0')
    updated_on = db.Column(db.DateTime,server_default=text("CURRENT_TIMESTAMP"),server_onupdate=text("CURRENT_TIMESTAMP"))
    
    def __init__(self,user_id):
      self.user_id = user_id
      
      
    def __repr__(self):
        return self.id
    
class BidModel(db.Model):
    __tablename__='bid'
    
    id = db.Column(db.String(20), primary_key=True, nullable=False,unique=True,autoincrement=False, default=gen_id(16))
    user_id = db.Column(db.String(20),ForeignKey('user.id'),nullable=False)
    product_id = db.Column(db.String(20),ForeignKey('product.id'),nullable=False)
    bid_amount = db.Column(db.Integer, nullable=False)
    created_on = db.Column(db.DateTime, server_default=text("CURRENT_TIMESTAMP"))
    updated_on = db.Column(db.DateTime,server_default=text("CURRENT_TIMESTAMP"), server_onupdate=text("CURRENT_TIMESTAMP"))
    
    def __init__(self,user_id,product_id,bid_amount):
      self.user_id = user_id
      self.product_id = product_id
      self.bid_amount = bid_amount
      
    def __repr__(self):
        return self.id

class CodeModel(db.Model):
    __tablename__='code' 
    
    id = db.Column(db.Integer, autoincrement=True, primary_key=True,nullable=False)
    user_id = db.Column(db.String(20), ForeignKey('user.id'),nullable=False)
    code = db.Column(db.String(6),nullable=False, default=gen_id(6))
    field = db.Column(db.String(100),nullable=False)
    expiry_time = db.Column(db.DateTime)
    created_on = db.Column(db.DateTime, server_default=text("CURRENT_TIMESTAMP"))
    
    def __init__(self,user_id,field,expiry_time):
      self.user_id = user_id
      self.field = field
      self.expiry_time = expiry_time
      
    def __repr__(self):
        return self.id
   
    