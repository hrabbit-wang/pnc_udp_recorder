import socket
import time
import struct
from udp_pack_def import UdpPack
from udp_sf_unpack import FusionObjectList

UDP_IP = "192.168.1.187"
UDP_PORT = 6001
MESSAGE = b"Hello, World!"
head_len = 16

def reverse_bytes(byte_obj):
    reversed_bytes = byte_obj[::-1]
    return reversed_bytes

def udp_unassemble_obs_head(obs_head):
    fmt = "QII"
    ts, rc, num = struct.unpack(fmt, obs_head)
    print(f"fusion msg head {hex(ts)}, {hex(rc)}, {hex(num)}")

def udp_unassemble(udp_data):
    fmt = "QHHI" + str(len(udp_data) - head_len) + "s"
    timestamp, msg_id, msg_count, msg_size, data = struct.unpack(fmt, udp_data)
    print("udp: ts: {}, id: {}, count: {}, size: {}".format(hex(timestamp), hex(msg_id), hex(msg_count), hex(msg_size)))
    obj_list = FusionObjectList(data)
    print(f"{obj_list}")

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

