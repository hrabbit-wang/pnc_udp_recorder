#
import time
import socket
import sys
import os
from udp_pack_def import UdpPack

max_struct_byte = 32 * 1024

class UdpRecorder(object):
    def __init__(self, server_ip, bind_port) -> None:
        self.client_ = None
        # create socket connection
        self.bind_server(server_ip, bind_port)

    def bind_server(self, ip, port):
        self.client_ = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client_.bind((ip, port))

    def receive(self):
        # always receive data
        while True:
            try:
                msg, addr  = self.client_.recvfrom(max_struct_byte)

                udp_pack = UdpPack()
                udp_pack.udp_unassemble(msg)
                # 
                print("receive udp pack {}".format(udp_pack))
                # time.sleep(3)
            except Exception as err:
                print("Error: {}".format(err))
                break
        self.client_.close()
        print("socket closed")

if __name__ == "__main__":
  if len(sys.argv) != 3:
  	print ("Usage: udp_recorder.py ip port")
  	exit(1)

  print("info {}, {}, {}".format(sys.argv[0], sys.argv[1], sys.argv[2]))
  udp_rec = UdpRecorder(sys.argv[1], int(sys.argv[2]))
  udp_rec.receive()
