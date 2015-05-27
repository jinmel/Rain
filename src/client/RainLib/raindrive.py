from os import path

RAIN_REMOTE_PATH = '/Rain/'


class RainDrive(object):
    def __init__(self, metafile_adapter):
        self.clouds = []
        self.mfa = metafile_adapter

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
        remote_filename = path.join(RAIN_REMOTE_PATH, filename)
        cloud.write(remote_filename, data)
        self.mfa.add_file(cloud.name, filename, remote_filename, path.getsize(filename))
        self.mfa.write()
        #TODO: server interaction

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






























