import httplib2
import simplejson as sj
import webbrowser

from apiclient.discovery import build
from oauth2client.client import OAuth2WebServerFlow, OAuth2Credentials
from oauth2client.client import AccessTokenCredentials, AccessTokenCredentialsError

class TransportVehicle(object):
    #Maybe make it non-classmethods?
    
    def __init__(self, token):
        self.token = token

    def createToken(self):
        d = sj.loads(self.token)
        at = d['AccessToken']
        d['access_token'] = at
        rt = d['RefreshToken']
        d['refresh_token'] = rt
        del d["AccessToken"]
        del d['RefreshToken']
        d['user_agent'] = 'Midgard/1.0'
        token = sj.dumps(d)
        return token
         
    def build_drive_service(self, credentials=None, credential_name="credentials.json"):
        token = self.createToken()
        if not credentials:
            try:
                cred_file = open(credential_name)
                credentials = OAuth2Credentials.from_json( cred_file.read() )
            except:
                credentials = AccessTokenCredentials.from_json(token)
            
        # Create an httplib2.Http object and authorize it with our credentials
        http = httplib2.Http()
        http = credentials.authorize(http)
        drive_service = build('drive', 'v2', http=http)
        return drive_service
       
    def manual_authorization( self , credential_file_name='credentials.json' ):
        # Copy your credentials from the APIs Console
        CLIENT_ID = 'CLIENT ID HERE'
        CLIENT_SECRET = 'CLIENT SECRET HERE'
        # Redirect URI for installed apps
        REDIRECT_URI = 'REDIRECT URI'
        
        # Before going through the hassle of authentication
        # attempt to load info from a JSON cache
        
        with open('client_secrets.json') as f:
            id_dict = sj.loads(f.read())
            # Copy your credentials from the APIs Console
            CLIENT_ID = id_dict['client_id']
            CLIENT_SECRET = id_dict['client_secret']
            # Redirect URI for installed apps
            REDIRECT_URI = id_dict['redirect_uri']

        # Check https://developers.google.com/drive/scopes for all available scopes
        OAUTH_SCOPE = 'https://www.googleapis.com/auth/drive'
        
        # Run through the OAuth flow and retrieve credentials
        flow = OAuth2WebServerFlow(CLIENT_ID, CLIENT_SECRET, OAUTH_SCOPE, REDIRECT_URI)
        authorize_url = flow.step1_get_authorize_url()
        webbrowser.open(authorize_url)
        code = raw_input('Enter verification code: ').strip()
        credentials = flow.step2_exchange(code)
        
        cred_file = open( credential_file_name , 'w+' )
        cred_file.write( credentials.to_json() )
        cred_file.close()
        
        return credentials