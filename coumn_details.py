import requests
import cred

BOARD_ID = '7198467067'

# Define the URL and headers for the request
url = "https://api.monday.com/v2"
headers = {
    "Authorization": cred.API_TOKEN,
    "Content-Type": "application/json"
}

# Define the query to fetch column names and descriptions (types)
query = """
{
  boards (ids: %s) {
    columns {
      id
      title
      type
    }
  }
}
""" % BOARD_ID

# Make the POST request to the Monday.com API
response = requests.post(url, headers=headers, json={"query": query})

# Print the response from the server
data = response.json()
columns = data['data']['boards'][0]['columns']

# Display the column names and types
for column in columns:
    print(f"Column ID: {column['id']}, Title: {column['title']}, Type: {column['type']}")
