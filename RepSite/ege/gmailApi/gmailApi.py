import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from bs4 import BeautifulSoup

from .Google import Create_Service


def requestForGmail(lastId):
    payments = []
    newLastId = None

    CLIENT_SECRET_FILE = 'credentials.json'
    API_NAME = 'gmail'
    API_VERSION = 'v1'
    SCOPES = ['https://mail.google.com/']

    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

    emailMsg = 'You won $100,000 again'
    mimeMessage = MIMEMultipart()
    mimeMessage['to'] = 'matvei.sergin2016@gmail.com'
    mimeMessage['subject'] = 'You won twice'
    mimeMessage.attach(MIMEText(emailMsg, 'plain'))
    raw_string = base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()

    result = service.users().messages().list(userId='me').execute()
    messages = result.get('messages')

    # messages is a list of dictionaries where each dictionary contains a message id.

    # iterate through all the messages
    flag = True # old message
    for msg in messages:
        # Get the message from its id
        txt = service.users().messages().get(userId='me', id=msg['id']).execute()

        if txt['id'] != lastId and flag:
            continue
        else:
            flag = False #get last message
            print('Find!')

        if txt['payload']['headers'][0]['value'] == 'sms.receiver23@gmail.com' \
                and 'ECMC4170' in txt['snippet'] and 'Перевод' in txt['snippet'] \
                and lastId != txt['id']:
            text = txt['snippet']
            text = text[ text.index('Соообщение:') + 12 : ]
            summ = text[23: text[23:].index(' ') + 22]
            sender = text[text[text.index('от'):].index(' ') + 1 + text.index('от'): text.index('Баланс') - 2]

            newLastId = txt['id']
            payments += [(summ, sender, txt['id'])]

    return payments, newLastId
