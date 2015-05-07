from .. import clouddrive
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive as _GoogleDrive
from pydrive.files import GoogleDriveFile
from os.path import os

class GoogleDrive(clouddrive.CloudDrive):
    def __init__(self, access_token=None):
        if access_token is not None :
            self.access_token = access_token
            clouddrive.CloudDrive.__init__(self, access_token)
        else :
           clouddrive.CloudDrive.__init__(self)
        if self.access_token is not None :
            f = open("oauth.txt", "w")
            f.write(self.access_token)
            f.close()
            gauth.LoadCredentialsFile("oauth.txt")
            os.remove("oauth.txt")
            self.drive = _GoogleDrive(gauth)

    def auth(self):
        gauth = GoogleAuth()
#        if(self.access_token == None) :
        gauth.LocalWebserverAuth()
        gauth.SaveCredentialsFile("oauth.txt")
        f = open("oauth.txt")
        self.access_token = f.readline()
        f.close()
        os.remove("oauth.txt")
        return self.access_token
#        else :
#            f = open("oauth.txt", "w")
#            f.write(self.access_token)
#            f.close()
#            gauth.LoadCredentials(self.access_token)
#            os.remove("oauth.txt")
            
#        self.drive = GoogleDrive(gauth)
    def read(self, filename):
        pass

    def write(self, filename):
        pass

    def mkdir(self, dirname):
        for i in len(dirname.split("/"))-1 :
            pass
            
        if os.path.isdir(dirname):
            file_new = drive.CreateFile({'title' : dirname, 'mimeType' : "application/vnd.google-apps.folder",'parents':[{'kind':parents['kind'], 'id':parents['id']}]})
        else :
            return -1
        file_new.Upload()
        return 1

    def delete(self, filename):
        pass


    def find_file_id(self, filename):
        pass
    
    def ListFolder(parent):
        file_list = self.drive.ListFile({'q':"'%s' in parents and trashed=false" % parent}).GetList()
        for f in file_list:
            if f['mimeType']=='application/vnd.google-apps.folder':
                ListFolder(f['id'])

