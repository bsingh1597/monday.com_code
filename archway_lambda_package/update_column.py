import httpx
import json

import cred
import Constants

# Headers including the API token
headers = {
    'Authorization': cred.API_TOKEN,
    'Content-Type': 'application/json'
}

def update_column(board_id, item_id, column_name, value, project_name="", is_link=False):
    # print(f"Column Value: {value}")
    # IDs for the board, item, and column
    column_id, column_type = retieve_column_info(board_id, column_name)

    if is_link:
        value = json.dumps({
        "url": value,
        "text": project_name
        }).replace('"', '\\"')
    
    match column_type:
        case 'text':
           value = f'"{value}"'.replace('"', '\\"')

    # GraphQL mutation to update the column value
    mutation = """
        mutation {
        change_column_value(
        board_id: %s,
        item_id: %s,
        column_id: "%s",
        value: "%s"
        ) {
        id
        }
    }
    """ % (board_id, item_id, column_id, value)

    # Send the request to Monday.com API
    response = httpx.post(Constants.URL, json={'query': mutation}, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        # Print response from Monday.com
        print(f"Response: {data}")
    else:
        print(f"Failed to update column: {response.status_code} {response.text}")

def retieve_column_info(board_id, column_name):
    # GraphQL query to get columns for the specified board
    retrieve_columns_query = """
    {
    boards(ids: [%s]) {
        columns {
        id
        title
        type
        }
    }
    }
    """ % board_id

    # Send the request to Monday.com API
    response = httpx.post(Constants.URL, json={'query': retrieve_columns_query}, headers=headers)
    column_id = None
    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        
        # Extract column data
        columns = data['data']['boards'][0]['columns']
        
        # Find the column ID based on the column name
        for column in columns:
            if column['title'] == column_name:
                column_id = column['id']
                column_type = column['type']
                break
        
        print(f"Column ID: {column_id}")
    else:
        print(f"Failed to retrieve columns: {response.status_code} {response.text}")
    return column_id, column_type
    
def fecth_workspace_id_from_board(board_id):
    # GraphQL query to get the workspace ID from the board
    query = """
    { boards(ids: %s) {
        workspace {
        id
        name
        }
    }
    }""" % board_id
    workspace_id = None
    
    response = httpx.post(Constants.URL, json={'query': query}, headers=headers)

    if response.status_code == 200:
        data = response.json()
        workspace_id = data['data']['boards'][0]['workspace']['id']
        print(f"Workspace ID: {workspace_id}")
    else:
        print(f"Failed to fetch workspace ID: {response.status_code} {response.text}")

    return workspace_id

def fecth_board_id_by_name(board_name, workspace_id):
    board = None
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
        matching_boards = [board for board in boards if board['name'] == board_name]
        
        if matching_boards:
           board = matching_boards[0]
            #for board in matching_boards:
           print(f"Found board: {board['name']} (ID: {board['id']}) and URL: {board['url']}")
    else:
        print(f"Failed to fetch boards: {response.status_code} {response.text}")
        
    return board