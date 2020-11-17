"""Server for HB Capstone app."""

from flask import (Flask, render_template, request, flash, session, redirect, jsonify)
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
        session["current_user"] = user.user_id
        session["logged_in"] = True
        flash(f'Log in successful! Current user:{session["current_user"]} Logged in: {session["logged_in"]}')

        return redirect(f'/user/{session["current_user"]}/inventory')
    else:
        flash('Log in unsuccessful. Please try again.')
        
    return render_template('login.html')

# FIXME : Uses GET method to logout; should replace with Flask-Login library       
@app.route('/logout')
def logout():
    """Log out current user."""

    session["current_user"] = None
    session["logged_in"] = False

    return redirect('/')

@app.route('/user/<user_id>/inventory')
def user_inventory(user_id):
    """View user inventory."""

    if session.get('logged_in') == True and int(user_id) == session.get('current_user'):
        user = crud.get_user_by_id(user_id)
        inventory = crud.get_first_inventory_for_user(user)

        return render_template('user-inventory.html', user=user, inventory=inventory)

    else:
        return redirect('/')

@app.route('/user/<user_id>/expiration-report')
def expiration_report(user_id):
    """View user expiration report."""

    if session.get('logged_in') == True and int(user_id) == session.get('current_user'):
        user = crud.get_user_by_id(user_id)
        inventory = crud.get_first_inventory_for_user(user)

        expiring_items = crud.get_items_expiring(inventory, 30)

        return render_template('expiration-report.html', 
                                user=user, 
                                expiring_items=expiring_items)
    
    else:
        return redirect('/')

@app.route('/user/<user_id>/inventory/item-editor')
def item_editor(user_id):
    """View item editor."""

    if session.get('logged_in') == True and int(user_id) == session.get('current_user'):
        return render_template('item-editor.html')
    
    else:
        return redirect('/')


@app.route('/user/<user_id>/inventory/add-item', methods=['GET','POST'])
def add_item(user_id):

    if session.get('logged_in') == True and int(user_id) == session.get('current_user'):
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
    
    else:
        return redirect('/')

@app.route('/get-item-ids')
def get_item_ids():

    user_item_dict = {}
    item_dict = {}
    user = crud.get_user_by_id(session['current_user'])
    inventory = crud.get_first_inventory_for_user(user)
    for item in inventory.items:
        item_dict[item.name] = item.item_id
    
    user_item_dict['user_id'] = user.user_id
    user_item_dict['items'] = item_dict

    print(f'{user_item_dict}')

    return jsonify(user_item_dict)

@app.route('/user/<user_id>/inventory/item-editor/<item_id>')
def edit_item(user_id, item_id):
    if session.get('logged_in') == True and int(user_id) == session.get('current_user'):
        
        item = crud.get_item_by_id(item_id)

        if item:
            return render_template('item-editor.html', item=item)
        else: 
            return redirect(f'/user/{user_id}/inventory')

    else:
        return redirect('/')

@app.route('/user/<user_id>/inventory/<item_id>/save-item', methods=['POST'])
def save_item(user_id, item_id):

    if session.get('logged_in') == True and int(user_id) == session.get('current_user'):
        user = crud.get_user_by_id(user_id)
        item = crud.get_item_by_id(item_id)
            
        name = request.form.get('name')
        quantity = request.form.get('quantity')
        expiration_date = request.form.get('expiration-date')

        if name != item.name:
            crud.update_item_name(item, name)
        
        if quantity != item.quantity:
            crud.update_item_quantity(item, quantity)

        if expiration_date != item.expiration_date:
            crud.set_expiration_date(item, expiration_date)

        return redirect(f'/user/{user_id}/inventory')
    
    else:
        return redirect('/')

if __name__ == '__main__':
    app.debug = False
    DebugToolbarExtension(app)
    connect_to_db(app, 'hbcapstone')
    app.run(host='0.0.0.0', debug=True)