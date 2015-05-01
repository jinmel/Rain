from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

#Auth(use Oauth2.0 import client_secrets.json)
gauth = GoogleAuth()
gauth.LocalWebserverAuth()

drive = GoogleDrive(gauth)

# file create & upload
"""
file1 = drive.CreateFile({'title' : 'Hello.txt'})
file1.SetContentString('Hello World!')
file1.Upload()
"""

#view file list

"""
file_list = drive.ListFile({'q':"'root' in parents"}).GetList()
for file1 in file_list:
	print 'title : %s, id : %s' % (file1['title'], file1['id'])
"""

file2 = drive.CreateFile()
file2.SetContentFile('Hello.txt')
file2.Upload()
print 'Created file %s with mimeType %s' % (file2['title'], file2['mimeType'])
# Created file Hello.txt with mimeType image/png

file3 = drive.CreateFile({'id': file2['id']})
print 'Downloading file %s from Google Drive' % file3['title'] # 'hello.png'
file3.GetContentFile('world.png')  # Save Drive file as a local file
