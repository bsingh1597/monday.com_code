import requests

import cred
import Constants


# Board ID for which you want to get the workspace ID
board_id = 7340225471

# Headers including the API token
headers = {
    'Authorization': cred.API_TOKEN,
    'Content-Type': 'application/json'
}

# GraphQL query to get the workspace ID from the board
query = """
    {
    boards(ids: %s) {
        workspace {
        id
        name
        }
    }
    }""" % board_id

# Send the request to Monday.com API
response = requests.post(Constants.URL, json={'query': query}, headers=headers)

workspace_id = None
    
response = requests.post(Constants.URL, json={'query': query}, headers=headers)

if response.status_code == 200:
    data = response.json()
    print(data)
    workspace_id = data['data']['boards'][0]['workspace']['id']
    print(f"Workspace ID: {workspace_id}")
else:
    print(f"Failed to fetch workspace ID: {response.status_code} {response.text}")
