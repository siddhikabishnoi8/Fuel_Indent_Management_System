from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class FuelIndent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nameplate = db.Column(db.String(80), unique=True, nullable=False)
    fuel_type = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    quality = db.Column(db.String(120))
    calorific_value = db.Column(db.Float)
    sulfur_content = db.Column(db.Float)
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'))
    supplier = db.relationship('Supplier', backref=db.backref('indents', lazy=True))
    price = db.Column(db.Float)
    contract_terms = db.Column(db.Text)
    budget = db.Column(db.Float)
    funding = db.Column(db.Float)
    date = db.Column(db.DateTime, default=datetime.utcnow)

class Supplier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    proximity = db.Column(db.String(100))
    reliability = db.Column(db.String(100))
    pricing = db.Column(db.Float)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
