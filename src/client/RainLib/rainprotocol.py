from socket import *

RAIN_REMOTE_PATH = '/Rain/'


def PackData(mod, userid, data):
    #return sendabledata
    raise NotImplemented


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
        pass

    def xml_request(self):
        pass

    def xml_upload(self):
        pass

    def xml_lock(self): #allow modify
        pass

    def hash_request(self):
        pass











