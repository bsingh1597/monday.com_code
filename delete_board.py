import httpx

import cred
import Constants

board_id = 7340465545

# Headers including the API token
headers = {
    'Authorization': cred.API_TOKEN,
    'Content-Type': 'application/json'
}

# GraphQL mutation to delete the board
mutation = """
mutation {
  delete_board (board_id: %s) {
    id
  }
}
""" % board_id

# Send the request to Monday.com API
response = httpx.post(Constants.URL, json={'query': mutation}, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    print("Board deleted successfully.")
else:
    print(f"Failed to delete board: {response.status_code} {response.text}")
