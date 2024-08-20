from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    products = db.relationship('Product', backref='category', lazy=True)


class Product(db.Model):
    __tablename__ = 'products2'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    stock_quantity = db.Column(db.Integer, nullable=True, default=0)
    created_at = db.Column(db.TIMESTAMP, nullable=True, default=datetime.now().date(), server_default=db.func.current_timestamp())
    updated_at = db.Column(db.TIMESTAMP, nullable=True, default=datetime.now().date(), server_default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    image_url = db.Column(db.String(255), nullable=True)
    
    
    # Foreign key should reference the correct table name
    # category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    
    

    
