import time
from collections import deque
from kafka import KafkaProducer


# kafka 消息生产者
class KafkaMessageProducer:
    def __init__(self, bootstrap_servers, topic):
        self.producer = KafkaProducer(
            bootstrap_servers = bootstrap_servers,
            api_version = (0, 10),
            max_request_size = 20 * 1024 * 1024,
            acks = 0,  # 不等待确认
            max_in_flight_requests_per_connection=100,  # 控制最大同时未确认的请求
        )
        self.topic = topic

        self.traj_data_queue = deque()
        self.flag_stop_send = False

    # 放数据
    def put_data(self, traj_data):
        self.traj_data_queue.append(traj_data)

    # 发数据
    def send_message(self, ):
        while True:
            if not self.traj_data_queue.empty():
                try:
                    message = self.traj_data_queue.popleft()
                    self.producer.send(self.topic, message.encode('utf-8'))
                    print(f"消息发送成功.")
                except Exception as e:
                    print(f"发送消息时发生错误：{e}")
            time.sleep(0.01)
            if self.flag_stop_send:
                break

    # 关闭
    def close(self):
        self.producer.close()
