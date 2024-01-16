import struct

class Fusion_Vector3d(object):
    def __init__(self, vec3d_data):
        self.x, self.y, self.z = struct.unpack("3f", vec3d_data)

    def __str__(self):
        return f"({self.x}, {self.y}, {self.z})"

class FusionObjectInfo(object):
    def __init__(self, object_data):
        self.obj_id, = struct.unpack("I", object_data[0:4])
        self.life_time, = struct.unpack("Q", object_data[4:12])
        self.confidence, = struct.unpack("f", object_data[12:16])
        self.class_type, = struct.unpack("b", object_data[16:17])
        self.class_type_confidence, = struct.unpack("f", object_data[20:24])
        # 
        self.center = Fusion_Vector3d(object_data[24:36])
        self.center_rms = Fusion_Vector3d(object_data[36:48])
        self.abs_vel = Fusion_Vector3d(object_data[48:60])
        self.abs_vel_rms = Fusion_Vector3d(object_data[60:72])
        #
        self.abs_acc = Fusion_Vector3d(object_data[72:84])
        self.abs_acc_rms = Fusion_Vector3d(object_data[84:96])
        self.size = Fusion_Vector3d(object_data[96:108])
        self.size_rms = Fusion_Vector3d(object_data[108:120])
        #
        self.corner_left_front = Fusion_Vector3d(object_data[120:132])
        self.corner_right_front = Fusion_Vector3d(object_data[132:144])
        self.corner_left_rear = Fusion_Vector3d(object_data[144:156])
        self.corner_right_rear = Fusion_Vector3d(object_data[156:168])
        #
        self.orientation_angle, = struct.unpack("f", object_data[168:172])
        self.orientation_rms, = struct.unpack("f", object_data[172:176])
        self.motion_status, = struct.unpack("b", object_data[176:177])
        self.measured_source, = struct.unpack("b", object_data[177:178])
        self.meas_state, = struct.unpack("b", object_data[178:179])
        self.cipv_id, = struct.unpack("I", object_data[180:184])

    def __str__(self):
        # ret_str = f"object:\n"
        ret_str = f"obj_id {hex(self.obj_id)} \nlife_time {hex(self.life_time)} \nconfidence {self.confidence} \nclass_type {hex(self.class_type)} \nclass_type_confidence {self.class_type_confidence}\n"
        ret_str += f"center {self.center} \ncenter_rms {self.center_rms} \nabs_vel {self.abs_vel} \nabs_vel_rms {self.abs_vel_rms}\n"
        ret_str += f"abs_acc {self.abs_acc} \nabs_acc_rms {self.abs_acc_rms} \nsize {self.size} \nsize_rms {self.size_rms}\n"
        ret_str += f"corner_left_front {self.corner_left_front} \ncorner_right_front {self.corner_right_front}\n"
        ret_str += f"corner_left_rear {self.corner_left_rear} \ncorner_right_rear {self.corner_right_rear}\n"
        ret_str += f"orientation_angle {self.orientation_angle} \norientation_rms {self.orientation_rms} \nmotion_status {hex(self.motion_status)}\n"
        ret_str += f"measured_source {hex(self.measured_source)} \nmeas_state {hex(self.meas_state)} \ncipv_id {hex(self.cipv_id)}\n"
        return ret_str


class FusionHeader(object):
    def __init__(self, header_dsata):
        self.timestamp, self.rolling_counter, self.obj_num = struct.unpack("QII", header_dsata)

    def __str__(self):
        return f"header:\n{hex(self.timestamp)}, {hex(self.rolling_counter)}, {hex(self.obj_num)}\n"


HEAD_SIZE = 16
OBJ_SIZE = 184
class FusionObjectList(object):
    def __init__(self, udp_data):
        self.header = FusionHeader(udp_data[0:HEAD_SIZE])
        self.objs = []
        for i in range(64):
            s_idx = HEAD_SIZE + i * OBJ_SIZE
            e_idx = s_idx + OBJ_SIZE
            self.objs.append(FusionObjectInfo(udp_data[s_idx:e_idx]))

    def __str__(self):
        ret_str = f"{self.header}"
        obj_idx = 0
        for obj in self.objs:
            ret_str += f"*********************************************************\n"
            ret_str += f"object {obj_idx}:\n{obj}"
            obj_idx = obj_idx + 1
        ret_str += f"\n"

        return ret_str