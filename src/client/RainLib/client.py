from rainprotocol import RainPacketBuilder

class RainClient(object):
    def __init__(self,user_id,rain_drive):
        self.rain_drive = rain_drive
        self.user_id = user_id
        self.packet_builder = RainPacketBuilder(self.user_id)

    def login(self,user_id):
        pass

    def check_hash(self):
        pass

    def update_xml(self):
        pass













