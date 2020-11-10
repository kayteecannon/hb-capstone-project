"""CRUD operations."""

from model import db, User, Inventory, Item, connect_to_db
from datetime import datetime

#
# Create functions
#
def create_user(email, password):
    """Create and return a new user."""

    user = User(email=email, password=password, date_added=datetime.now(), last_updated_on=datetime.now())

    db.session.add(user)
    db.session.commit()

    return user

def create_inventory(user_id, title):
    """Create and return a new inventory."""

    user = User.query.get(user_id)
    inventory = Inventory(user_id=user_id, title=title, date_added=datetime.now(), last_updated_on=datetime.now())
    
    user.inventories.append(inventory)

    db.session.add(inventory)
    db.session.commit()

    return inventory

def create_item(inventory_id, name, quantity):
    """Create and return a new item."""

    inventory = Inventory.query.get(inventory_id)
    item = Item(inventory_id=inventory_id, name=name, quantity=quantity, date_added=datetime.now(), last_updated_on=datetime.now())

    inventory.items.append(item)

    db.session.add(item)
    db.session.commit()

    return item

#
# Read functions
#
def get_user_by_id(user_id):
    """Return user given user_id."""

    user = User.query.get(user_id)

    if user == None:
        print(f'No user found with id: {user_id}')

    return user

def get_user_by_email(email):
    """Return user give email."""

    user = User.query.filter_by(email=email).one()
    
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

def get_inventories_for_user(user):
    """Return all inventories for given user."""

    inventories = Inventory.query.filter_by(user=user).all()

    return inventories

def get_first_inventory_for_user(user):
    """Return first inventory for given user."""

    inventory = Inventory.query.filter_by(user=user).first()

    return inventory

def get_all_items_for_user(user):
    """Return a list of all items for given user."""

    all_items = []
    inventories = get_inventories_for_user(user)

    for inventory in inventories:
        items = get_items_from_inventory(inventory)
        all_items += items

    return all_items

#
# Update functions
#

def update_item_quantity(item, quantity):
    """Update quantity of given item."""

    item.quantity = quantity
    item.last_updated_on = datetime.now()

    db.session.commit()

    print(f'Item quantity updated: name: {item.name}, qty: {quantity}')

def update_item_name(item, name):
    """Update name of given item."""

    item.name = name
    item.last_updated_on = datetime.now()

    db.session.commit()

    print(f'Item name updated: item_id: {item.item_id}, name: {name}')

def update_inventory_title(inventory, title):
    """Update title of given inventory."""

    inventory.title = title
    inventory.last_updated_on = datetime.now()

    db.session.commit()

    print(f'Inventory title updated: inventory_id: {inventory.inventory_id}, title: {title}')

#
# Delete functions
#
def delete_item(item):
    """Delete given item from database."""

    print(f'Deleting item: {item}')

    db.session.delete(item)
    db.session.commit()

def delete_inventory(inventory):
    """Delete given inventory from database. Cascade deletes all items within inventory."""

    print(f'Deleting inventory: {inventory}')

    db.session.delete(inventory)
    db.session.commit()

def delete_user(user):
    """Delete given user from database. Cascade deletes all inventories of user."""

    print(f'Deleting user: {user}')

    db.session.delete(user)
    db.session.commit()

if __name__ == '__main__':
    from server import app
    connect_to_db(app, 'hbcapstone')
