#
class UdpPack(object):
    def __init__(self) -> None:
        self.timestamp_ = 0
        self.msg_id_ = 0
        self.msg_count = 0
        self.msg_size = 0
        self.data_ = None


