from socket import *
import struct

RAIN_REMOTE_PATH = '/Rain/'


def PackData(mod, userid, data):
    fmt = "<BBHH%ds%ds" % (len(userid), len(data))
    return struct.pack(fmt, mod, len(userid), len(userid) + 6, len(data), userid, data)



class RainPacketBuilder(object):
    def __init__(self, user_id):
        self.user_id = user_id

    def login(self):
        return PackData(0x0, self.user_id, "")

    def xml_request(self):
        return PackData(0x1, self.user_id, "")

    def xml_upload(self, xmldata): #string
        return PackData(0x4, self.user_id, xmldata)

    def xml_lock(self): #allow modify
        return PackData(0x3, self.user_id, "")

    def hash_request(self):
        return PackData(0x2, self.user_id, "")

    def UnpackData(self, pack) :
        fmt1 = "<BBHH"
        (mod, userid_len, data_offset, data_len) = struct.unpack(fmt1, pack[0:6])
        fmt2 = "<BBHH%ds%ds" % (userid_len, data_len)
        (mod, userid_len, data_offset, data_len, userid, data) = struct.unpack(fmt2, pack)
        return (mod, userid, data)








