import os
import pandas as pd
try:
    from .....Tessng.MyMenu import ProgressDialog as pgd
except:
    class pgd: progress = lambda values, text="": values


# 获取路段信息
def get_data(file_path):
    # 获取文件后缀
    _, extension = os.path.splitext(file_path)
    # 读取文件
    if extension == ".csv":
        try:
            data = pd.read_csv(file_path, encoding="utf-8")
        except:
            data = pd.read_csv(file_path, encoding="gbk")
    elif extension in [".xlsx", ".xls"]:
        data = pd.read_excel(file_path)
    else:
        raise Exception("Invaild file format !")

    # 保存路段信息
    links_data = {}
    ID = 1
    for col in pgd.progress(data.to_numpy(), '路段数据解析中（1/2）'):
        link_name = col[0] if col[0] else ID
        link_count = int(col[1])
        link_points = [list(map(float, j.split(","))) for j in col[2:] if str(j) != "nan"]
        links_data[ID] = {
            "link_name": link_name,
            "link_count": link_count,
            "link_points": link_points
        }
        ID += 1

    return links_data