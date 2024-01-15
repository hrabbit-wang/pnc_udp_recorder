#
import time
import numpy as np
from threading import Thread
from udp_pack_def import UdpPack


class UdpPackBuffer(object):
    def __init__(self, buffer_duration, save_dir):
        self.datas_ = {}
        self.exit_ = False
        self.triggers_ = {}
        self.save_dir_ = save_dir
        self.bd_ = int(buffer_duration * 1.1)
        self.save_proc = Thread(target=self.save_thread, args=())
        self.save_proc.start()

    def set_save_dir(self, save_dir):
        self.save_dir_ = save_dir

    def exit(self):
        self.exit_ = True
        self.save_proc.join()

    def save(self, trigger_time, trigger):
        # save to file
        file_name = self.save_dir_ + "/evt_trigger_{}.txt".format(trigger_time)
        save_data = {
            'Veh_CAN_Inputs': bytearray(), 'CAM_CAN_Inputs': bytearray(), 'FusionObjects_Com': bytearray(), 'TFL_message': bytearray(),
            'ADAS_Inputs': bytearray(), 'EM_Outputs': bytearray(), 'FCT_Outputs': bytearray(), 'PLN_Outpus': bytearray(),
            'CTRL_Outputs': bytearray(), 'AdptrOut_ADS2VEH': bytearray(), 'AdptrOut_ADS2HMI': bytearray(), 'AdptrOut_Out2In': bytearray(),
            'FCT_Measurement': bytearray(), 'PLN_Measurement': bytearray(), 'CTRL_Measurement': bytearray()
        }
        id_name_mapping = {
            0x0001: 'Veh_CAN_Inputs', 0x0002: 'CAM_CAN_Inputs', 0x0003: 'FusionObjects_Com', 0x0004: 'TFL_message',
            0x0005: 'ADAS_Inputs', 0x0006: 'EM_Outputs', 0x0007: 'FCT_Outputs', 0x0008: 'PLN_Outpus',
            0x0009: 'CTRL_Outputs', 0x0010: 'AdptrOut_ADS2VEH', 0x0011: 'AdptrOut_ADS2HMI', 0x0012: 'AdptrOut_Out2In',
            0x0013: 'FCT_Measurement', 0x0014: 'PLN_Measurement', 0x0015: 'CTRL_Measurement'
        }
        # ref: https://u0x5270897.feishu.cn/docx/IGdfdoatGoESLNx3iQhcmOENnMe
        for t in range(trigger[0], trigger[1]):
            if t in self.datas_.keys():
                for udp_pack in self.datas_[t]:
                    save_data[id_name_mapping[udp_pack.msg_id_]].extend(udp_pack.data_)
        # save to file
        np.save(file_name, save_data)
        print("Trigger [{}, {}] saved !!!!!!".format(trigger[0], trigger[1]))

    def save_thread(self):
        while not self.exit_:
            if len(self.triggers_) > 0:
                last_time = list(self.datas_.keys())[-1]
                # print("time infos {}, {}".format(last_time, self.triggers_[0]))
                key_to_save = list(self.triggers_.keys())[0]
                if last_time > self.triggers_[key_to_save][1]:
                    # save to file
                    self.save(key_to_save, self.triggers_[key_to_save])
                    # remove the saved trigger
                    self.triggers_.pop(key_to_save)
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

    def trigger(self, time_range, time_trigger):
        print("one trigger added !!!")
        self.triggers_[time_trigger] = time_range
