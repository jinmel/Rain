class CloudDrive(object):
    def __init__(self, access_token):
        self.access_token = access_token

    @staticmethod
    def auth():
        #TODO : Do authentification and return access token
        raise NotImplementedError()

    def read(self, filename):
        #TODO : Read filename(remote_filename) from cloud drive and return contets on success or -1 on failure
        raise NotImplementedError()

    def write(self, filename, data):
        #TODO : Write filename(remote_filename) from cloud drive and return 1 on success or -1 on failure
        raise NotImplementedError()

    def mkdir(self, dirname):
        #TODO : Make directory at dirname at cloud drive return 1 on success or -1 on failure
        raise NotImplementedError()

    def delete(self, filename):
        #TODO : delete filename(remote_filename) from cloud drive return 1 on success or -1 on failure
        raise NotImplementedError()

    def capacity(self):
        #TODO : return remaining capacity of cloud drive
        raise NotImplementedError()




