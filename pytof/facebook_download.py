from facebook import Facebook
from os.path import join, exists, basename, sep
from shutil import rmtree
import os, sys

from utils import _err_exit
from utils import ProgressMsg

def facebook_download(outDir, fb_uid = None):

    # out dir setup
    if exists(outDir):
        rmtree(outDir)
    os.makedirs(outDir)
 
    # Get api_key and secret_key from a file
    # first line is api key and second line is secret
    fbs = open('/tmp/facebook_keys.txt').readlines()
    facebook = Facebook(fbs[0].strip(), fbs[1].strip())
 
    facebook.auth.createToken()
    # Show login window
    facebook.login()
 
    # Login to the window, then press enter
    print 'After logging in, press enter...'
    raw_input()
 
    facebook.auth.getSession()
 
    # PHOTOS
    # By album ID
    # photos = facebook.photos.getAlbums(friends[1]['uid'])
    # photos = facebook.photos.get('', '5307080636404757', '')

    friends = facebook.friends.get()
    names = facebook.users.getInfo(friends, ['name'])
    for n in names:
        print n['name'].encode('utf-8'), ':', n['uid']

    # By user id
    if fb_uid is None:
        fb_uid = facebook.uid
    photos = facebook.photos.get(fb_uid)

    progress = ProgressMsg(len(photos), output=sys.stderr)
    for p in photos:
        url = p['src_big']
        fn = url.split('/')[-1]
        fd = open(join(outDir, fn), 'w')

        import urllib
        bytes = urllib.urlopen(url).read()
        fd.write(bytes)
        fd.close()

        progress.Increment()
 
if __name__ == "__main__":
    desktop_app()
