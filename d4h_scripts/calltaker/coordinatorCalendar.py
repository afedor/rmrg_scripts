import datetime
import sys
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

class CoordinatorCalendar:

  def __init__(self):
    self.calendarId = 0
    self.events = []

  def authenticate(self):
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(sys.path[0] + "/token.json"):
      creds = Credentials.from_authorized_user_file(sys.path[0] + "/token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
      if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
      else:
        flow = InstalledAppFlow.from_client_secrets_file(
            "credentials_private.json", SCOPES
        )
        creds = flow.run_local_server(port=0)
      # Save the credentials for the next run
      with open(sys.path[0] + "/token.json", "w") as token:
        token.write(creds.to_json())
    self.service = build("calendar", "v3", credentials=creds)

  def getCalendarId(self):
    page_token = None
    calendarId = 0
    while True:
      calendar_list = self.service.calendarList().list(pageToken=page_token).execute()
      for calendar_list_entry in calendar_list['items']:
        if calendar_list_entry['summary'] == 'Calltaker Schedule':
          calendarId = calendar_list_entry['id']
      page_token = calendar_list.get('nextPageToken')
      if not page_token:
        break
    return calendarId
    
  def grabEvents(self, theCalendarId):
    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
    events_result = (
        self.service.events()
        .list(
            calendarId=theCalendarId,
            timeMin=now,
            maxResults=10,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    events = events_result.get("items", [])

    if not events:
      return []
    self.events = events

  def getCoordinatorForDate(self, thedate):
    if self.calendarId == 0:
      self.authenticate()
      self.calendarId = self.getCalendarId()
      self.grabEvents(self.calendarId)

    coordinator=""
    for event in self.events:
      startStr = event["start"].get("dateTime", event["start"].get("date"))
      startDate = datetime.datetime.strptime(startStr, '%Y-%m-%d')
      endStr = event["end"].get("dateTime", event["end"].get("date"))
      endDate = datetime.datetime.strptime(endStr, '%Y-%m-%d')
      if thedate >= startDate and thedate <= endDate:
        coordinator = event["summary"]
    return coordinator

