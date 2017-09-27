'''
Copyright 2017 Google Inc.
Modifications copyright 2017 Inovex GmbH

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

import mailbox
import os
import httplib2
from apiclient import errors

from oauth2client.file import Storage
from oauth2client import client
from oauth2client import tools
from apiclient import discovery

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None





class Extract:

    already_loaded_googleids = set()

    def fromMbox(self, location):
        return mailbox.mbox(location)


    def fromGmail(self, client_secret_file, credentials):

        credentials = self.get_credentials(client_secret_file=client_secret_file, credential_dir=credentials)

        http = credentials.authorize(httplib2.Http())
        service = discovery.build('gmail', 'v1', http=http)

        available_messageIDs = self.get_messageIDs(service)

        # to debug only use a subset of the messages for a way faster parsing
        #available_messageIDs = available_messageIDs[:5]

        newIDs = []

        #load only the not yet loaded messages
        for aid in available_messageIDs:
            if aid not in self.already_loaded_googleids:
                self.already_loaded_googleids.add(aid)
                newIDs.append(aid)

        messages = self.get_messages(service, newIDs)
        return messages


    def get_messages(self, service, messageIDs):

        """
        :param service: gmail service
        :param messageIDs: all the ids of the emails that should be downloaded
        :return: a list of emails
        """

        messages = []
        try:
            for id in messageIDs:
                message = service.users().messages().get(userId='me', id=id, format='raw').execute()
                messages.append(message)

        except errors.HttpError, error:
            print 'An error occurredduring the loading of the messagnes: %s' % error

        return messages

    def get_messageIDs(self, service):
        """
        :param service: gemail service
        :return: all the messageids from the user
        """

        response = service.users().messages().list(userId='me').execute()

        messageIDs = []
        if 'messages' in response:
            for item in response['messages']:
                messageIDs.append(item['id'])

        while 'nextPageToken' in response:
            page_token = response['nextPageToken']
            response = service.users().messages().list(userId='me', pageToken=page_token).execute()
            for item in response['messages']:
                messageIDs.append(item['id'])

        return messageIDs


    def get_credentials(self, client_secret_file, credential_dir):
        SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
        APPLICATION_NAME = 'newsflash-loader'

        """Gets valid user credentials from storage.

        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.

        Returns:
            Credentials, the obtained credential.
        """

        if credential_dir is None:
            credential_dir = os.path.join(".", 'credentials')


        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)

        credential_path = os.path.join(credential_dir,
                                       'newsflash-loader-credentials.json')



        store = Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            print "No credentials or credentials invalid"
            flow = client.flow_from_clientsecrets(client_secret_file, SCOPES)
            flow.user_agent = APPLICATION_NAME

            if flags:
                credentials = tools.run_flow(flow, store, flags)
            else: # Needed only for compatibility with Python 2.6
                credentials = tools.run(flow, store)


            print('Storing credentials to ' + credential_path)
        return credentials
