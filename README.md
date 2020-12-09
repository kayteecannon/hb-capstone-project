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
* HTML
* CSS
* Bootstrap

## Installation

1. Clone project:

```
$ git clone https://github.com/kayteecannon/hb-capstone-project.git
```

2. Inside your project directory, create a virtual environment:

```
$ virtualenv env
```

3. Activate virtual environment:

```
$ source env/bin/activate
```

4. Install required libraries using pip:

```
$ pip install -r requirements.txt
```

5. Create a PostgreSQL database:

```
$ createdb hbcapstone
```

6. Run model.py file interactively to create database tables:

```
$ python3 -i model.py
>>> db.create_all()
```