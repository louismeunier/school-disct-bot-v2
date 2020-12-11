from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from datetime import date
import json

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def cred():
    """
    The majority of the functionality of these functions was learned or copied from https://developers.google.com/calendar/quickstart/python
    The Google Calendar API can be pretty tricky to work with, so make sure your system is set up properly to use it
    """
    creds = None

    if os.path.exists('utils/calendar_api/token.pickle'):
        with open('utils/calendar_api/token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'utils/calendar_api/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('utils/calendar_api/token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds
    
def get_current_day():
    creds = cred()
    service = build('calendar', 'v3', credentials=creds)

    page_token = None
    while True:
      with open("secrets.json","r") as f:
        data = json.load(f)
      calendarID = data["OtherTokens"]["CalendarID"]
      f.close()
      events = service.events().list(calendarId=calendarID, pageToken=page_token).execute()
      for event in events['items']:
        try:
            if (str(date.today())==event["start"]["date"] and event["summary"][:20]=="High School Rotation"):
                return event["summary"][23:]
        except:
            pass
      page_token = events.get('nextPageToken')
      if not page_token:
        break

def get_upcoming_events(options):
    creds = cred()
    service = build('calendar', 'v3', credentials=creds)
    print(options)
    page_token = None
    with open("secrets.json","r") as f:
        data = json.loads(f)
    calendarID = data["OtherTokens"]["CalendarID"]
    f.close()
    while True:
      events = service.events().list(calendarId=calendarID, pageToken=page_token).execute()
      for event in reversed(events['items']):
        try:
            print(event['summary'])
            print(event["start"]["date"])
        except:
            pass
      page_token = events.get('nextPageToken')
      if not page_token:
        break

