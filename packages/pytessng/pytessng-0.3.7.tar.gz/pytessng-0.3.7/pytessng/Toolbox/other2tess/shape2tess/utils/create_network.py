from .config import LANE_TYPE_MAPPING
from .functions import get_coo_list
try:
    from .....Tessng.MyMenu import ProgressDialog as pgd
except:
    class pgd: progress = lambda values, text="": values


def create_network(netiface, links_info, connectors_info, other_info):
    netiface.setNetAttrs("Shapefile Network", otherAttrsJson=other_info)
    print("Network attrs: ", netiface.netAttrs().otherAttrs())
    
    width, height = 600, 400

    error_links = []
    error_connector = []
    
    # 创建路段
    for road_id in pgd.progress(links_info, "创建路段中（7/8）"):
        link_info = links_info[road_id]
        link_type = []
        
        # 获取车道点位
        lanesWithPoints = []
        for lane_id, lane in link_info["lanes_data"].items():
            points = lane["points"]
            lane_type = LANE_TYPE_MAPPING.get(lane["type"], '机动车道')
            link_type.append(lane_type)
            try:
                lanesWithPoints.append({
                    'left': get_coo_list(points['left']),
                    'center': get_coo_list(points['center']),
                    'right': get_coo_list(points['right']),
                })
            except Exception as e:
                error_links.append(f"{road_id}-{lane_id}")
                print(str(e))
                continue
            
            # 场景宽度和高度
            width = max(width, max([abs(p[0]) for p in points["left"]]))
            height = max(height, max([abs(p[1]) for p in points["left"]]))
        
        # 获取路段点位
        # 如果是奇数，取中间车道的中心线
        laneCount = len(lanesWithPoints)
        if laneCount % 2 == 1:
            lCenterLinePoint = lanesWithPoints[int((laneCount-1)/2)]["center"]
        # 如果是偶数，取中间两车道的边线
        else:
            lCenterLinePoint = lanesWithPoints[int(laneCount/2)]["right"]
        
        # 创建路段及车道
        link_obj = netiface.createLink3DWithLanePoints(lCenterLinePoint, lanesWithPoints)
        if link_obj:
            link_obj.setName(f"shp_road_id: {road_id}")
            link_obj.setLaneTypes(link_type)
            links_info[road_id]['obj'] = link_obj
        else:
            error_links.append(f"{road_id}-all")
    
    # 设置场景宽度和高度
    netiface.setSceneSize(width*2+20, height*2+20) # (m)
        
    # 创建连接段
    for connector_road_tuple, connector_info in pgd.progress(connectors_info.items(), "创建连接段中（8/8）"):
        from_link = links_info[connector_road_tuple[0]]['obj']
        to_link = links_info[connector_road_tuple[1]]['obj']
        
        from_link_id, to_link_id = from_link.id(), to_link.id()
        
        from_lane_numbers, to_lane_numbers, lanesWithPoints3 = [], [], []
        for connector in connector_info:
            from_lane_numbers.append(connector['from_lane_number'])
            to_lane_numbers.append(connector['to_lane_number'])
            if connector.get('points'):
                points = connector['points']
                lanesWithPoints3.append(
                    {
                        "center": get_coo_list(points['center']),
                        "left": get_coo_list(points['left']),
                        "right": get_coo_list(points['right']),
                    }
                )

        try:
            if all(lanesWithPoints3):
                netiface.createConnector3DWithPoints(from_link_id, to_link_id, from_lane_numbers, to_lane_numbers,
                                                     lanesWithPoints3, f"{from_link_id}-{to_link_id}")
            else:
                netiface.createConnector(from_link_id, to_link_id, from_lane_numbers, to_lane_numbers)
        except:
            error_connector.append(connector_road_tuple)

    if error_links or error_connector:
        error_message = f"创建失败的路段：{error_links}\n创建失败的连接段：{error_connector}"
        print(error_message)
