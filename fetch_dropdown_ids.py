import requests
import json
import csv

import cred
import Constants


BOARD_ID = '7198467067'
DROPDOWN_COLUMN_ID = 'dropdown__1'  # Replace with your dropdown column ID

headers = {
    "Authorization": cred.API_TOKEN,
    "Content-Type": "application/json"
}

# Define the query to fetch the dropdown column details
query = """
{
  boards (ids: %s) {
    columns (ids: "%s") {
      id
      title
      type
      settings_str
    }
  }
}
""" % (BOARD_ID, DROPDOWN_COLUMN_ID)

# Make the POST request to the Monday.com API
response = requests.post(Constants.URL, headers=headers, json={"query": query})

# Print the response from the server
data = response.json()
column_data = data['data']['boards'][0]['columns'][0]

# Extract the dropdown options from the settings_str field
dropdown_options = json.loads(column_data['settings_str'])

print(f"{dropdown_options}")

# Print out the options and their IDs
# for dict in dropdown_options['labels']:
#     for id, name in dict.items():
#             print(f"ID: {name}")
#     print("")
        
csv_file = "../counties.csv"
with open(csv_file, mode='w',newline='') as file:
    writer = csv.DictWriter(file, fieldnames=['id','name'])
    writer.writeheader
    writer.writerows(dropdown_options['labels'])


with open(csv_file) as file:
    print(file.read())