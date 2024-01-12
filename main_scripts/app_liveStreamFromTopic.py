import cv2
import sys
import rospy
import numpy as np
from PyQt6.QtWidgets import  QWidget, QLabel, QApplication, QVBoxLayout, QTabWidget
from PyQt6.QtCore import QThread, Qt, pyqtSignal, pyqtSlot
from PyQt6.QtGui import QImage, QPixmap
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
            convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format.Format_RGB888)
            p = convertToQtFormat.scaled(640, 480, Qt.AspectRatioMode.KeepAspectRatio)
            self.changePixmap.emit(p)

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
        layout = QVBoxLayout()
        self.setWindowTitle('Katya App')
        self.resize(1600, 1000)

        self.label = QLabel(self)

        th = Thread(self)
        th.changePixmap.connect(self.setImage)
        th.start()
   
        self.setLayout(layout)
        label = QLabel("Smth else")
        tabwidget = QTabWidget()
        tab1 = QWidget()

        self.image_label = QLabel()
        self.image_label.move(0,0)
        tab1_layout = QVBoxLayout()
        tab1_layout.addWidget(self.image_label)
        
        tab1.setLayout(tab1_layout)

        tabwidget.addTab(tab1, "Camera window")
        tabwidget.addTab(label, "New tab")

        layout.addWidget(tabwidget)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    image_topic = ImageTopic()
    ex = App()
    ex.show()
    app.exec()
