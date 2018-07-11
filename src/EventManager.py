##!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import client, tools
from Credentials import getCredentials
import datetime, logging

def getUpcomingEvents(service, number_of_events, timeMin, calendarId='primary'):
    """
        Get upcoming events starting the current day.

            x Input :
                - number_of_events : number of events to get
                - timeMin : date for the beginning of the first event
                - calendarId : calendar you want to look up
            x Output : dict containing the events
    """
    logging.info("Getting the next %d upcoming events in your calendar ...")
    events_result = service.events().list(calendarId=calendarId, timeMin=timeMin,
                                      maxResults=number_of_events, singleEvents=True,
                                      orderBy='startTime', showDeleted=True).execute()
    events = events_result.get('items', [])
    print(len(events), " events were found in : ", calendarId)
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])
    return events


def addEvent(service, event):
    """
        Adding an event to your calendar.
    """
    event = service.events().insert(calendarId='primary', body=event).execute()
    #logging.info('Event created: %s' % (event.get('htmlLink')))
    print('Event created: %s' % (event.get('htmlLink')))


def updateEventTitle(service, eventId, summary):#, NEW_EVENT):
    """
        Update the name of an existing event.
    """
    event = service.events().get(calendarId='primary', eventId=eventId).execute()
    event['summary'] = summary
    updated_event = service.events().update(calendarId='primary', eventId=event['id'], body=event).execute()
    logging.info('Event updated: %s' % (event.get('htmlLink')))


def updateEventDate(service, eventId, startDate, endDate):
    """
        Update the date of an existing event.
    """
    event = service.events().get(calendarId='primary', eventId=eventId).execute()
    event['start']['dateTime'] = startDate
    event['end']['dateTime'] = endDate
    updated_event = service.events().update(calendarId='primary', eventId=event['id'], body=event).execute()
    logging.info('Event updated: %s' % (event.get('htmlLink')))

def addEventProperty(service, eventId, value, property, calendarId='primary'):
    """
        Add a property to an event.
    """
    event = service.events().get(calendarId=calendarId, eventId=eventId).execute()
    event[property] = value
    updated_event = service.events().update(calendarId=calendarId, eventId=event['id'], body=event).execute()
    logging.info(updated_event['updated'])

def deleteEvent(service, eventId):
    """
        Delete an event from your calendar.
    """
    event = service.events().get(calendarId='primary', eventId=eventId).execute()
    deleted_event = service.events().delete(calendarId='primary', eventId=event['id']).execute()
    logging.info('Event deleted: %s' % (event.get('htmlLink')))


if __name__ == '__main__':
    SCOPES = 'https://www.googleapis.com/auth/calendar'
    CREDENTIAL_PATH = '../credentials/client_secret.json'
    credentials = getCredentials(CREDENTIAL_PATH) #insert your client_secret.json file path
    service = build('calendar', 'v3', http=credentials.authorize(Http()))
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
