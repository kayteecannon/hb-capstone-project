"""CRUD operations."""

from model import db, User, Inventory, Item, connect_to_db
from datetime import datetime

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

def create_item(inventory_id, name, quantity, date_added):
    """Create and return a new item."""

    inventory = Inventory.query.get(inventory_id)
    item = Item(inventory_id=inventory_id, name=name, quantity=quantity, date_added=date_added)

    inventory.items.append(item)

    db.session.add(item)
    db.session.commit()

    return item

def get_user_by_id(user_id):
    """Return user given user_id."""

    user = User.query.get(user_id)

    if user == None:
        print(f'No user found with id: {user_id}')

    return user

def get_inventory_by_id(inventory_id):
    """Return inventory given inventory_id."""

    inventory = Inventory.query.get(inventory_id)

    if inventory == None:
        print(f'No inventory found with id: {inventory_id}')

    return inventory

def get_item_by_id(item_id):
    """Return item given item_id."""
    item = Item.query.get(item_id)

    if item == None:
        print(f'No item found with id: {item_id}')

    return item

def get_items_from_inventory(inventory):
    """Return all items in given inventory."""

    items = Item.query.filter_by(inventory=inventory).all()

    return items


if __name__ == '__main__':
    from server import app
    connect_to_db(app, 'hb-capstone-db')
