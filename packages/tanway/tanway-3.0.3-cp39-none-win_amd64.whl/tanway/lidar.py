import _tanway
from tanway.point_cloud import PointCloud
class Lidar:
    def __init__(self):
        self.__impl = _tanway.LidarDevice()
        self.lidar_types = {
            "TensorLite": 0,
            "Tensor16": 1,
            "TensorPro_echo2": 2,
            "Scope64": 3,
            "Tensor32": 4,
            "Scope192": 5,
            "DuettoA1": 6,
            "DuettoA2": 7,
            "ScopeMiniA2_192": 8,
            "TempoA1": 9,
            "TempoA2": 10,
            "TempoA3": 11,
            "Tensor48_Polar": 12,
            "Tensor48_Depth": 13,
            "Scope256_Polar": 14,
            "Scope256_Depth": 15,
            "Focus": 16,
            "TempoA2H": 17,
        }

    def __str__(self):
        return str(self.__impl)
    
    def create_online(self, lidarIP, localIP, local_pointloud_port, local_dif_port, lidar_type):
        try:
            lidar_type_class = self.lidar_types[lidar_type]
        except KeyError as ex:
            raise ValueError(
                "Unsupported data format: {lidar_type}. Supported formats: {all_formats}".format(
                    lidar_type=lidar_type, all_formats=list(self.lidar_types.keys())
                )
            ) from ex
        
        return self.__impl.create_online(lidarIP, localIP, local_pointloud_port, local_dif_port, lidar_type_class)
    
    def create_offline(self, pcap_path, lidarIP, local_pointloud_port, local_dif_port, lidar_type, repeat):      
        try:
            lidar_type_class = self.lidar_types[lidar_type]
        except KeyError as ex:
            raise ValueError(
                "Unsupported data format: {lidar_type}. Supported formats: {all_formats}".format(
                    lidar_type=lidar_type, all_formats=list(self.lidar_types.keys())
                )
            ) from ex
        
        return self.__impl.create_offline(str(pcap_path), str(lidarIP), local_pointloud_port, local_dif_port, lidar_type_class, repeat)

    def start(self):
        return self.__impl.start()
    
    def stop(self):
        return self.__impl.stop()
    
    def set_distance_range(self, min, max):
        return self.__impl.set_distance_range(min, max)

    def parse_algo_config(self, algo_config):
        return self.__impl.parse_algo_config(algo_config)
    
    def capture(self):
        return PointCloud(self.__impl.capture())