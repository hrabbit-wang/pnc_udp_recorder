#
import time
import socket
import sys
import os
from udp_pack_def import UdpPack
from udp_buffer import UdpPackBuffer


max_struct_byte = 32 * 1024
record_duration = 10
dur_before_trig = 4
dur_after_trig = 2

class UdpRecorder(object):
    def __init__(self, server_ip, bind_port) -> None:
        self.client_ = None
        self.record_duration_ = record_duration
        self.buf_ = UdpPackBuffer(self.record_duration_, "./")
        # create socket connection
        self.bind_server(server_ip, bind_port)
        self.exit_ = False

    def trigger_evt(self, time):
        time_s = time - dur_before_trig
        time_e = time + dur_after_trig
        self.buf_.trigger([time_s, time_e], time)

    def exit(self):
        self.exit_ = True
        self.buf_.exit()

    def set_save_dir(self, dir):
        self.buf_.set_save_dir(dir)

    def bind_server(self, ip, port):
        self.client_ = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client_.bind((ip, port))

    def receive(self):
        # always receive data
        while not self.exit_:
            try:
                msg, addr  = self.client_.recvfrom(max_struct_byte)
                udp_pack = UdpPack()
                udp_pack.udp_unassemble(msg)
                self.buf_.add(udp_pack)
                # 
                print("receive udp pack {}".format(udp_pack))
                # time.sleep(3)
            except Exception as err:
                print("Error: {}".format(err))
                break
        self.client_.close()
        print("socket closed")
