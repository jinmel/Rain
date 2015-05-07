from .. import clouddrive
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive as _GoogleDrive
from pydrive.files import GoogleDriveFile
from os.path import os

__name__ = "Google Drive"

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
            gauth = GoogleAuth()
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
        fid = self.find_file_id(filename) 
        if fid is None:
            return -1
        else:
            file_new = drive.CreateFile({'id' : fid})
            file_new.GetContentFile(filename)
            return 1


    def write(self, filename):
        dirname_s = dirname.split("/")
        if len(dirname_s) > 2:
            fid = self.find_file_id(dirname_s[len(dirname_s)-2])
            if fid is None :
                return -1
        else:
            fid = 'root'
        
        file_new = drive.CreateFile({'title':filename,'parents':[{'kind':"dirve#fileLink",'id':fid}]})
        try:
            file_new.SetContentFile(filename)

            file_new.Upload()
        except:
            return -1

        return 1

    def mkdir(self, dirname):
        dirname_s = dirname.split("/")
        if len(dirname_s) > 3 :
            fid = self.find_file_id(dirname_s[len(dirname_s)-3])
            if fid is None :
                return -1
        else:
            fid = 'root'
            
#        dir_list = self.make_parents_list(dirname_s)
#        p1, p2 = dir_list[len(dir_list)-1]
          
        if os.path.isdir(dirname):
            file_new = drive.CreateFile({'title' : dirname, 'mimeType' : "application/vnd.google-apps.folder",'parents':[{'kind':"drive#fileLink", 'id':fid}]})
        else :
            return -1
        try :
            file_new.Upload()
        except:
            return -1
        return 1

    def delete(self, filename):
        fid = self.find_file_id(filename)
        if fid is None :
            return -1
        else:
            file_new = drive.CreateFile({'id' : fid})
            file_new._FilesDelete()
            return 1

    """
    def make_parents_list(self, dirname_s):
        parents_list = []
        if len(dirname_s) > 3 :
            for i in xrange(len(dirname_s)-1) :
                if i != 0 :
                    if find_file_id(dirname_s[i]) is None :
                        return -1
                    else
                        if i != 1 :
                            p1, p2 = parents_list[i-2]
                        else
                            p2 = {'id':'root','kind':'drive#fileLink'}
                        parents_list += [(drive.CreateFile({'id' :find_file_id(dirname_s[i]),'kind':"drive#fileLink",'parents':[p2]}), {'id' :find_file_id(dirname_s[i]),'kind':"dirve#fileLink"})]
        
        return parents_list
    """

    def find_file_id(self, filename):
        fid = ListFolder('root',filename)
        return fid
    
    def ListFolder(parent, filename):
        file_list = self.drive.ListFile({'q':"'%s' in parents and trashed=false" % parent}).GetList()
        for f in file_list:
            if f['title']=="filename":
                return f['id']
                
            if f['mimeType']=='application/vnd.google-apps.folder':
                ListFolder(f['id'])
        return None
