import os
import requests
from ms_graph import generate_access_token, GRAPH_API_ENDPOINT

APP_ID = '82fbc472-d859-4baa-a0e5-2a30e64f1a38'
SCOPES = ['Files.ReadWrite']

access_token = generate_access_token(APP_ID, SCOPES)
headers = {
    'Authorization': 'Bearer' + access_token['access_token']
}

file_path = 'data.json'
file_name = os.path.basename(file_path)
with open(file_path, 'rb') as upload:
    media_client = upload.read()

response = requests.put(
    GRAPH_API_ENDPOINT + f'/me/drive/items/root:/{file_name}:/content',
    headers=headers,
    data=media_client
)

print(response.json())