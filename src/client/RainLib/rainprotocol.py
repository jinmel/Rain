from socket import *

RAIN_REMOTE_PATH = '/Rain/'

class RainProtocol():
     @staticmethod
     def PackData(mod,userid,data):
	#return sendabledata
	raise NotImplemented


     @staticmethod
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
	
	msg=RainProtocol.PackData(mod,userid,data)
	totalsent = 0
	msglen=len(msg)
        while totalsent < MSGLEN:
            sent = self.sock.send(msg[totalsent:])
            if sent == 0:
                raise RuntimeError("socket connection broken")
            totalsent = totalsent + sent
	
	header=RainProtocol.RecvData(6)
	mod,idlen,Dataoffset,DataLen=RainProtocol.UnpackHeader(header)
	RainProtocol.RecvData(Dataoffset-6)
	realData=RainProtocol.RecvData(DataLen)
		
	sock.close()
	return realData


