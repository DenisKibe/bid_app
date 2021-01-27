import flask, jwt,datetime
from flask import json, Response, jsonify, make_response
from app import db, app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float,Text, TIMESTAMP,text, ForeignKey
from sqlalchemy.orm import relationship

class OutletModel(db.Model):
    __tablename__='outlet'
    
    id = db.Column(db.String(20), primary_key=True, nullable=False, unique=True, autoincrement=False)
    name =db.Column(db.String(50), nullable=False,unique=True)
    description = db.Column(db.Text)
    created_on = db.Column(db.DateTime, server_default=text("CURRENT_TIMESTAMP")) 
    
class ProductsModel(db.Model):
    __tablename__='product'
    
    id = db.Column(db.String(20), primary_key=True, nullable=False,unique=True, autoincrement=False)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    buying_price = db.Column(db.Integer,nullable=False)
    state = db.Column(db.String(10),nullable=False)
    category_id = db.Column(db.String(20),ForeignKey('product_category.id'),nullable=False)
    image_url = db.Column(db.String(100),nullable=False)
    expiry_date = db.Column(db.DateTime)
    created_on = db.Column(db.DateTime, server_default=text("CURRENT_TIMESTAMP"))
    updated_on = db.Column(db.DateTome)
    
class ProductCategoryModel(db.Model):
    __tablename__='product_category'
    
    id = db.Column(db.String(20),primary_key=True,nullable=False,unique=True,autoincrement=False)
    name = db.Column(db.String(50),nullable=False)
    description = db.Column(db.Text)
    created_on =  db.Column(db.DateTime, server_default=text("CURRENT_TIMESTAMP"))
    
class UserModel(db.Model):
    __tablename__='user'
    
    
    
class AccountDetailsModel(db.Model):
    __tablename__='account_detail'
    
class WalletModel(db.Model):
    __tablename__='wallet'
    
class BidModel(db.Model):
    __tablename__='bid'

class codeModel(db.Model):
    __tablename__='code' 