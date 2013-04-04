import sys
import requests
from google import TransportVehicle

class Download(object):
    def __init__(self, given_name, file_id):
        self.file_id = file_id
        self.given_name = given_name
    
    def download(self):
        # Get a file
        drive_service = TransportVehicle.build_drive_service()
        try:
            file = drive_service.files().get(fileId=self.file_id).execute()
        except AccessTokenCredentialsError as a:
            print "Download try:", a
            creds = TransportVehicle.manual_authorization()
            drive_service = TransportVehicle.build_drive_service(credentials=creds)
            file = drive_service.files().get(fileId=self.file_id).execute()

        url = file.get('downloadUrl')
        if url:
            resp, content = drive_service._http.request(url)
            if resp.status == 200:
                f = open(self.given_name,'w+')
                f.write(content)
                f.close()


if __name__ == '__main__':
    FILE_ID = sys.args[1]
    GIVEN_NAME = sys.args[2]
    JSESSIONID = sys.args[3]
    
    cookie = dict(JSESSIONID=JSESSIONID)
    access = requests.get('https://myglims.appspot.com/token', cookies=cookie)
    token = str( access.text ).strip( )
    
    TransportVehicle.setToken(token)

    TransportVehicle.download( FILE_ID, GIVEN_NAME )