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
        while True:
            frame = image_topic.image
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

class ImageTopic():

    def __init__(self) -> None:
        rospy.init_node('video_frame', anonymous=True)
        self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber("/rs_camera/color/image_raw/compressed",CompressedImage ,self.callback)
        self.image = np.zeros((480, 640, 3), dtype='uint8')
        self.dst_folder = rospy.get_param('~dst_folder','test_folder')
        self.rate = rospy.Rate(15)
        
    def callback(self,data):
        try:
            np_arr = np.fromstring(data.data, np.uint8)
            cv_image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        except CvBridgeError as e:
            print(e)
        self.image = cv_image

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def setImage(self, image):
        self.image_label.setPixmap(QPixmap.fromImage(image))

    def initUI(self):
        
        self.setWindowTitle('Katya App')
        self.resize(1600, 1000)
        self.label = QLabel(self)

        th = Thread(self)
        th.changePixmap.connect(self.setImage)
        th.start()

        rviz = start_rviz.frame

        layout = QVBoxLayout()
        self.setLayout(layout)
        rviz_tab = QWidget()
        tabwidget = QTabWidget()
        image_tab = QWidget()

        self.image_label = QLabel()
        self.image_label.move(0,0)
        image_tab_layout = QVBoxLayout()
        self.image_label.setStyleSheet("background-color: #222b33;")
        image_tab_layout.addWidget(self.image_label)
        
        self.rviz_frame = QLabel()
        rviz_tab_layout = QVBoxLayout()
        rviz_tab_layout.addWidget(rviz)

        image_tab.setLayout(image_tab_layout)
        rviz_tab.setLayout(rviz_tab_layout)

        tabwidget.addTab(image_tab, "CameraWindow")
        tabwidget.addTab(rviz_tab, "RvizWindow")

        layout.addWidget(tabwidget)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    start_rviz = StartRviz()
    image_topic = ImageTopic()
    ex = App()
    ex.show()
    app.exec()
