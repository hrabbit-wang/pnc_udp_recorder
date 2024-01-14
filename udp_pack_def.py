#
import struct

class UdpPack(object):
    def __init__(self) -> None:
        self.head_len_ = 16
        self.timestamp_ = 0
        self.msg_id_ = 0
        self.msg_count_ = 0
        self.msg_size_ = 0
        self.data_ = None

    def udp_unassemble(self, udp_data):
        fmt = "QII" + str(len(udp_data) - self.head_len_) + "s"
        self.timestamp_, self.msg_count_, self.msg_size_, self.data_ = struct.unpack(fmt, udp_data)
        print("udp: {}, {}, {}, {}".format(self.timestamp_, self.msg_count_, self.msg_size_, self.data_))

    def udp_assemble(self, timestamp, msg_count, data):
        self.timestamp_ = timestamp
        self.msg_count_ = msg_count
        self.msg_size_ = len(data)
        self.data_ = data
        
        fmt = "QII" + str(self.msg_size_) + "s"
        byte_date = struct.pack(fmt, self.timestamp_, self.msg_count_,
                                     self.msg_size_, self.data_)
        return byte_date

    def __str__(self):
        return f"{self.timestamp_}, {self.msg_count_}, {self.msg_size_}, {self.data_}"