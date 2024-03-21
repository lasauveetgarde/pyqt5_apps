import cv2
import roslib; roslib.load_manifest('rviz_python_tutorial')
import sys
from rviz import bindings as rviz
import rospy
import numpy as np
from PyQt5.QtWidgets import  QWidget, QLabel, QApplication, QVBoxLayout, QTabWidget
from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
from sensor_msgs.msg import CompressedImage
from cv_bridge import CvBridge, CvBridgeError


class Thread(QThread):
    changePixmap = pyqtSignal(QImage)

    def run(self):
        self.cap = cv2.VideoCapture(0)
        while True:
            ret, frame = self.cap.read()
            if ret:
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgbImage.shape
                bytesPerLine = ch * w
                convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
                p = convertToQtFormat.scaled(1080, 720, Qt.KeepAspectRatio)
                self.changePixmap.emit(p)

class StartRviz():
    def __init__(self):
        self.frame = rviz.VisualizationFrame()
        self.frame.setSplashPath( "" )
        self.frame.initialize()
        reader = rviz.YamlConfigReader()
        config = rviz.Config()
        reader.readFile( config, "turtle_bot.rviz" )
        self.frame.load( config )
        self.frame.setMenuBar( None )
        self.frame.setStatusBar( None )
        self.frame.setHideButtonVisibility( False )
        self.manager = self.frame.getManager()
        self.grid_display = self.manager.getRootDisplayGroup().getDisplayAt( 0 )
        self.frame_widget = self.manager._displayWidget()
        self.frame_widget.hide()

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def setImage(self, image):
        self.image_label_frst.setPixmap(QPixmap.fromImage(image))

    def initUI(self):
        
        self.setWindowTitle('Test App')
        self.resize(2000, 2000)
        self.label = QLabel(self)

        th = Thread(self)
        th.changePixmap.connect(self.setImage)
        th.start()

        rviz = start_rviz.frame

        layout = QVBoxLayout()
        self.setLayout(layout)
        rviz_tab = QWidget()

        self.image_label_frst = QLabel()
        self.image_tab_frst = QWidget()
        self.image_tab_layout_frst = QVBoxLayout()

        self.image_tab_layout_frst.addWidget(self.image_label_frst)

        self.rviz_frame = QLabel()
        rviz_tab_layout = QVBoxLayout()
        rviz_tab_layout.addWidget(rviz)

        self.image_tab_frst.setLayout(self.image_tab_layout_frst)
        rviz_tab.setLayout(rviz_tab_layout)

        tabwidget = QTabWidget()
        tabwidget.addTab(self.image_tab_frst, "CameraWindow")
        tabwidget.addTab(rviz_tab, "RvizWindow")

        layout.addWidget(tabwidget)

        self.image_label_frst.setFixedSize(1080, 720)
        self.image_label_frst.setStyleSheet("background-color: #222b33;")
        self.image_tab_layout_frst.setAlignment(Qt.AlignTop)
        self.image_tab_layout_frst.setContentsMargins(0, 0, 0, 0)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    start_rviz = StartRviz()
    ex = App()
    ex.show()
    app.exec()
