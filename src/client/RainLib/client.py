from rainprotocol import RainPacketBuilder
import socket
import time


class RainClient(object):
    def __init__(self,user_id,rain_drive):
        self.rain_drive = rain_drive
        self.user_id = user_id
        self.packet_builder = RainPacketBuilder(self.user_id)

    def login(self):
        clientsocket = socket(AF_INET, SOCK_STREAM)
        addr = ("plus7.postech.ac.kr", 1287)
        bufsize = 1024
      
        try :
          clientsocket.connect(addr)
        except :
          print ("don't reach (%s:%s)" % addr)
        
        clientsocket.send(self.packet_builder.login())
        xml_content = self.recv_timeout(clientsocket)
        xml = open("metafile.xml", "w")
        xml.write(xml_content)
        xml.close()

        #pass

    def check_hash(self):
        pass

    def update_xml(self):
        pass

    def recv_timeout(self, sock, timeout = 2):
      sock.setblocking(0)

      total_data=[]
      data = ''

      begin = time.time()
      while 1:
        if total_data and time.time()-begin > timeout :
          break

        elif time.time()-begin > timeout * 2:
          break

        try :
          data = sock.recv(8192)
          if data:
            total_data.append(data)
            begin = time.time()
          else:
            time.sleep(0.1)

        except:
          pass

      return ''.join(total_data)











