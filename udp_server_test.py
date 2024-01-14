import socket
import time
from udp_pack_def import UdpPack

UDP_IP = "192.168.1.246"
UDP_PORT = 5005
MESSAGE = b"Hello, World!"
 
print("UDP target IP: %s" % UDP_IP)
print("UDP target port: %s" % UDP_PORT)
print("message: %s" % MESSAGE)

udp_pack = UdpPack()
udp_data = udp_pack.udp_assemble(1123, 32, MESSAGE)

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
while True:
    sock.sendto(udp_data, (UDP_IP, UDP_PORT))
    print("Msg sent: {}".format(udp_pack))
    time.sleep(1)

