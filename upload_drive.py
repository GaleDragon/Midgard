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
        except AccessTokenCredentialsError as a:
            print "Upload try:", a
            creds = TransportVehicle.manual_authorization()
            drive_service = TransportVehicle.build_drive_service(credentials=creds)
            file = drive_service.files().insert(body=body, media_body=media_body).execute()

        return file['id']
        
if __name__ == '__main__':
    FILE_PATH = sys.args[1]
    GIVEN_NAME = sys.args[2]
    JSESSIONID = sys.args[3]
    
    cookie = dict(JSESSIONID=JSESSIONID)
    access = requests.get('https://myglims.appspot.com/token', cookies=cookie)
    token = str( access.text ).strip( )
    
    TransportVehicle.setToken(token)

    fileID = TransportVehicle.upload( FILE_PATH, GIVEN_NAME )