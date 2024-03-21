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
        self.cap = cv2.VideoCapture(8)
        while True:
            ret, frame = self.cap.read()
            if ret:
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgbImage.shape
                bytesPerLine = ch * w
                convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
                p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                self.changePixmap.emit(p)

class StartRviz():
    def __init__(self):
        self.frame = rviz.VisualizationFrame()
        self.frame.setSplashPath( "" )
        self.frame.initialize()
        reader = rviz.YamlConfigReader()
        config = rviz.Config()
        reader.readFile( config, "rs.rviz" )
        self.frame.load( config )
        self.frame.setMenuBar( None )
        self.frame.setStatusBar( None )
        self.frame.setHideButtonVisibility( False )
        self.manager = self.frame.getManager()
        self.grid_display = self.manager.getRootDisplayGroup().getDisplayAt( 0 )


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def setImage(self, image):
        self.image_label.setPixmap(QPixmap.fromImage(image))

    def initUI(self):
        
        self.setWindowTitle('Test App')
        self.resize(3200, 2000)
        self.label = QLabel(self)

        th = Thread(self)
        th.changePixmap.connect(self.setImage)
        th.start()

        rviz = start_rviz.frame

        layout = QVBoxLayout()
        self.setLayout(layout)
        rviz_tab = QWidget()

        tabwidget = QTabWidget()


        self.image_tab = QWidget()
        self.image_label = QLabel()
        self.image_tab_layout = QVBoxLayout()

        self.image_tab_layout.addWidget(self.image_label)

        self.rviz_frame = QLabel()
        rviz_tab_layout = QVBoxLayout()
        rviz_tab_layout.addWidget(rviz)

        self.image_tab.setLayout(self.image_tab_layout)
        rviz_tab.setLayout(rviz_tab_layout)

        tabwidget.addTab(self.image_tab, "CameraWindow")
        tabwidget.addTab(rviz_tab, "RvizWindow")

        layout.addWidget(tabwidget)

        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setFixedSize(640, 480)
        self.image_label.setStyleSheet("background-color: #222b33;")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    start_rviz = StartRviz()
    ex = App()
    ex.show()
    app.exec()
