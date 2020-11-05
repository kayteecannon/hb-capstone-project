from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """A user"""

    __tablename__ = 'users'

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    
    inventories = db.relationship('Inventory', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<User user_id: {self.user_id}, email: {self.email}>'

class Inventory(db.Model):
    """An inventory"""

    __tablename__ = 'inventories'

    inventory_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    title = db.Column(db.String, nullable=False)

    user = db.relationship('User')
    items = db.relationship('Item', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Inventory inventory_id: {self.inventory_id}, title: {self.title}>'

class Item(db.Model):
    """An item"""

    __tablename__ = 'items'

    item_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    inventory_id = db.Column(db.Integer, db.ForeignKey('inventories.inventory_id'), nullable=False)
    name = db.Column(db.String, nullable=False)
    category = db.Column(db.String)
    quantity = db.Column(db.Float, nullable=False)
    units = db.Column(db.String)
    expiration_date = db.Column(db.DateTime)
    date_added = db.Column(db.DateTime, nullable=False)

    inventory = db.relationship('Inventory')

    def __repr__(self):
        return f'<Item item_id: {self.item_id}, name: {self.name}>'

def connect_to_db(app, db_name):
    """Connect to database."""

    app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql:///{db_name}"
    app.config["SQLALCHEMY_ECHO"] = True
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = app
    db.init_app(app)

if __name__ == '__main__':
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app, 'hb-capstone-db')