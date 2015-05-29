from socket import *

RAIN_REMOTE_PATH = '/Rain/'


def PackData(mod, userid, data):
    fmt="<BBHH%ds%ds" % (len(userid),len(data))
    return struct.pack(fmt,mod,len(userid),len(userid+6),len(data),userid,data)


def UnPackHeader(header):
    #return mod,useridlen, Dataoffset,DataLenth
    raise NotImplemented


def RecvData(sock, lenth):
    chucks = []
    bytes_recd = 0
    msglen = lenth
    while bytes_recd < msglen:
        chunk = sock.recv(min(msglen - bytes_recd, 2048))
        if chunk == '':
            raise RuntimeError("socket connection broken")
        chunks.append(chunk)
        bytes_recd = bytes_recd + len(chunk)
    return ''.join(chunks)


def SendAndRecv(mod, userid, data, port=8787, host="plus.or.kr"):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.connet((host, port))

    msg = RainProtocol.PackData(mod, userid, data)
    totalsent = 0
    msglen = len(msg)
    while totalsent < msglen:
        sent = self.sock.send(msg[totalsent:])
        if sent == 0:
            raise RuntimeError("socket connection broken")
        totalsent = totalsent + sent

    header = RainProtocol.RecvData(6)
    mod, idlen, Dataoffset, DataLen = RainProtocol.UnpackHeader(header)
    RainProtocol.RecvData(Dataoffset - 6)
    realData = RainProtocol.RecvData(DataLen)

    sock.close()
    return realData


class RainPacketBuilder(object):
    def __init__(self, user_id):
        self.user_id = user_id

    def login(self):
        return PackData(0x0, self.user_id, "")

    def xml_request(self): 
        return PackData(0x1, self.user_id, "")

    def xml_upload(self,xmldata): #string
        return PackData(0x4, self.user_id, xmldata)

    def xml_lock(self): #allow modify
        return PackData(0x3, self.user_id,"")

    def hash_request(self):
        return PackData(0x2, self.user_id,"")









