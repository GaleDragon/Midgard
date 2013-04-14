import sys
from apiclient.http import MediaFileUpload
from google import TransportVehicle
import requests

class Upload(object):
    def __init__(self, file_path, given_name):
        self.file_path = file_path
        self.given_name = given_name
    
    def upload(self):
        # Path to the file to upload
        drive_service = TransportVehicle.build_drive_service()
        media_body = MediaFileUpload(self.file_path, mimetype='text/plain', resumable=True)
        body = {
            'title': self.given_name,
            'description': 'A test document',
            'mimeType': 'text/plain'
        }
        try:
            file = drive_service.files().insert(body=body, media_body=media_body).execute()
        except Exception as a:
            print "Upload try:", a
            creds = TransportVehicle.manual_authorization()
            drive_service = TransportVehicle.build_drive_service(credentials=creds)
            file = drive_service.files().insert(body=body, media_body=media_body).execute()

        return file['id']
        
if __name__ == '__main__':
    # Add argparse here
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--jsession_id', metavar="ID", default=None, 
						help="The JSession ID that will be used to attempt to authenticate.")
    parser.add_argument('file_path')
    parser.add_argument('given_name')
    args = parser.parse_args()
    FILE_PATH = args.file_path
    GIVEN_NAME = args.given_name
    token = None
    if args.jsession_id:
        JSESSIONID = args.jsession_id
        cookie = dict(JSESSIONID=JSESSIONID)
        access = requests.get('https://myglims.appspot.com/token', cookies=cookie)
        token = str( access.text ).strip( )
    t = TransportVehicle(token)
    u = Upload( FILE_PATH, GIVEN_NAME )
    fileID = u.upload()