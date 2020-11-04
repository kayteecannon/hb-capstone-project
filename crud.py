"""CRUD operations."""

from model import db, User, Inventory, Item, connect_to_db


def create_user(email, password):
    """Create and return a new user."""

    user = User(email=email, password=password)

    db.session.add(user)
    db.session.commit()

    return user

def create_inventory(user_id, title):
    """Create and return a new inventory."""

    user = User.query.get(user_id)
    inventory = Inventory(user_id=user_id, title=title)
    
    user.inventories.append(inventory)

    db.session.add(inventory)
    db.session.commit()

    return inventory

if __name__ == '__main__':
    from server import app
    connect_to_db(app, 'hb-capstone-db')
