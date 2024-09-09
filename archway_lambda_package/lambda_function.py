import json
import httpx
from update_column import update_column, fecth_workspace_id_from_board, fecth_board_id_by_name

import cred
import Constants

def lambda_handler(event, context):
    if("challenge") in event:
        print("challenge payload")
        return event
    else:
        # print("Received event:", json.dumps(event))
        webhook_payload = event["event"]
        print(webhook_payload["pulseName"])
        # *****Name of the new project created
        project_name = webhook_payload["pulseName"]
        portfolio_item_id = webhook_payload["pulseId"]
        # *****Current workspace - Archway Workspace
        workspace_id = fecth_workspace_id_from_board(board_id=webhook_payload["boardId"])
        portfolio_board_id = webhook_payload["boardId"]
            
        board = fecth_board_id_by_name(project_name,workspace_id)
        
        if board is not None:
            #    Updating the link Column
            update_column(portfolio_board_id, portfolio_item_id, "Project Link",  board["url"], board['name'], True)
            #   Update the Project Board Id column
            update_column(portfolio_board_id, portfolio_item_id, "Project Board Id",  board["id"])
        else:
            print(f"No board found with the name '{project_name}'.")
            
        return {"status_code":200}

def delete_board_handler(event, context):
    print(event)
    if("challenge") in event:
        print("challenge payload")
        return event
    else:
        webhook_payload = event["event"]
        project_name = webhook_payload["itemName"]
        workspace_id = fecth_workspace_id_from_board(board_id=webhook_payload["boardId"])
        board = fecth_board_id_by_name(project_name,workspace_id)

        if board is not None:
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
            """ % board["id"]

            # Send the request to Monday.com API
            response = httpx.post(Constants.URL, json={'query': mutation}, headers=headers)

            # Check if the request was successful
            if response.status_code == 200:
                print("Board deleted successfully.")
            else:
                print(f"Failed to delete board: {response.status_code} {response.text}")
        else:
            print(f"No board found with the name '{project_name}'.")

        return {"status_code":200}