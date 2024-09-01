import httpx

import cred
import Constants
from update_link_column import update_link_column

# Headers including the API token
headers = {
    'Authorization': cred.API_TOKEN,
    'Content-Type': 'application/json'
}

# The board name you're searching for
board_name_to_find = 'test web hook 2'

workspace_id = 7582973
portfolio_board_id = 7163711212

# GraphQL query to find boards by name
query = """
{
  boards (workspace_ids: [%s]) {
    id
    name
    url
  }
}
""" % workspace_id

# Send the request to Monday.com API
response = httpx.post(Constants.URL, json={'query': query}, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()
    
    # Extract boards data
    # print(data)
    boards = data['data']['boards']

    # Filter boards by the desired name
    matching_boards = [board for board in boards if board['name'] == board_name_to_find]
    
    if matching_boards:
       board = matching_boards[0]
        #for board in matching_boards:
       print(f"Found board: {board['name']} (ID: {board['id']}) and URL: {board['url']}")

    #    Updating the link Column
       update_link_column(portfolio_board_id, 7337332192, "Project Link",  board["url"], board['name'])
    else:
        print(f"No board found with the name '{board_name_to_find}'.")
else:
    print(f"Failed to fetch boards: {response.status_code} {response.text}")
