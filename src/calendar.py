##!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import client, tools
from oauth2client.file import Storage
import datetime
import logging

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


def getUpcomingEvents(service, number_of_events, timeMin):
    """
        Get upcoming events starting the current day.

            x Input :
                - service : calendar
                - number_of_events : number of events to get
                - timeMin : date for the beginning of the first event
            x Output : dict containing the events
    """
    logging.info("Getting the next %d upcoming events in your calendar ...")
    events_result = service.events().list(calendarId='primary', timeMin=timeMin,
                                      maxResults=number_of_events, singleEvents=True,
                                      orderBy='startTime', showDeleted=True).execute()
    events = events_result.get('items', [])
    print(len(events), " events were found in your calendar")
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])
    return events

def addEvent(service, event):
    """
        Adding an event to your calendar.
    """
    event = service.events().insert(calendarId='primary', body=event).execute()
    print('Event created: %s' % (event.get('htmlLink')))

def updateEventTitle(service, eventId, summary):#, NEW_EVENT):
    """
        Update the name of an existing event.
    """
    event = service.events().get(calendarId='primary', eventId=eventId).execute()
    event['summary'] = summary
    updated_event = service.events().update(calendarId='primary', eventId=event['id'], body=event).execute()
    print(updated_event['updated'])


def updateEventDate(service, eventId, startDate, endDate):
    """
        Update the date of an existing event.
    """
    event = service.events().get(calendarId='primary', eventId=eventId).execute()
    event['start']['dateTime'] = startDate
    event['end']['dateTime'] = endDate
    updated_event = service.events().update(calendarId='primary', eventId=event['id'], body=event).execute()
    print(updated_event['updated'])
    print('Event updated: %s' % (event.get('htmlLink')))


if __name__ == '__main__':
    SCOPES = 'https://www.googleapis.com/auth/calendar'
    credentials = getCredentials('../credentials/client_secret.json')
    service = build('calendar', 'v3', http=credentials.authorize(Http()))
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    #events = getUpcomingEvents(service, 10, now)
    GMT_OFF = '+02:00'
    event = {
        'id': 'testconc',
        'summary': 'Concert à Bercy',
        'start':   {'dateTime': '2018-07-02T04:00:00%s' % GMT_OFF},
        'end':     {'dateTime': '2018-07-02T09:00:00%s' % GMT_OFF},
    }
    addEvent(service, event)
    updateEventTitle(service, 'testconc', 'Concert à ciel ouvert')
    updateEventDate(service, 'testconc', '2018-07-02T08:00:00+02:00', '2018-07-02T10:00:00+02:00')
