from socket import *

RAIN_REMOTE_PATH = '/Rain/'

class RainProtocall():
     @staticmethod
     def PackData(mod,userid,data):
	#return sendabledata
	raise NotImplemented


     def UnPackHeader(header) :
	#return mod,useridlen, Dataoffset,DataLenth
	raise NotImplemented

 
     @staticmethod
     def RecvData(sock,lenth):
	chucks=[]
	bytes_recd = 0 
	msglen=lenth
	while bytes_recd < msglen :
	    chunk = sock.recv(min(msglen - bytes_recd, 2048))
            if chunk == '':
                raise RuntimeError("socket connection broken")
            chunks.append(chunk)
            bytes_recd = bytes_recd + len(chunk)
	return ''.join(chunks)
	
	


     @staticmethod
     def SendAndRecv(mod,userid,data,port=8787,host="plus.or.kr"):
	sock=socket(AF_INET,SOCK_STREAM)
	sock.connet((host,port))
	
	msg=PackData(mod,userid,data)
	totalsent = 0
	msglen=len(msg)
        while totalsent < MSGLEN:
            sent = self.sock.send(msg[totalsent:])
            if sent == 0:
                raise RuntimeError("socket connection broken")
            totalsent = totalsent + sent
	
	header=RecvData(6)
	mod,idlen,Dataoffset,DataLen=UnpackHeader(header)
	RecvData(Dataoffset-6)
	realData=RecvData(DataLen)
		
	sock.close()
	return realData


