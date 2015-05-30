from os import path
import os
from ports.dropbox import DropBox
from ports.googledrive import GoogleDrive
from ports.box import Box
from utils import RainMetaFileAdapter
from rainprotocol import RainPacketBuilder
import time
from socket import *
from hashlib import md5

RAIN_REMOTE_PATH = '/Rain'
RAIN_HOST = "plus.or.kr"
RAIN_PORT = 1287
RAIN_ADDR = (RAIN_HOST, RAIN_PORT)


class RainDrive(object):
    def __init__(self, metafile_adapter):
        self.clouds = []
        self.mfa = metafile_adapter
        username = self.mfa.get_username()
        self.packet_builder = RainPacketBuilder(username)
        self.load_cloud()

    def add_cloud(self, cloud):
        self.clouds.append(cloud)
        # sort by descending disk capacity
        self.clouds.sort(key=lambda disk: disk.capacity(), reverse=True)

    def load_cloud(self):
        cloud_names = self.mfa.get_all_cloud_name()
        loaded_cloud_names = [cloud.name for cloud in self.clouds]
        for cloud_name in cloud_names:
            if cloud_name not in loaded_cloud_names:
                if cloud_name == DropBox.name:
                    self.add_cloud(DropBox(self.mfa.get_cloud_access_token(cloud_name)))
                elif cloud_name == GoogleDrive.name:
                    self.add_cloud(GoogleDrive(self.mfa.get_cloud_access_token(cloud_name)))
                elif cloud_name == Box.name:
                    self.add_cloud(Box(self.mfa.get_cloud_access_token(cloud_name)))
                else:
                    raise Exception('Unknown cloud service name: ' + cloud_name)

    def get_cloud_num(self):
        return len(self.clouds)

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
        print 'sync invoked'
        if not self.check_hash(): #hash is different->get new xml
            print 'hash fail'
            self.acquire_lock()
            latest_xml = self.request_metafile()
            latest_mfa = RainMetaFileAdapter()
            latest_mfa.set_metafile_from_string(latest_xml)
            latest_cloud_names = latest_mfa.get_all_cloud_name()
            current_cloud_names = self.mfa.get_all_cloud_name()
            for latest_cname in latest_cloud_names:
                if latest_cname not in current_cloud_names:
                    access_token = latest_mfa.get_cloud_access_token(latest_cname)
                    self.mfa.add_cloud(latest_cname, access_token)
            self.load_cloud()

            for cloud_name in latest_cloud_names:
                cloud = self.get_cloud_by_name(cloud_name)
                latest_file_map = latest_mfa.get_file_map(cloud_name)
                current_file_map = self.mfa.get_file_map(cloud_name)
                diff = set(latest_file_map.keys()) - set(current_file_map.keys())
                new_local_files = list(diff)
                for new_local_file in new_local_files:
                    remote_file_name = latest_file_map[new_local_file]
                    data = cloud.read(latest_file_map[new_local_file])
                    f = open(new_local_file, "wb")
                    f.write(data)
                    f.close()
                    self.mfa.add_file(cloud_name, new_local_file, remote_file_name, str(path.getsize(new_local_file)))

                diff = set(current_file_map.keys()) - set(latest_file_map.keys())
                delete_local_files = list(diff)
                for deleted_local_file in delete_local_files:
                    os.unlink(deleted_local_file)
                    self.mfa.remove_file(cloud_name, delete_local_files)
                    # no need to request delete to cloud drive because it
                    # already has been deleted by another node

            #finally, update current mfa to latest mfa
            self.upload_metafile()

    def login(self):
        s = socket(AF_INET, SOCK_STREAM)
        s.connect(RAIN_ADDR)
        s.send(self.packet_builder.login())
        data = self.recv_timeout(s)
        xml_content = self.packet_builder.UnpackData(data)[2]
        s.close()

    def check_hash(self):
        hashreq = self.packet_builder.hash_request()
        s = socket(AF_INET, SOCK_STREAM)
        s.connect(RAIN_ADDR)
        s.send(hashreq)
        data = self.recv_timeout(s)
        hash_value = self.packet_builder.UnpackData(data)[2]
        s.close()
        metafile_data = self.mfa.get_raw_xml()
        metafile_hash = md5(metafile_data).hexdigest()

        return hash_value == metafile_hash

    def request_metafile(self):
        s = socket(AF_INET, SOCK_STREAM)
        s.connect(RAIN_ADDR)
        s.send(self.packet_builder.xml_request())
        data = self.recv_timeout(s)
        print data
        xml_content = self.packet_builder.UnpackData(data)[2]
        s.close()
        return xml_content

    def acquire_lock(self):
        print "acquiring lock"
        s = socket(AF_INET, SOCK_STREAM)
        s.connect(RAIN_ADDR)
        s.send(self.packet_builder.xml_lock())
        data = self.recv_timeout(s)
        print repr(data)
        lock = self.packet_builder.UnpackData(data)[2]
        print lock
        s.close()
        return lock == "YES"

    def upload_metafile(self):
        print "uploading metafile.."
        s = socket(AF_INET, SOCK_STREAM)
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

