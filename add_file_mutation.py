import json
import requests

import cred
import Constants

headers = {
    "Authorization": cred.API_TOKEN
}

# apiQuery = 'mutation add_file($file: File!, $item: ID!) {add_file_to_column (item_id: $item, column_id:"files__1" file: $file) { id } }'
# apiMap = json.dumps({"file" : "variables.file", "item" : "variables.item_id"}).replace('"', '\\"')
payload = {
    'query': 'mutation ($file: File!) {add_file_to_column (file: $file,item_id: 7227992789, column_id:"files__1") {id}}'
}
files=[
('variables[file]',('filename',open('test.txt','rb'),'contenttype'))
]

response = requests.post(Constants.URL_FILE, headers=headers,  data=payload, files=files) 
print(response.status_code)
print(response.reason)