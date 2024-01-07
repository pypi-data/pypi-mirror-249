# 拉取的路段类型
road_class_type = {
    1: ["motorway", "motorway_link"],
    2: ["motorway", "motorway_link", "trunk", "primary", "secondary", "tertiary"],
}

# 默认路段类型等级
default_road_class = 3

# 不同道路类型的默认车道数
default_lane_count = {
    "motorway": 3,
    "motorway_link": 1,
    "trunk": 3,
    "primary": 3,
    "secondary": 2,
    "tertiary": 2,
    }

# 车道宽度
default_lane_width = 3.5

# osm json数据保存路径
import os
# 这个路径需要按照需求修改
# osm_data_save_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "WorkSpace", "Data", "osm_data")
osm_data_save_path = os.path.join(os.getcwd(), "WorkSpace", "Data", "osm_data")
osm_data_before_process_save_path = os.path.join(osm_data_save_path, "before_process")
osm_data_after_process_save_path = os.path.join(osm_data_save_path, "after_process")
