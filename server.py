"""Server for HB Capstone app."""

from flask import (Flask, render_template, request, flash, session, redirect, jsonify)
from model import connect_to_db
import crud
import os
from flask_debugtoolbar import DebugToolbarExtension
import datetime

from jinja2 import StrictUndefined

import mail_helper
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

jobstores = {
    'default': SQLAlchemyJobStore(url='postgresql:///hbcapstone')
}

scheduler = BackgroundScheduler(jobstores=jobstores)


# scheduler.print_jobs()
# job = scheduler.add_job(scheduled_email, 'interval', minutes=1, max_instances=1, id='my_job_id', replace_existing=True)
# scheduler.start()

app = Flask(__name__)

SECRET_KEY = os.environ['SECRET_KEY']
app.secret_key = SECRET_KEY
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def homepage():
    """View homepage."""
    if scheduler.running == False:
        scheduler.start()
    scheduler.print_jobs()

    if session.get('logged_in'):
        return redirect(f'/user/{session["current_user"]}/inventory')

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
        items = inventory.items
        items.sort(key=lambda item: item.name)

        return render_template('user-inventory.html', user=user, items=items)

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

@app.route('/delete-item', methods=['POST'])
def delete_item():

    print(request)
    content = request.get_json()
    print(content)
    name = content['name']
    quantity = content['quantity']
    expiration = content['expiration']

    item = crud.get_item_by_info(name=name, quantity=quantity, expiration_date=expiration)

    crud.delete_item(item)

    return jsonify('ITEM DELETED!')

# FIXME: Check for current_user in session before setting user to current_user in session
@app.route('/send-email')
def send_email():
    
    user = crud.get_user_by_id(session['current_user'])
    inventory = crud.get_first_inventory_for_user(user)

    expiring_items = crud.get_items_expiring(inventory, 30)

    html_list = []

    for item in expiring_items:
        html_list.append(f'''<tr>
                                <td>{item.name}</td>
                                <td>{item.quantity}</td>
                                <td>{item.expiration_date}</td>
                                <td>{item.date_added.strftime('%Y-%m-%d')}</td>
                            </tr>''')
    
    separator = ''
    htmlString = separator.join(html_list)

    mail_helper.send_email(htmlString)

    return 'Email test'

@app.route('/user/<user_id>/settings')
def settings(user_id):
    """View user settings page"""

    user = crud.get_user_by_id(user_id)
    return render_template('user-settings.html', user=user)

def send_scheduled_email(current_user):
    
    user = crud.get_user_by_id(current_user)
    inventory = crud.get_first_inventory_for_user(user)

    expiring_items = crud.get_items_expiring(inventory, 30)

    html_list = []

    for item in expiring_items:
        html_list.append(f'''<tr>
                                <td>{item.name}</td>
                                <td>{item.quantity}</td>
                                <td>{item.expiration_date}</td>
                                <td>{item.date_added.strftime('%Y-%m-%d')}</td>
                            </tr>''')
    
    separator = ''
    htmlString = separator.join(html_list)

    mail_helper.send_email(htmlString)

    print('Email sent.')

#FIXME: GET should lead to homepage/user inventory
@app.route('/schedule-report', methods=['POST'])
def schedule_report():
    """Schedules an automated email report for expiring items."""
    scheduler.print_jobs()
    current_user = session['current_user']
    email_frequency = int(request.form.get('email-frequency'))

    print(f'EMAIL FREQUENCY: {email_frequency}')
    if scheduler.running == True:
        scheduler.pause()
        job = scheduler.add_job(send_scheduled_email, 'interval', days=email_frequency, max_instances=1, id='my_job_id', replace_existing=True, kwargs= {'current_user': current_user}, jobstore='default')
        scheduler.resume()
    
    else:
        job = scheduler.add_job(send_scheduled_email, 'interval', days=email_frequency, max_instances=1, id='my_job_id', replace_existing=True, kwargs= {'current_user': current_user}, jobstore='default')
        scheduler.start()

    scheduler.print_jobs()

    return "Expiration report email scheduled!"

@app.route('/set-new-password', methods=['POST'])
def update_password():
    """Changes user password"""

    user = crud.get_user_by_id(session['current_user'])
    old_password = request.form.get('old-password')
    new_password = request.form.get('new-password')
    confirm_password = request.form.get('confirm-password')

    if old_password == user.password:
        if new_password == confirm_password:
            crud.update_user_password(user=user,new_password=new_password)
            flash('Password updated!')
        else:
            flash('New passwords do not match. Please try again.')
    else:
        flash('Incorrect password.  Please try again.')

    return redirect('/user/1/settings')

if __name__ == '__main__':
    app.debug = False
    DebugToolbarExtension(app)
    connect_to_db(app, 'hbcapstone')
    app.run(host='0.0.0.0', debug=True, use_reloader=False)