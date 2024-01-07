def osm2tess(netiface, params):
    # params:
    # - osm_file_path
    # - bounding_box
    # - center_point
    # - proj_mode

    osm_params = {
        "osm_file_path": params.get("osm_file_path"),
        "bounding_box": params.get("bounding_box"),
        "center_point": params.get("center_point"),
        "road_class": params.get("road_class"),
        "proj_mode": None,
    }
    # print(osm_params)

    from .utils.my_class import OSMData, Network, NetworkCreator

    # 获取数据
    save_file_name = "" # 传入非空参数可保存为json文件
    osm_data = OSMData(osm_params).get_osm_data(save_file_name)
    # 解析数据
    network = Network(**osm_data)
    # network.draw()
    # 创建路网
    network_creator = NetworkCreator(netiface, network)
    print(network_creator.error_message)

