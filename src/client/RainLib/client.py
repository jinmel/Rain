from rainprotocol import RainPacketBuilder
import time
from socket import *
from hashlib import md5
from utils import RainMetaFileAdapter


HOST = "plus7.postech.ac.kr"
PORT = 1287


class RainClient(object):
    def __init__(self, user_id, rain_drive, mfa, host, port):
        self.rain_drive = rain_drive
        self.user_id = user_id
        self.packet_builder = RainPacketBuilder(self.user_id)
        self.host, self.port = host, port

    def login(self):
        clientsocket = socket(AF_INET, SOCK_STREAM)
        addr = ("plus7.postech.ac.kr", 1287)
        bufsize = 1024

        try:
            clientsocket.connect(addr)
        except:
            print ("don't reach (%s:%s)" % addr)

        clientsocket.send(self.packet_builder.login())
        xml_content = self.recv_timeout(clientsocket)
        xml = open("metafile.xml", "w")
        xml.write(xml_content)
        xml.close()
        self.rain_drive.set_metafile_adapter(RainMetaFileAdapter("metafile.xml"))

    def check_hash(self):
        hashreq = self.packet_builder.hash_request()
        s = socket(AF_INET, SOCK_STREAM)
        s.connect((self.host, self.port))
        s.send(hashreq)
        hash_value = s.recv(1024)
        s.close()
        metafile_data = self.rain_drive.dump_metafile()
        metafile_hash = md5(metafile_data).hexdigest()

        return hash_value == metafile_hash

    def request_metafile(self):
        s = socket(AF_INET, SOCK_STREAM)
        s.connect((self.host, self.port))
        s.send(self.packet_builder.xml_request())
        xml_content = self.recv_timeout(s)
        xml = open("metafile.xml", "w")
        xml.write(xml_content)
        xml.close()
        self.rain_drive.set_metafile_adapter(RainMetaFileAdapter("metafile.xml"))

    def update_metafile(self):
        #hash is same xml not changed
        if self.check_hash():
            lock = ''
            while lock == "YES":
                time.sleep(3)
                s = socket(AF_INET, SOCK_STREAM)
                s.connect((self.host, self.port))
                s.send(self.packet_builder.xml_lock())
                lock = s.recv(100)
            s.close()
            s = socket(AF_INET, SOCK_STREAM)
            s.connect((self.host, self.port))
            xml = open("metafile.xml", "r")
            xml_content = xml.read()
            xml.close()
            s.send(self.packet_builder.xml_upload(xml_content))
            s.close()
        else:
            raise Exception("Hash value conflict")

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











