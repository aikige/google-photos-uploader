import os.path
import pickle
import json
import mimetypes
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import AuthorizedSession
from google.auth.transport.requests import Request

def get_authorized_session_oob(opt):
    # Reference: https://github.com/ido-ran/google-photos-api-python-quickstart
    SCOPES = [ 'https://www.googleapis.com/auth/photoslibrary.appendonly',
            'https://www.googleapis.com/auth/photoslibrary.readonly.appcreateddata' ]
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

def create_album(session, title):
    url = 'https://photoslibrary.googleapis.com/v1/albums'
    session.headers['Content-type'] = 'application/json'
    msg = {'album':{ 'title': title }}
    json_body = json.dumps(msg)
    resp = session.post(url, json_body).json()
    del(session.headers['Content-type'])
    if resp.ok:
        resp_json = resp.json()
        print(json.dumps(resp_json, indent=2))
        return resp_json.get('id')
    else:
        return None

def list_albums(session):
    url = 'https://photoslibrary.googleapis.com/v1/albums'
    resp = session.get(url)
    if resp.ok:
        resp_json = resp.json()
        print(json.dumps(resp_json, indent=2))
        return resp_json
    else:
        return {}

def upload(session, file, album_id=None):
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
    msg = {'newMediaItems':[{'description':'','simpleMediaItem':{'uploadToken':upload_token}}]}
    if album_id is not None:
        msg['albumId'] = album_id
    json_body = json.dumps(msg)
    url = 'https://photoslibrary.googleapis.com/v1/mediaItems:batchCreate'
    resp = session.post(url, json_body)
    if resp.ok:
        print('done')
    else:
        print('failed: %d: %s' % (resp.status_code, resp.text))

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Script to upload an image to Google Photos.')
    parser.add_argument('filename', nargs='?', help='filename of image to upload', default=None)
    parser.add_argument('-c', '--creds', default='credentials.pickle',
            help='specify credential file. default: credentials.pickle')
    parser.add_argument('-s', '--client-secret', default='client_secret.json',
            help='specify Client-Secret file, used to set Client ID etc. defalt: client_secret.json')
    parser.add_argument('-l', '--list-albums', action='store_true',
            help='list albums created by this application.')
    parser.add_argument('-a', '--album-id', default=None,
            help='set album id to upload the image (optional)')
    parser.add_argument('-n', '--new-album', default=None,
            help='crate album with specified title and append image to the album.')
    opt = vars(parser.parse_args())
    session = get_authorized_session_oob(opt)
    if opt['new_album']:
        opt['album_id'] = create_album(session, opt['new_album'])
    if opt['list_albums']:
        list_albums(session)
    if opt['filename']:
        upload(session, opt['filename'], opt['album_id'])
