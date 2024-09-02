import httpx
import json

import cred
import Constants

# Headers including the API token
headers = {
    'Authorization': cred.API_TOKEN,
    'Content-Type': 'application/json'
}

def update_link_column(board_id, item_id, column_name, value, project_name):
    print(value)
    # IDs for the board, item, and column
    column_id = retieve_column_id(board_id, column_name)

    link_value = json.dumps({
    "url": value,
    "text": project_name
    }).replace('"', '\\"')

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
    """ % (board_id, item_id, column_id, link_value)

    # Send the request to Monday.com API
    response = httpx.post(Constants.URL, json={'query': mutation}, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        # Print response from Monday.com
        print(f"Response: {data}")
    else:
        print(f"Failed to update column: {response.status_code} {response.text}")

def retieve_column_id(board_id, column_name):
    # GraphQL query to get columns for the specified board
    retrieve_columns_query = """
    {
    boards(ids: [%s]) {
        columns {
        id
        title
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
                break
        
        print(f"Column ID: {column_id}")
    else:
        print(f"Failed to retrieve columns: {response.status_code} {response.text}")
    return column_id
    
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