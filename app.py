from flask import Flask, flash, redirect, render_template, url_for
from models import db, Product, Category
from forms import ProductForm
from dotenv import load_dotenv
import os

import pymysql
pymysql.install_as_MySQLdb()


# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = (f"mysql://{os.getenv('RDS_USERNAME')}:{os.getenv('RDS_PASSWORD')}"f"@{os.getenv('RDS_ENDPOINT')}/{os.getenv('RDS_DB_NAME')}")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)

@app.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)


@app.route('/admin/products/new', methods=['GET', 'POST'])
def add_product():
    form = ProductForm()
    # Populate the category choices
    form.category_id.choices = [(c.id, c.name) for c in Category.query.all()]

    if form.validate_on_submit():
        # Create a new product instance with form data
        new_product = Product(
            name=form.name.data,
            description=form.description.data,
            price=form.price.data,
            stock_quantity=form.stock_quantity.data,
            category_id=form.category_id.data,
     