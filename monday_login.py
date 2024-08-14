import requests

import cred

apiUrl = "https://api.monday.com/v2"
headers = {"Authorization" : cred.API_TOKEN}

query = '''{ boards (ids: 6983341020 items) 
            {
                name
                items_page {
                items {
                    id
                    name
                        }
                url 
            }
            }'''

data = {'query' : query}

r = requests.post(url=apiUrl, json=data, headers=headers) # make request
print(r.json())