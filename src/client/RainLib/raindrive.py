from os import path
from ports.dropbox import DropBox
from ports.googledrive import GoogleDrive
from ports.box import Box
from utils import RainMetaFileAdapter

RAIN_REMOTE_PATH = '/Rain'


class RainDrive(object):
    def __init__(self, metafile_adapter):
        self.clouds = []
        self.mfa = metafile_adapter
        cloud_names = self.mfa.get_all_cloud_name()
        for cloud_name in cloud_names:
            if cloud_name == DropBox.name:
                self.add_cloud(DropBox(self.mfa.get_cloud_access_token(cloud_name)))
            elif cloud_name == GoogleDrive.name:
                self.add_cloud(GoogleDrive(self.mfa.get_cloud_access_token(cloud_name)))
            elif cloud_name == Box.name:
                self.add_cloud(Box(self.mfa.get_cloud_access_token(cloud_name)))
            else:
                raise Exception('Unknown cloud service name: ' + cloud_name)

    def add_cloud(self, cloud):
        self.clouds.append(cloud)
        # sort by descending disk capacity
        self.clouds.sort(key=lambda disk: disk.capacity(), reverse=True)

    def get_cloud_by_name(self, cloud_name):
        for d in self.clouds:
            if d.name == cloud_name:
                return d
        return None

    def new_file(self, filename):
        cloud = self.clouds[0] # add file to cloud that has highest capacity
        f = open(filename, 'rb')
        data = f.read()
        f.close()
        remote_filename = path.join(RAIN_REMOTE_PATH, filename).replace('./', '')
        cloud.write(remote_filename, data)
        self.mfa.add_file(cloud.name, filename, remote_filename, str(path.getsize(filename)))
        self.mfa.write()


    def remove_file(self, filename):
        # get corresponding cloud drive by local filename
        cloud_name = self.mfa.get_cloud_name_by_local_filename(filename)
        mapping = self.mfa.get_file_map(cloud_name)
        remote_filename = mapping[filename]

        # delete from drive
        cloud = self.get_cloud_by_name(cloud_name)
        cloud.delete(remote_filename)

        # delete from metafile
        self.mfa.remove_file(cloud_name, filename)
        self.mfa.write()
        #TODO: server interaction

    def dump_metafile(self):
        return self.mfa.get_raw_xml_file()

    def set_metafile_adpater(self,mfa):
        self.mfa = mfa

