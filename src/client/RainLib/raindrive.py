from os import path
from ports.dropbox import DropBox
from ports.googledrive import GoogleDrive
from ports.box import Box
from utils import RainMetaFileAdapter
from rainprotocol import RainPacketBuilder
import time
from socket import *
from hashlib import md5

RAIN_REMOTE_PATH = '/Rain'
RAIN_HOST = "plus7.postech.ac.kr"
RAIN_PORT = 1287
RAIN_ADDR = (RAIN_HOST, RAIN_PORT)


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
        username = self.mfa.get_username()
        self.packet_builder = RainPacketBuilder(username)

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
        #try acquire lock every 3 seconds
        while not self.acquire_lock():
            time.sleep(3)

        cur_cloud = self.clouds[0]  # add file to cloud that has highest capacity
        f = open(filename, 'rb')
        data = f.read()
        f.close()
        remote_filename = path.join(RAIN_REMOTE_PATH, filename).replace('./', '')
        cur_cloud.write(remote_filename, data)
        self.mfa.add_file(cur_cloud.name, filename, remote_filename, str(path.getsize(filename)))
        self.upload_metafile()

    def remove_file(self, filename):
        while not self.acquire_lock():
            time.sleep(3)

        # get corresponding cloud drive by local filename
        cloud_name = self.mfa.get_cloud_name_by_local_filename(filename)
        mapping = self.mfa.get_file_map(cloud_name)
        remote_filename = mapping[filename]

        # delete from drive
        cloud = self.get_cloud_by_name(cloud_name)
        cloud.delete(remote_filename)

        # delete from metafile
        self.mfa.remove_file(cloud_name, filename)
        # upload metafile
        self.upload_metafile()

    def sync(self):
        pass


    def login(self):
        s = socket(AF_INET, SOCK_STREAM)
        try:
            s.connect(RAIN_ADDR)
        except:
            print ("don't reach (%s:%s)" % RAIN_ADDR)

        s.send(self.packet_builder.login())
        xml_content = self.recv_timeout(s)
        s.close()
        self.mfa.set_metafile_from_string(xml_content)

    def check_hash(self):
        hashreq = self.packet_builder.hash_request()
        s = socket(AF_INET, SOCK_STREAM)
        s.connect(RAIN_ADDR)
        s.send(hashreq)
        hash_value = s.recv(1024)
        s.close()
        metafile_data = self.mfa.get_raw_xml()
        metafile_hash = md5(metafile_data).hexdigest()

        return hash_value == metafile_hash

    def request_metafile(self):
        s = socket(AF_INET, SOCK_STREAM)
        s.connect(RAIN_ADDR)
        s.send(self.packet_builder.xml_request())
        xml_content = self.recv_timeout(s)
        s.close()
        return xml_content

    def acquire_lock(self):
        s = socket(AF_INET, SOCK_STREAM)
        s.connect(RAIN_ADDR)
        s.send(self.packet_builder.xml_lock())
        lock = s.recv(100)
        s.close()
        return lock == "YES"

    def upload_metafile(self):
        s = socket(AF_INET,SOCK_STREAM)
        s.connect(RAIN_ADDR)
        current_xml_content = self.mfa.get_raw_xml()
        s.send(self.packet_builder.xml_upload(current_xml_content))
        s.close()

    def recv_timeout(self, sock, timeout=2):
        sock.setblocking(0)

        total_data = []
        data = ''

        begin = time.time()
        while 1:
            if total_data and time.time() - begin > timeout:
                break

            elif time.time() - begin > timeout * 2:
                break

            try:
                data = sock.recv(8192)
                if data:
                    total_data.append(data)
                    begin = time.time()
                else:
                    time.sleep(0.1)

            except:
                pass

        return ''.join(total_data)

