import cv2
import roslib; roslib.load_manifest('rviz_python_tutorial')
import sys
from rviz import bindings as rviz
import rospy
import numpy as np
from PyQt5.QtWidgets import  QWidget, QLabel,QHBoxLayout, QPushButton, QApplication, QVBoxLayout, QTabWidget, QGridLayout
from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap, QIcon
from sensor_msgs.msg import CompressedImage
from cv_bridge import CvBridge, CvBridgeError


class ThreadCam(QThread):
    changePixmap = pyqtSignal(QImage)

    def __init__(self, idx, parent=None):
        super().__init__(parent)
        self.cam_idx = idx

    def run(self):
        self.cap = cv2.VideoCapture(self.cam_idx)
        while True:
            ret, frame = self.cap.read()
            if ret:
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgbImage.shape
                bytesPerLine = ch * w
                convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
                p = convertToQtFormat.scaled(1080, 720, Qt.KeepAspectRatio)
                self.changePixmap.emit(p)
                if cv2.waitKey(1) == ord('q'):
                    break

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
        self.frame.setEnabled(False)
        self.frame.setHideButtonVisibility( False )
        self.manager = self.frame.getManager()
        self.grid_display = self.manager.getRootDisplayGroup().getDisplayAt( 0 )

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def setImageRow1(self, image):
        self.image_label_cam.setPixmap(QPixmap.fromImage(image))

    def setImageRow2(self, image):
        self.image_label_rs.setPixmap(QPixmap.fromImage(image))

    def initUI(self):
                
        self.setWindowTitle('Test App')
        self.resize(2000, 2000)

        th_cam1 = ThreadCam(0, self)
        th_cam1.changePixmap.connect(self.setImageRow1)
        th_cam1.start()

        self.image_label_cam = QLabel()
        self.image_label_rs = QLabel()

        rviz = start_rviz.frame

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.rviz_tab = QWidget()
        self.image_tab = QWidget()

        self.camera_button = QPushButton()
        self.info_button = QPushButton()
        self.camera_button.setLayout(QHBoxLayout())
        self.info_button.setLayout(QHBoxLayout())
        self.camera_button.layout().addWidget(QLabel("Stop", self))
        self.info_button.layout().addWidget(QLabel("Stop", self))
        self.camera_button.setFixedSize(200, 200)
        self.info_button.setFixedSize(200, 200)
        self.camera_button.setIcon(QIcon("main_scripts/camera.png"))
        self.camera_button.layout().setAlignment(Qt.AlignRight | Qt.AlignTop)
        self.info_button.layout().setAlignment(Qt.AlignRight | Qt.AlignTop)

        self.image_tab_layout = QGridLayout()
        self.image_tab_layout.addWidget(self.camera_button, 0, 1, alignment=Qt.AlignLeft)
        self.image_tab_layout.addWidget(self.info_button,1, 1, alignment=Qt.AlignLeft)
        self.image_tab_layout.addWidget(self.image_label_cam, 0,0)
        self.image_tab_layout.addWidget(self.image_label_rs,1,0)
        self.image_tab.setLayout(self.image_tab_layout)

        self.rviz_tab_layout = QGridLayout()
        self.rviz_tab_layout.addWidget(rviz)
        self.rviz_tab.setLayout(self.rviz_tab_layout)

        tabwidget = QTabWidget()
        tabwidget.addTab(self.image_tab, "CameraWindow")
        tabwidget.addTab(self.rviz_tab, "RvizWindow")

        layout.addWidget(tabwidget)

        self.image_label_cam.setFixedSize(1080, 720)
        self.image_label_cam.setStyleSheet("background-color: #222b33;")

        self.image_label_rs.setFixedSize(1080, 720)
        self.image_label_rs.setStyleSheet("background-color: #222b33;")

        self.camera_button.clicked.connect(self.button_clicked)

    def button_clicked(self):
            print("Button was clicked!")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    start_rviz = StartRviz()
    ex = App()
    ex.show()
    app.exec()