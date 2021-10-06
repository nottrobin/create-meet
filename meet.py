#! /usr/bin/env python3

import time
import os.path
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account
import googleapiclient.discovery


SCOPES = ["https://www.googleapis.com/auth/calendar"]


def get_service_account_credentials():
    return service_account.Credentials.from_service_account_file(
        "service.json", scopes=SCOPES
    )


def get_user_account_credentials():
    """
    Get credentials for authorising an installed application using the
    Google API OAuth 2.0 method.

    Code copied from here:
    https://developers.google.com/people/quickstart/python
    """

    credentials = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        credentials = Credentials.from_authorized_user_file(
            "token.json", SCOPES
        )
    # If there are no (valid) credentials available, let the user log in.
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "user.json", SCOPES
            )
            credentials = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(credentials.to_json())

    return credentials


event_body = {
    "summary": "Sample event",
    "description": "This is a sample event.",
    "start": {
        "dateTime": "2015-05-28T09:00:00-07:00",
        "timeZone": "America/Los_Angeles",
    },
    "end": {
        "dateTime": "2015-05-28T17:00:00-07:00",
        "timeZone": "America/Los_Angeles",
    },
    "conferenceData": {
        "createRequest": {
            "requestId": str(time.time())[:10],
            "conferenceSolutionKey": {"type": "hangoutsMeet"},
        }
    },
}

calendar = googleapiclient.discovery.build(
    "calendar", "v3", credentials=get_user_account_credentials()
)
event = (
    calendar.events()
    .insert(calendarId="primary", conferenceDataVersion=1, body=event_body)
    .execute()
)

meet_url = event.get("hangoutLink")

calendar.events().delete(calendarId="primary", eventId=event["id"]).execute()

print(f"Meet created: {meet_url}")
