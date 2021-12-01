######################################################################
# An example of python script to upload an image to Google Photo
#
# This script simply uploads an image to Google Photos,
# using OAuth scenario for Limite-input devices
# https://developers.google.com/identity/protocols/oauth2#device
#
# == Preparation ==
# Please follow instruction of Google and generate a JSON file which
# contains Client Secret:
# https://developers.google.com/workspace/guides/create-credentials
# 
# Here, please keep in mind:
# 1. Please select "TV and Limited input device" as "Application type".
# 2. Please download JSON object for Client ID information, and
#    store it as 'client_secret.json'.
#
# == 1st Run / Authentication ==
# Upon first run, please follow these steps:
# 1. The script will show URL for authentication to standard output.
# 2. Please open your favorite browser to open URL
#    and perform authentication.
#    Here, the browser may show security warnings,
#    but please ignore these warnings.
# 3. At last step of authentication, the authorization code will be
#    shown on your browser.
# 4. Please copy the code and enter it to standard input of this script,
#    to complete authentication.
######################################################################
import os.path
import pickle
import json
import mimetypes
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import AuthorizedSession
from google.auth.transport.requests import Request

def get_authorized_session_oob(opt):
    # Reference: https://github.com/ido-ran/google-photos-api-python-quickstart
    SCOPES = [ 'https://www.googleapis.com/auth/photoslibrary' ]
    creds_file_name = opt.get('creds')
    client_secret_file = opt.get('client_secret')
    creds = None
    try:
        with open(creds_file_name, 'rb') as creds_file:
            creds = pickle.load(creds_file)
            print('credential loaded: ' + creds_file_name)
    except:
        print('failed to read:' + creds_file_name)
    if not creds or not creds.valid:
        if (creds and creds.expired and creds.refresh_token):
            print('credential refreshed')
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                    client_secret_file, SCOPES,
                    redirect_uri='urn:ietf:wg:oauth:2.0:oob')
            url, user_code = flow.authorization_url()
            print('User code: ' + user_code)
            print('Please connect to following URL to authorize this application, and input authorization code.')
            print(url)
            code = input('Enter authorization code: ').strip()
            flow.fetch_token(code=code)
            creds = flow.credentials
        with open(creds_file_name, 'wb') as creds_file:
            pickle.dump(creds, creds_file)
    return AuthorizedSession(creds)

def upload(session, file):
    # Step 1: upload media body
    try:
        with open(file, 'rb') as photo_file:
            photo_bytes = photo_file.read()
    except OSError as err:
        print('failed to read: ' + file)
        return
    mime_type, encoding = mimetypes.guess_type(file)
    session.headers['Content-type'] = 'application/octet-stream'
    session.headers['X-Goog-Upload-Content-Type'] = mime_type
    session.headers['X-Goog-Upload-Protocol'] = 'raw'
    session.headers['X-Goog-Upload-File-Name'] = os.path.basename(file)
    url = 'https://photoslibrary.googleapis.com/v1/uploads'
    resp = session.post(url, photo_bytes)
    if resp.ok:
        print('uploaded: %d bytes' % len(photo_bytes))
        print('token: ' + resp.text)
        upload_token = resp.text
    else:
        print('failed: %d' % resp.status_code)
        return
    del(session.headers['X-Goog-Upload-Content-Type'])
    del(session.headers['X-Goog-Upload-Protocol'])
    del(session.headers['X-Goog-Upload-File-Name'])
    # Step 2: create media-item based on upload data.
    session.headers['Content-type'] = 'application/json'
    json_body = json.dumps({'newMediaItems':[{'description':'','simpleMediaItem':{'uploadToken':upload_token}}]})
    url = 'https://photoslibrary.googleapis.com/v1/mediaItems:batchCreate'
    resp = session.post(url, json_body)
    if resp.ok:
        print('done')
    else:
        print('failed: %d' % resp.status_code)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Script to upload an image to Google Photos.')
    parser.add_argument('filename', help='filename of image to upload')
    parser.add_argument('-c', '--creds', default='credentials.pickle',
            help='specify credential file. default: credentials.pickle')
    parser.add_argument('-s', '--client_secret', default='client_secret.json',
            help='specify Client-Secret file, used to set Client ID etc. defalt: client_secret.json')
    opt = vars(parser.parse_args())
    session = get_authorized_session_oob(opt)
    upload(session, opt['filename'])
