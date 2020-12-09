from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from datetime import date

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def cred():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('calendar_api_things/token.pickle'):
        with open('calendar_api_things/token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'calendar_api_things/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('calendar_api_things/token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds
def get_current_day():
    creds = cred()
    service = build('calendar', 'v3', credentials=creds)
    #calendar_list_entry = service.calendarList().get(calendarId='9i14aufrnvmsalodjls87b1rrs@group.calendar.google.com').execute()

    #print(calendar_list_entry)
    # Call the Calendar API
    page_token = None
    while True:
      events = service.events().list(calendarId='9i14aufrnvmsalodjls87b1rrs@group.calendar.google.com', pageToken=page_token).execute()
      for event in events['items']:
        try:
            if (str(date.today())==event["start"]["date"] and event["summary"][:20]=="High School Rotation"):
                return event["summary"]
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

    while True:
      events = service.events().list(calendarId='9i14aufrnvmsalodjls87b1rrs@group.calendar.google.com', pageToken=page_token).execute()
      for event in reversed(events['items']):
        try:
            print(event['summary'])
            print(event["start"]["date"])
        except:
            pass
      page_token = events.get('nextPageToken')
      if not page_token:
        break

