import socket
import time
import struct
from udp_pack_def import UdpPack

UDP_IP = "192.168.1.187"
UDP_PORT = 6001
MESSAGE = b"Hello, World!"
head_len = 16

def reverse_bytes(byte_obj):
    reversed_bytes = byte_obj[::-1]
    return reversed_bytes

def udp_unassemble(udp_data):
    fmt = "QHHI" + str(len(udp_data) - head_len) + "s"
    timestamp, msg_id, msg_count, msg_size, data = struct.unpack(fmt, udp_data)
    print("udp: ts: {}, id: {}, count: {}, size: {}".format(hex(timestamp), hex(msg_id), hex(msg_count), hex(msg_size)))
    # t_bts = reverse_bytes(udp_data[0:8])
    # print(f"{udp_data[0:8]}")
    # print(f"{t_bts}")
    # r_ts = struct.unpack("Q", t_bts)
    # print(f"reverse ts {r_ts}")


print("UDP target IP: %s" % UDP_IP)
print("UDP target port: %s" % UDP_PORT)
print("message: %s" % MESSAGE)

udp_pack = UdpPack()
sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind(("", UDP_PORT))

while True:
    msg, addr  = sock.recvfrom(32000)
    udp_unassemble(msg)
    print("Msg recv: {}".format(len(msg)))

