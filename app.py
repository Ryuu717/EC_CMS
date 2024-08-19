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
            image_url=form.image_url.data
        )
        try:
            # Add the product to the database
            db.session.add(new_product)
            db.session.commit()
            flash('Product added successfully!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'danger')

    return render_template('add_product.html', form=form)

@app.route('/admin/products/edit/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    # Get the product by ID
    product = Product.query.get_or_404(product_id)

    # Create the form and populate it with the existing product data
    form = ProductForm(obj=product)

    # Update the category choices in the form
    form.category_id.choices = [(c.id, c.name) for c in Category.query.all()]

    if form.validate_on_submit():
        try:
            # Update the product with the form data
            product.name = form.name.data
            product.description = form.description.data
            product.price = form.price.data
            product.stock_quantity = form.stock_quantity.data
            product.category_id = form.category_id.data
            product.image_url = form.image_url.data

            # Commit the changes to the database
            db.session.commit()
            flash('Product updated successfully!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'danger')
    
    # Render the edit product page
    return render_template('edit_product.html', form=form, product=product)

@app.route('/admin/products/delete/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    # Get the product by ID, or return a 404 if not found
    product = Product.query.get_or_404(product_id)

    try:
        # Delete the product from the database
        db.session.delete(product)
        db.session.commit()
        flash('Product deleted successfully!', 'success')
    except Exception as e:
        # Rollback in case of error
        db.session.rollback()
        flash(f'Error: {str(e)}', 'danger')

    # Redirect back to the product management page
    return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(debug=True)
