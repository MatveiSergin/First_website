import webbrowser
import requests
import msal
from urllib.parse import urlparse
from msal import PublicClientApplication
APPLICATION_ID = '82fbc472-d859-4baa-a0e5-2a30e64f1a38'
CLIENT_SECRET = '1XR8Q~EM84QZhaRKqc4B~a5d7VptJMfN3vWt8cjq'

base_url = 'https://graph.microsoft.com/v1.0/'
endpoint = base_url + 'me'
authority_url = 'https://login.microsoftonline.com/consumers/'

SCOPES = [
    'User.Read',
    'User.Export.All',
]

clients_instance = msal.ConfidentialClientApplication(
    client_id=APPLICATION_ID,
    client_credential=CLIENT_SECRET,
    authority=authority_url
)

authorization_request_url = clients_instance.get_authorization_request_url(SCOPES)
webbrowser.open(authorization_request_url, new=True)

#print(urlparse(authorization_request_url), '\n', authorization_request_url)
authorization_code = 'M.C106_BAY.2.3db03cd5-2110-38c0-034b-15baa94ab86e'

access_token = clients_instance.acquire_token_by_authorization_code(
    code=authorization_code,
    scopes=SCOPES,
)
print(access_token)
access_token_id = access_token['access_token']
headers = {'Authorization': 'Beaner' + access_token_id}

response = requests.get(endpoint, headers=headers)
print(response.json())

