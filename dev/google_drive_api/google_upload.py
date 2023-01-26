from __future__ import print_function

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials

def upload_basic():
    """Insert new file.
    Returns : Id's of the file uploaded

    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.
    """
    # creds, _ = google.auth.load_credentials_from_file("token.json")
    creds = Credentials.from_authorized_user_file('token.json')

    try:
        # create drive api client
        service = build('drive', 'v3', credentials=creds)

        # Information about the file
        file_metadata = {'name': 'pic_1.png',
                         'parents': ['1LhKRe91Vu2JSbWUIU6Q_bSGFE6WowNH_']}
        # File itself (path to the file required)
        media = MediaFileUpload('../../archive/pic_1.png',
                                mimetype='image/jpeg', resumable=True)
        file = service.files().create(body=file_metadata, media_body=media,
                                      fields='id').execute()
        print(F'File ID: {file.get("id")}')

    except HttpError as error:
        print(F'An error occurred: {error}')
        file = None

    return file.get('id')


if __name__ == '__main__':
    upload_basic()
    print(help(MediaFileUpload))
