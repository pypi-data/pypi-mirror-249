import sys
sys.path.append('src')
from python_bring_api.bring import Bring

# Create Bring instance with email and password
bring = Bring("e.ball227@gmail.com", "SHSFJvKNOA*U4a5")
# Login
bring.login()

# Get information about all available shopping lists
lists = bring.loadLists()['lists']

# Save an item with specifications to a certain shopping list
bring.saveItem(lists[0]['listUuid'], 'Milk', 'low fat')

# Get all the items of a list
items = bring.getItems(lists[0]['listUuid'])
print(items['purchase']) # [{'specification': 'low fat', 'name': 'Milk'}]

# Get all item details of a list
bring.getAllItemDetails(lists[0]['listUuid'])

# Update an item in a list
bring.updateItem(lists[0]['listUuid'], 'Milk', 'high fat')

# Remove an item from a list
bring.removeItem(lists[0]['listUuid'], 'Milk')