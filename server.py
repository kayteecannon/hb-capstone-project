"""Server for HB Capstone app."""

from flask import (Flask, render_template, request, flash, session, redirect)
from model import connect_to_db
import crud
import os
from flask_debugtoolbar import DebugToolbarExtension

from jinja2 import StrictUndefined

app = Flask(__name__)

SECRET_KEY = os.environ['SECRET_KEY']
app.secret_key = SECRET_KEY
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def homepage():
    """View homepage."""

    return render_template('homepage.html')
    
@app.route('/register', methods=['GET','POST'])
def registration():
    """View registration page."""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm-password')

        print(f'password: {password}, confirm password: {confirm_password}')

        user = crud.get_user_by_email(email)

        if user:
            flash(f'Cannot create account with email: {email}.')
        elif password == confirm_password:
            crud.create_user(email, password)
            flash('Account created successfully.  Please log in.')
            return redirect('/login')
        else:
            flash(f'Passwords do not match. Please try again.')
            return redirect('/register')

    return render_template('registration.html')

@app.route('/login')
def show_login():
    """View log in page."""
    return render_template('login.html')

@app.route('/login', methods=['GET','POST'])
def login():
    """Verify login credentials."""

    email = request.form.get('email')
    password = request.form.get('password')

    user = crud.get_user_by_email(email)
    
    if user and user.password == password:
        flash('Log in successful!')
        return redirect(f'/user/{user.user_id}/inventory')
    else:
        flash('Log in unsuccessful. Please try again.')
        
    return render_template('login.html')
        

@app.route('/user/<user_id>/inventory')
def user_inventory(user_id):
    """View user inventory."""

    user = crud.get_user_by_id(user_id)
    inventory = crud.get_first_inventory_for_user(user)

    return render_template('user-inventory.html', user=user, inventory=inventory)

@app.route('/user/<user_id>/expiration-report')
def expiration_report(user_id):
    """View user expiration report."""

    user = crud.get_user_by_id(user_id)
    inventory = crud.get_first_inventory_for_user(user)

    expiring_items = crud.get_items_expiring(inventory, 30)

    return render_template('expiration-report.html', 
                            user=user, 
                            expiring_items=expiring_items)

@app.route('/user/<user_id>/inventory/item-editor')
def item_editor(user_id):
    """View item editor."""

    return render_template('item-editor.html')


@app.route('/user/<user_id>/inventory/add-item', methods=['GET','POST'])
def add_item(user_id):

    if request.method == 'POST':
        user = crud.get_user_by_id(user_id)
        inventory = crud.get_first_inventory_for_user(user)
        
        name = request.form.get('name')
        quantity = request.form.get('quantity')
        expiration_date = request.form.get('expiration-date')

        item = crud.create_item(inventory.inventory_id, name, quantity)

        if expiration_date:
            crud.set_expiration_date(item, expiration_date)

        return redirect(f'/user/{user_id}/inventory')
    
    return render_template('add-item.html')

@app.route('/user/1/inventory/item-editor/1')
def edit_item():

    item = crud.get_item_by_id(1)

    return render_template('item-editor.html', item=item)


if __name__ == '__main__':
    app.debug = False
    DebugToolbarExtension(app)
    connect_to_db(app, 'hbcapstone')
    app.run(host='0.0.0.0', debug=True)