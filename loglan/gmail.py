import httplib2
import os
import base64
import json

from apiclient import discovery
from email.mime.text import MIMEText
from email import encoders
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

from elearning.settings import BASE_DIR

flags = None


# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/gmail-python-quickstart.json
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.send']
CLIENT_SECRET_FILE = 'credentials/client_secret.json'
APPLICATION_NAME = 'Gmail API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = BASE_DIR
    credential_dir = os.path.join(home_dir, 'credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'gmail-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
           credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
           credentials = tools.run_flow(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def create_message(sender, to, subject, message_text):
  """Create a message for an email.

  Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.

  Returns:
    An object containing a base64url encoded email object.
  """
  message = MIMEText(message_text, 'html')
  msg = MIMEText(message_text, _subtype='octet-stream')
  message['to'] = to
  message['from'] = sender
  message['subject'] = subject

  return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}
  #return {'raw': encoders.encode_base64(message)}

def send_message(service, user_id, message):
  """Send an email message.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    message: Message to be sent.

  Returns:
    Sent Message.
  """
  #try:
  message = (service.users().messages().send(userId=user_id, body=message)
               .execute())
  print('Message Id: %s' % message['id'])
  return message
  #except as error:
   # print('An error occurred: %s' % error)
def main():
    """Shows basic usage of the Gmail API.

    Creates a Gmail API service object and outputs a list of label names
    of the user's Gmail account.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)

    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])

    message = create_message('loglan.gc@gmail.com', 'muhammadnizaryp@gmail.com', 'test subject', '<h1>Ini judul</h1><p>test_message</p>')
    send_message(service, 'me', message)

    print('sent message')


def send_mail_gmail(subject, message, from_email, to):
    """Shows basic usage of the Gmail API.

    Creates a Gmail API service object and outputs a list of label names
    of the user's Gmail account.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)

    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])

    message = create_message(from_email, to, subject, message)
    send_message(service, 'me', message)

    print('sent message')

if __name__ == '__main__':
    main()
