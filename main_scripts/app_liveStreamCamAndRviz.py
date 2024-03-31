import cv2
import roslib; roslib.load_manifest('rviz_python_tutorial')
import sys
from rviz import bindings as rviz
import rospy
import numpy as np
from PyQt5.QtWidgets import  QWidget, QLabel,QHBoxLayout, QPushButton, QApplication, QVBoxLayout, QTabWidget, QGridLayout, QCheckBox
from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap, QIcon
from sensor_msgs.msg import CompressedImage
from cv_bridge import CvBridge, CvBridgeError
import threading

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

    def startThread(self, should_run):
        self.should_run = should_run
        if self.should_run:
            self.start()
        else:
            self.cap.release()
            self.cap = None

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
                    
            self.button_is_checked = False

            self.thread_stop_event = threading.Event() # Create a threading.Event() object
            self.thread_stop_event.clear()

            self.setWindowTitle('Test App')
            self.resize(2000, 2000)

            self.th_cam1 = ThreadCam(0, self)
            self.th_cam1.changePixmap.connect(self.setImageRow1)

            self.th_cam1.start()

            self.image_label_cam = QLabel()
            self.image_label_rs = QLabel()

            rviz = start_rviz.frame

            layout = QVBoxLayout()
            self.setLayout(layout)

            self.rviz_tab = QWidget()
            self.image_tab = QWidget()

            self.camera_button = QPushButton(checkable=True)

            self.camera_button.setLayout(QHBoxLayout())
            self.camera_button.setIcon(QIcon("main_scripts/camera.png"))
            self.camera_button.layout().setAlignment(Qt.AlignRight | Qt.AlignTop)
            self.camera_button.setChecked(self.button_is_checked)
            self.camera_button.clicked.connect(self.button_clicked)

            self.checkbox = QCheckBox(self)
            self.checkbox.setGeometry(200, 150, 100, 80)
            
            self.checkbox.setStyleSheet("QCheckBox::indicator"
                                "{"
                                "width :40px;"
                                "height : 40px;"
                                "}")
            self.checkbox.stateChanged.connect(self.onStateChanged)

            self.image_tab_layout = QGridLayout()
            self.image_tab_layout.addWidget(self.camera_button, 0, 0, alignment=Qt.AlignLeft)
            self.image_tab_layout.addWidget(self.image_label_cam, 1, 0, alignment=Qt.AlignLeft)
            self.image_tab_layout.addWidget(self.image_label_rs, 2, 0, alignment=Qt.AlignLeft)
            self.image_tab_layout.addWidget(self.checkbox, 0, 1)
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

    def button_clicked(self):
        if self.camera_button.isChecked():
            print("Button was clicked!")
        else:
            print("nothing")
    
    def onStateChanged(self):
        if self.checkbox.isChecked():
            self.checkbox.setText("Камера переднего наблюдения")
            self.thread_stop_event.set()  # Signal the thread to stop when the button is checked
            self.th_cam1.startThread(False)  # Stop the thread
            self.image_label_cam.setPixmap(QPixmap())  # Hide the QLabel object
            self.image_label_rs.setPixmap(QPixmap())  # Hide the QLabel object
        else:
            self.checkbox.setText("Камера заднего наблюдения")
            self.thread_stop_event.clear()  # Clear the threading.Event() object
            self.th_cam1.startThread(True)  # Start the thread

if __name__ == '__main__':
    app = QApplication(sys.argv)
    start_rviz = StartRviz()
    ex = App()
    ex.show()
    app.exec()