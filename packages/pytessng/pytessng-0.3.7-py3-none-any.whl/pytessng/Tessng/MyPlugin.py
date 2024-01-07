from functools import partial

from ..DLLs.Tessng import TessPlugin, tessngIFace
from ..Tessng.MyMenu import MyMenu
from ..Tessng.MyNet import MyNet
from ..Tessng.MySimulator import MySimulator


class MyPlugin(TessPlugin):
    def __init__(self, extension):
        super(MyPlugin, self).__init__()
        self.mNetInf = None
        self.mSimuInf = None

        # 功能拓展
        self.extension = extension

    def initGui(self):
        iface = tessngIFace()
        guiiface = iface.guiInterface()

        # 增加菜单及菜单项
        menuBar = guiiface.menuBar()
        my_menu = MyMenu(menuBar, extension=self.extension)
        menuBar.addAction(my_menu.menuAction())

    # 过载父类方法，在 TESS NG工厂类创建TESS NG对象时调用
    def init(self):
        self.initGui()
        self.mNetInf = MyNet()
        self.mSimuInf = MySimulator()

    # 过载父类方法，返回插件路网子接口，此方法由TESS NG调用
    def customerNet(self):
        return self.mNetInf

    #过载父类方法，返回插件仿真子接口，此方法由TESS NG调用
    def customerSimulator(self):
        return self.mSimuInf


