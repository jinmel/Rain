from .. import clouddrive
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from pydrive.files import GoogleDriveFile
from os.path import os

__name__ = "Google Drive"


class GoogleDrive(clouddrive.CloudDrive):
    def __init__(self, access_token=None, drive=None):
        super.__init__(self.access_token)
        pass

    def auth(self):
        gauth = GoogleAuth()
        if(self.access_token == None) :
            gauth.LocalWebserverAuth()
            gauth.SaveCredentialsFile("oauth.txt")
            f = open("oauth.txt")
            self.access_token = f.readline()
            f.close()
            os.remove("oauth.txt")
        else :
            f = open("oauth.txt", "w")
            f.write(self.access_token)
            f.close()
            gauth.LoadCredentials(self.access_token)
            os.remove("oauth.txt")
            
        self.drive = GoogleDrive(gauth)
    def read(self, filename):

    def write(self, filename):

    def mkdir(self, dirname):
        for i in len(dirname.split("/"))-1 :
            
        if os.path.isdir(dirname):
            file_new = drive.CreateFile({'title' : dirname, 'mimeType' : "application/vnd.google-apps.folder",'parents':[{'kind':parents['kind'], 'id':parents['id']}]})
        else :
            return -1
        file_new.Upload()
        return 1

    def delete(self, filename):


    def find_file_id(self, filename):
    
