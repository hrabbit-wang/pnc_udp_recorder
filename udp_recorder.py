#
import time
import socket
import sys
import os


max_struct_byte = 6 * 1024

class UdpRecorder(object):
    def __init__(self) -> None:
        self.client_ = None

    def ConnectToServer(self, server_ip, bind_port):
        self.client_ = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # create socket connection
            self.client_.connect((server_ip, bind_port))
        except:
            print("Could not connected to {}:{}".format(server_ip, bind_port))
            return
        # always receive data
        while True:
            try:
                msg = self.client_.recvfrom(max_struct_byte)
                
                # 
                print("Delta time {}".format(cur_delta))
                # time.sleep(3)
            except:
                break
        self.client_.close()
        print("socket closed")
