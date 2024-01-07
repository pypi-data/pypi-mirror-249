import os
import sys
import shutil
from pathlib import Path
from PySide2.QtWidgets import QApplication

from pytessng.DLLs.Tessng import TessngFactory
from pytessng.Tessng.MyPlugin import MyPlugin


class TessngObject:
    def __init__(self, extension=False):
        # 加载之前
        self.before_load()
        # 初始化界面
        self.app = QApplication()
        self.config = {
            '__workspace': self.workspace_path, # 工作空间
            # '__netfilepath': "",
            '__simuafterload': False, # 加载路网后是否自动启动仿真
            '__custsimubysteps': False, # 是否自定义仿真调用频率
            '__allowspopup': False, # 禁止弹窗
            '__cacheid': True, # 快速创建路段
        }
        self.plugin = MyPlugin(extension)
        self.factory = TessngFactory()
        self.tessng = self.factory.build(self.plugin, self.config)
        # 启动
        self.run()

    def run(self, ):
        if self.tessng is not None:
            sys.exit(self.app.exec_())
        else:
            sys.exit()

    def before_load(self):
        # 工作空间是本进程所在的路径
        self.workspace_path = os.path.join(os.getcwd(), "WorkSpace")
        # 创建文件夹
        os.makedirs(self.workspace_path, exist_ok=True)

        # 试用版key的位置
        cert_file_path = os.path.abspath(Path(__file__).resolve().parent / "Files" / "Cert" / "JidaTraffic_key")
        # 复制key
        _cert_folder_path = os.path.join(self.workspace_path, "Cert")
        _cert_file_path = os.path.join(_cert_folder_path, "_cert")
        if not os.path.exists(_cert_file_path):
            new_cert_file_path = os.path.join(self.workspace_path, "Cert", "可使用本试用版密钥激活TESSNG")
            os.makedirs(_cert_folder_path, exist_ok=True)
            shutil.copy(cert_file_path, new_cert_file_path)

        # 导入样例的位置
        examples_file_path = os.path.abspath(Path(__file__).resolve().parent / "Files" / "Examples")
        new_examples_file_path = os.path.join(os.getcwd(), "WorkSpace", "Examples")
        try:
            shutil.copytree(examples_file_path, new_examples_file_path)
        except:
            pass
