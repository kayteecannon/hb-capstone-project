# Fill Me Inventory

Fill Me Inventory is a web application that assists users with both emergency preparedness and everyday life.  Fill Me Inventory allows users to build an inventory of items, including quantities and expiration dates.  Along with the ability to add, edit, and delete items, users are also able to schedule regularly occurring emails that notify them of soon-to-expire items.  This allows the user to better manage their inventory and prevent waste.

## Tech Stack
* PostgreSQL
* SQLAlchemy
* Python
* Flask
* Jinja
* JavaScript
* jQuery
* AJAX
* Twilio SendGrid Email API
* APScheduler
* HTML
* CSS
* Bootstrap

## Installation

1. **Clone project:**

```
$ git clone https://github.com/kayteecannon/hb-capstone-project.git
```

2. **Inside your project directory, create a virtual environment:**

```
$ virtualenv env
```

3. **Activate virtual environment:**

```
$ source env/bin/activate
```

4. **Install required libraries using pip:**

```
$ pip3 install -r requirements.txt
```

5. **Create a PostgreSQL database:**

```
$ createdb hbcapstone
```

6. **Run model.py file interactively to create database tables:**

```
$ python3 -i model.py
>>> db.create_all()
```

7. **Create a secrets.sh file to hold:**
* Flask app secret key
* Twilio SendGrid Email API key
* Environmental variables for testing SendGrid API, to be replaced later

```
$ touch secrets.sh
```
IMPORTANT: DO NOT COMMIT secrets.sh file! Add secrets.sh file to .gitignore 

secrets.sh file will contain:
```
export SECRET_KEY='your secret key here'
export SENDGRID_API_KEY='your api key here'
export FROM_EMAIL_TEST='your test from email address here'
export TO_EMAIL_TEST='your test to email address here'
```

To access secrets.sh variables, inside project directory, run:
```
$ source secrets.sh
```

8. **To run Fill Me Inventory locally, inside project directory run:**
```
$ python3 server.py
```

Then, open web browser to localhost:5000


## Current Features (Version 1.0)

* User registration
* User log in
* Inventory
* Expiration report
* Add Item
* Edit/Delete Item
* Settings page
    * Schedule email
    * Change password

## Acknowledgments

Homepage image by [Annie Spratt](https://unsplash.com/@anniespratt)
Background textures from [Subtle Patterns by Toptal](https://www.toptal.com/designers/subtlepatterns/)