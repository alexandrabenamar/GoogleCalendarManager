##!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import client, tools
import datetime
import logging
from Credentials import getCredentials

def createCalendar(service, calendar):
    """
        Creates a secondary calendar
    """
    created_calendar = service.calendars().insert(body=calendar).execute()
    print(created_calendar['id'], '|', created_calendar['summary'])


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
    CREDENTIAL_PATH = '../credentials/client_secret.json'
    credentials = getCredentials(CREDENTIAL_PATH) #insert your client_secret.json file path
    service = build('calendar', 'v3', http=credentials.authorize(Http()))
    #perform actions
    getAllCalendars(service)
