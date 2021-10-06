# Create meet using Google Calendar API

This script creates a Google Meet using the Google Calendar API by creating a calendar meeting with a conference call.

## Installation

``` bash
# Install requirements
python3 -m venv .env3
source .env3/bin/activate
pip3 install -r requirements.txt
```

## Getting secrets

Go to the credential page in the Google Cloud Console for an OAuth 2.0 credential (e.g. this ["meetbot" oauth2 credential](https://console.cloud.google.com/apis/credentials/oauthclient/399896422909-1c2oeats1d48gtri7usfque3u47635qe.apps.googleusercontent.com?authuser=1&project=mattermost-meet-328008) for Canonical members), and click "Download JSON". Save the file as `user.json` alongside this project's `meet.py`.

## Usage

``` bash
./meet.py
```

The first time you run this it will open a browser window. You should authorize with your organisation account.

Once authorized correctly, it will generate a meet code. On subsequent runs it shouldn't require authorization:

``` bash
$ ./meet.py 
Meet created: https://meet.google.com/guv-somv-haw
```

## Service accounts vs user accounts

It could in theory be possible to use a service account instead of your user account. E.g. [here's a service account credential for Canonical members](https://console.cloud.google.com/iam-admin/serviceaccounts/details/105695916903695317913;edit=true?previousPage=%2Fapis%2Fcredentials%3Fauthuser%3D1%26project%3Dmattermost-meet-328008&authuser=1&project=mattermost-meet-328008). You would simply save this credential as `service.json`, then change the code to use the `get_service_account_credentials` function instead of the `get_user_account_credentials` one.

The trouble is that a bare service account [can't create conference calls](https://stackoverflow.com/questions/61050432/cant-create-a-hangoutsmeet-with-calendar-api-using-java). Instead it needs to impersonate a user. To do that, it needs [domain-wide delegation of authority](https://developers.google.com/cloud-search/docs/guides/delegation) which must be granted by an organisation administrator.

Instead, we use [a standard OAuth2 flow](https://developers.google.com/people/quickstart/python) to authenticate as your user, and save your API token in `token.json`. Then as long as this file exists, you shouldn't need to authenticate again. This isn't ideal as it's sharing the permissions for a user, but it works.
