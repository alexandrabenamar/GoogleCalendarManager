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


def getAllCalendars(service):
    """
        Get calendars informations : id and summary
            x Output : list of calendars
    """
    page_token = None

    calendars = (service.calendarList()
                        .list(pageToken = page_token).execute())

    for calendar in calendars['items']:
        print(calendar.get('id', None), '|', calendar.get('summary', None))

    return calendars


def clearCalendar(service):
    """
        Clear the principal calendar only.
    """
    cleared_calendar = service.calendars().clear(calendarId='primary').execute()
    logging.info('Calendar cleared')


def deleteCalendar(service, calendarId):
    """
        Delete a calendar from a Google Calendar list.
        Note : does not work with the principal calendar, use clearCalendar() instead.
    """
    deleted_calendar = service.calendars().delete(calendarId=calendarId).execute()
    logging.info('Calendar %s deleted' % (calendarId))


if __name__ == '__main__':
    SCOPES = 'https://www.googleapis.com/auth/calendar'
    credentials = getCredentials(CREDENTIAL_PATH)
    service = build('calendar', 'v3', http=credentials.authorize(Http()))
    #perform actions
