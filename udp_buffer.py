#
import time
from threading import Thread
from udp_pack_def import UdpPack

class UdpPackBuffer(object):
    def __init__(self, buffer_duration, save_dir):
        self.datas_ = {}
        self.exit_ = False
        self.triggers_ = []
        self.save_dir_ = save_dir
        self.bd_ = int(buffer_duration * 1.1)
        self.save_proc = Thread(target=self.save_thread, args=())
        self.save_proc.start()

    def set_save_dir(self, save_dir):
        self.save_dir_ = save_dir

    def exit(self):
        self.exit_ = True
        self.save_proc.join()

    def save(self, trigger):
        print("Trigger [{}, {}] saved !!!!!!".format(trigger[0], trigger[1]))
        pass

    def save_thread(self):
        while not self.exit_:
            if len(self.triggers_) > 0:
                last_time = list(self.datas_.keys())[-1]
                # print("time infos {}, {}".format(last_time, self.triggers_[0]))
                if last_time > self.triggers_[0][1]:
                    # save to file
                    self.save(self.triggers_[0])
                    # remove the saved trigger
                    self.triggers_.pop(0)
            # sleep a little
            # print("save threading !!!")
            time.sleep(0.5)

    def ms_to_s(self, timestamp):
        return int(timestamp / 1000)

    def add(self, udp_pack):
        time_s = self.ms_to_s(udp_pack.timestamp_)
        keys = list(self.datas_.keys())
        if time_s not in keys:
            self.datas_[time_s] = []
        self.datas_[time_s].append(udp_pack)
        # check if need to remove the oldest data
        if len(keys) > 0:
            delta_t = time_s - keys[0]
            if delta_t > self.bd_:
                self.datas_.pop(keys[0])
        
        # keys = list(self.datas_.keys())
        # print("buf range {} : {}".format(keys[0], keys[-1]))

    def trigger(self, time_range):
        print("one trigger added !!!")
        self.triggers_.append(time_range)
