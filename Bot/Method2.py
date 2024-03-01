import webbrowser

import requests
from msal import PublicClientApplication
APPLICATION_ID = '82fbc472-d859-4baa-a0e5-2a30e64f1a38'
CLIENT_SECRET = '1XR8Q~EM84QZhaRKqc4B~a5d7VptJMfN3vWt8cjq'

base_url = 'https://graph.microsoft.com/v1.0/'
endpoint = base_url + 'me'
authority_url = 'https://login.microsoftonline.com/consumers/'

SCOPES = [
    'User.Read',
]

app = PublicClientApplication(
    APPLICATION_ID,
    authority=authority_url,

)

accounts = app.get_accounts()

#if accounts:
#    app.acquire_token_silent(scopes=SCOPES, account=accounts[0])

flow = app.initiate_device_flow(scopes=SCOPES)
print(flow)
print(flow['message'])
webbrowser.open(flow['verification_uri'])

result = app.acquire_token_by_device_flow(flow)

access_token_id = result['access_token']
headers = {'Authorization': 'Beaner' + access_token_id}

response = requests.get(endpoint, headers=headers)
print(response)
print(1, response.json())