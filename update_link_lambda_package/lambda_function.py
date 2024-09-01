import json
import httpx
from update_link_column import update_link_column

import cred
import Constants

def lambda_handler(event, context):

    # print("Received event:", json.dumps(event))
    webhook_payload = event["event"]
    print(webhook_payload["pulseName"])
    # *****Name of the new project created
    board_name_to_find = webhook_payload["pulseName"]
    portfolio_item_id = webhook_payload["pulseId"]
    # *****Current workspace - no in Event
    workspace_id = 7582973
    portfolio_board_id = webhook_payload["boardId"]
        
    # Headers including the API token
    headers = {
        'Authorization': cred.API_TOKEN,
        'Content-Type': 'application/json'
    }
    
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
    
    # Fecth the boards information in the workspace
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
           update_link_column(portfolio_board_id, portfolio_item_id, "Project Link",  board["url"], board['name'])
        else:
            print(f"No board found with the name '{board_name_to_find}'.")
    else:
        print(f"Failed to fetch boards: {response.status_code} {response.text}")
        
    return {"status_code":200}
