from dropbox import client, rest, session
import simplejson as json

APP_KEY = "APP_KEY"
APP_SECRET = "APP_SECRET"
ACCESS_TYPE = "dropbox"

def authorize():
    sess = session.DropboxSession(APP_KEY, APP_SECRET, ACCESS_TYPE)
    
    try:
        stored_creds = open( 'dropbox.json' ).read().strip()
        cred_dict = json.loads( stored_creds )
        restored_token = sess.set_token( cred_dict['key'], cred_dict['secret'] )
        auth_client = client.DropboxClient(sess)
        return auth_client
    except Exception as e:
        print e.message

    request_token = sess.obtain_request_token()
    url = sess.build_authorize_url(request_token)
    print "url:", url
    print "Please visit this website and press the 'Allow' button, then hit 'Enter' here."
    raw_input()
    # This will fail if the user didn't visit the above URL and hit 'Allow'
    access_token = sess.obtain_access_token(request_token)
    auth_client = client.DropboxClient(sess)
    d = dict()
    d['key'] = access_token.key
    d['secret'] = access_token.secret
    drop = open('dropbox.json','w+')
    drop.write( json.dumps( d ) )
    drop.close()
    
    return auth_client

if __name__ == '__main__':
    authorized_client = authorize()
    
    #f = open('upload.txt')
    #response = authorized_client.put_file('/transit.txt', f)
    
    #f, metadata = authorized_client.get_file_and_metadata('/transit.txt')
    #out = open('download.txt', 'w')
    #out.write(f.read())
    #out.close()
    #print(metadata)