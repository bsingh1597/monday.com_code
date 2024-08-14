import requests
import json

import cred

BOARD_ID = '7198467067'

# Define the URL and headers for the request
url = "https://api.monday.com/v2"
headers = {
    "Authorization": cred.API_TOKEN,
    "Content-Type": "application/json"
}

# Define the column values for the item
column_values = {
    'text_1__1':'H-184',  # Replace with your text column ID and value
    "status": {"label": "Completed"},  
    "dropdown__1": {"ids": [73]},  # Replace with your dropdown column ID and the list of IDs
    "dropdown1__1": {"ids": [12, 13, 14]},  # Replace with your dropdown column ID and the list of IDs
    # "date_column": "2024-08-12"  # Replace with your date column ID and value (YYYY-MM-DD format)
}

item_name = "Hart Botanical Garden Brochure"

# Convert the dictionary to a JSON string and Escape the JSON string for GraphQL
column_values_json = json.dumps(column_values).replace('"', '\\"')

# Define the query to create an item with multiple column values
query = """
mutation {
  create_item (
    board_id: %s,
    item_name: "%s",
    column_values: "%s"
  ) {
    id
  }
}
""" % (BOARD_ID, item_name, column_values_json)  #to covert into json

# Make the POST request to the Monday.com API
response = requests.post(url, headers=headers, json={"query": query})

# Print the response from the server
print(response.json())
