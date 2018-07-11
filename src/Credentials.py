##!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import print_function
from oauth2client.file import Storage

def getCredentials(file):
    """
        Get user credentials from Google Calendar API
        For more informations, go to :
            https://developers.google.com/calendar/quickstart/python

            x Input : json secret client file obtained with GC API
            X Output : the obtained credentials
    """
    store = Storage('credentials.json')
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(file, SCOPES)
        credentials = tools.run_flow(flow, store)
    return credentials

if __name__ == '__main__':
    SCOPES = 'https://www.googleapis.com/auth/calendar'
    CREDENTIAL_PATH = '../credentials/client_secret.json'
    credentials = getCredentials(CREDENTIAL_PATH) #insert your client_secret.json file path
