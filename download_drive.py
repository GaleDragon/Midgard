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
    # Add argparse here
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--jsession_id', metavar="ID", default=None, help="The JSession ID that will be used to attempt to authenticate.")
    parser.add_argument('file_path')
    parser.add_argument('given_name')
    args = parser.parse_args()
    
    FILE_ID = sys.argv[1]
    GIVEN_NAME = sys.argv[2]
    token = None
    if args.jsession_id:
        JSESSIONID = args.jsession_id
        cookie = dict(JSESSIONID=JSESSIONID)
        access = requests.get('https://myglims.appspot.com/token', cookies=cookie)
        token = str( access.text ).strip( )
    
    
    TransportVehicle.setToken(token)
    d = Download( GIVEN_NAME, FILE_ID )
    d.download()