import os
import time
import copy
import json
import threading
from queue import Queue
from datetime import datetime
from pyproj import Proj
from PySide2.QtCore import QObject, Signal, QCoreApplication

from ..DLLs.Tessng import PyCustomerSimulator, tessngIFace, p2m
from ..Toolbox.traj_output.get_traj_data import get_traj_data
from ..Toolbox.traj_output.kafka_producer import KafkaMessageProducer
from ..Tessng.MyMenu import GlobalVar


class MySimulator(QObject, PyCustomerSimulator):
    signalRunInfo = Signal(str)
    forStopSimu = Signal()
    forReStartSimu = Signal()

    def __init__(self):
        QObject.__init__(self)
        PyCustomerSimulator.__init__(self)

        # 投影关系
        self.traj_proj = None
        self.traj_move = None
        # JSON 保存路网
        self.json_save_path = None
        # Kafka 生产者和发送线程
        self.kafka_producer = None
        self.kafka_send_thread = None
        # 数据队列
        self.queue = Queue()
        self.send_data_thread = None
        self.flag_send_data = False

    # 仿真开始前
    def ref_beforeStart(self, ref_keepOn):
        iface = tessngIFace()
        simuiface = iface.simuInterface()
        netiface = iface.netInterface()
        # # 设置仿真精度
        # simuiface.setSimuAccuracy(5)

        # 投影
        traj_proj_string = GlobalVar.traj_proj_string
        if traj_proj_string:
            self.traj_proj = Proj(traj_proj_string)
        else:
            self.traj_proj = lambda x,y,inverse: (None,None)

        # move
        move = netiface.netAttrs().otherAttrs().get("move_distance")
        if move is None or "tmerc" in traj_proj_string:
            self.traj_move = {"x_move": 0, "y_move": 0}
        else:
            self.traj_move = {"x_move": -move["x_move"], "y_move": -move["y_move"]}

        # JSON
        traj_json_config = GlobalVar.traj_json_config
        if traj_json_config:
            current_time = datetime.now()
            formatted_time = current_time.strftime("%Y%m%d%H%M%S")
            folder_path = os.path.join(traj_json_config, f"轨迹数据_{formatted_time}")
            # 创建文件夹
            os.makedirs(folder_path, exist_ok=True)
            self.json_save_path = os.path.join(folder_path, "{}.json")

        # Kakfa
        traj_kafka_config = GlobalVar.traj_kafka_config
        if traj_kafka_config:
            ip = traj_kafka_config["ip"]
            port = traj_kafka_config["port"]
            topic = traj_kafka_config["topic"]
            self.kafka_producer = KafkaMessageProducer(f"{ip}:{port}", topic)
            # 使用线程来发送，不会阻塞主进程，不知道是否发送成功
            self.kafka_send_thread = threading.Thread(target=self.kafka_producer.send_message, args=())
            self.kafka_send_thread.start()

        # 发送队列
        if traj_json_config or traj_kafka_config:
            self.flag_send_data = True
            self.send_data_thread = threading.Thread(target=self.send_data, args=())
            self.send_data_thread.start()

    # 仿真结束后
    def afterStop(self):
        # 投影关系
        self.traj_proj = None
        # JSON
        self.json_save_path = None
        # Kafka
        if self.kafka_producer:
            if self.kafka_send_thread:
                self.kafka_producer.flag_stop_send = True
                self.kafka_send_thread.join()
                self.kafka_send_thread = None
            self.kafka_producer.close()
            self.kafka_producer = None
        # 发送线程
        if self.send_data_thread:
            self.flag_send_data = False
            self.send_data_thread.join()
            self.send_data_thread = None
        self.queue.queue.clear()

    # 每帧仿真后
    def afterOneStep(self):
        iface = tessngIFace()
        simuiface = iface.simuInterface()

        # 如果不需要导出，就不需要计算
        if not self.json_save_path and not self.kafka_producer:
            return

        # 当前正在运行车辆列表
        lAllVehi = simuiface.allVehiStarted()
        # 当前仿真计算批次
        batchNum = simuiface.batchNumber()
        # 当前已仿真时间，单位：毫秒
        simu_time = simuiface.simuTimeIntervalWithAcceMutiples()
        # 开始仿真的现实时间戳，单位：毫秒
        start_time = simuiface.startMSecsSinceEpoch()

        # 把数据放入队列
        self.queue.put_nowait(copy.copy([lAllVehi, batchNum, simu_time, start_time]))


    # 发送数据的线程
    def send_data(self,):
        # return
        while True:
            time.sleep(0.001)
            if self.queue.empty():
                if self.flag_send_data:
                    continue
                elif not self.flag_send_data:
                    break
            print("qsize:", self.queue.qsize())
            # 从队列中取出数据
            try:
                lAllVehi, batchNum, simu_time, start_time = self.queue.get_nowait()
            except:
                continue
            self.send_data_function(lAllVehi, batchNum, simu_time, start_time)
        print("Sending data thread is stopping!")

    # 发送数据的函数
    def send_data_function(self, lAllVehi, batchNum, simu_time, start_time):
        t1 = time.time()
        # 轨迹数据计算和导出
        traj_data = get_traj_data(lAllVehi, simu_time, start_time, self.traj_proj, p2m, self.traj_move)

        t2 = time.time()
        # 需要保存为json
        if self.json_save_path:
            # 当前仿真计算批次
            file_path = self.json_save_path.format(batchNum)
            try:
                # 将JSON数据写入文件
                with open(file_path, 'w', encoding="utf-8") as file:
                    json.dump(traj_data, file, indent=4, ensure_ascii=False)
            except:
                pass

        t3 = time.time()
        # 需要上传至kafka
        if self.kafka_producer:
            traj_data_json = json.dumps(traj_data)
            self.kafka_producer.put_data(traj_data_json)

        t4 = time.time()
        clac_time = round((t2 - t1) * 1000, 1)
        json_time = round((t3 - t2) * 1000, 1)
        kafka_time = round((t4 - t3) * 1000, 1)
        print(f"仿真批次：{batchNum}，计算时间：{clac_time}ms，导出时间：{json_time}ms，上传时间：{kafka_time}ms")
