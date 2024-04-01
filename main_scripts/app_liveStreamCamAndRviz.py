import cv2
import roslib; roslib.load_manifest('rviz_python_tutorial')
import sys
from rviz import bindings as rviz
import rospy
import numpy as np
from PyQt5.QtWidgets import  QWidget, QLabel,QHBoxLayout, QPushButton, QApplication, QVBoxLayout, QTabWidget, QGridLayout, QCheckBox, QLineEdit, QMessageBox
from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap, QIcon
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
                p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
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

class LoginWindow(QWidget):
	def __init__(self):
		super().__init__()
		self.setWindowTitle('Login Form')
		self.resize(3000, 2000)

		layout = QGridLayout()

		label_name = QLabel('<font size="4"> Username </font>')
		self.lineEdit_username = QLineEdit()
		self.lineEdit_username.setPlaceholderText('Please enter your username')
		layout.addWidget(label_name, 0, 0)
		layout.addWidget(self.lineEdit_username, 0, 1)

		label_password = QLabel('<font size="4"> Password </font>')
		self.lineEdit_password = QLineEdit()
		self.lineEdit_password.setPlaceholderText('Please enter your password')
		self.lineEdit_password.setEchoMode(QLineEdit.Password)
		layout.addWidget(label_password, 1, 0)
		layout.addWidget(self.lineEdit_password, 1, 1)

		button_login = QPushButton('Login')
		button_login.clicked.connect(self.check_password)
		layout.addWidget(button_login, 2, 0, 1, 2)
		layout.setRowMinimumHeight(20, 150)
		self.w = App()
		self.w.resize(3000, 2000)
		self.setLayout(layout)

	def check_password(self):
		msg = QMessageBox()
		if self.lineEdit_username.text() == 'user' and self.lineEdit_password.text() == '0000':
			self.w.show()
			self.close()
		else:
			msg.setText('Incorrect Password')
			msg.exec_()
               
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

            self.setWindowTitle('User interface')

            self.th_cam1 = ThreadCam(0, self)
            self.th_cam1.changePixmap.connect(self.setImageRow1)
            self.th_cam2 = ThreadCam(6, self)
            self.th_cam2.changePixmap.connect(self.setImageRow1)
            self.th_cam3 = ThreadCam(8, self)
            self.th_cam3.changePixmap.connect(self.setImageRow2)

            self.th_cam1.wait()
            self.th_cam2.wait()
            self.th_cam3.start()

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
            self.camera_button.layout().setAlignment(Qt.AlignLeft | Qt.AlignTop)
            self.camera_button.setChecked(self.button_is_checked)
            self.camera_button.clicked.connect(self.button_clicked)

            self.checkbox = QCheckBox(self)
            self.checkbox.setGeometry(0, 0, 100, 180)
            self.checkbox.setStyleSheet("QCheckBox::indicator"
                                "{"
                                "width :40px;"
                                "height : 40px;"
                                "background-color: rgb(255, 0, 0);"
                                "}")
            self.checkbox.stateChanged.connect(self.onStateChanged)

            self.image_tab_layout = QGridLayout()
            self.image_tab_layout.addWidget(self.camera_button, 0, 0, alignment=Qt.AlignLeft)
            self.image_tab_layout.addWidget(self.image_label_cam, 1, 0, alignment=Qt.AlignLeft)
            self.image_tab_layout.addWidget(self.image_label_rs, 2, 0, alignment=Qt.AlignLeft)
            self.image_tab_layout.addWidget(self.checkbox, 0, 1, alignment=Qt.AlignLeft)
            self.image_tab.setLayout(self.image_tab_layout)

            self.rviz_tab_layout = QGridLayout()
            self.rviz_tab_layout.addWidget(rviz)
            self.rviz_tab.setLayout(self.rviz_tab_layout)

            tabwidget = QTabWidget()
            tabwidget.addTab(self.image_tab, "CameraWindow")
            tabwidget.addTab(self.rviz_tab, "RvizWindow")

            layout.addWidget(tabwidget)

            self.image_label_cam.setFixedSize(640,480)
            self.image_label_cam.setStyleSheet("background-color: #222b33;")

            self.image_label_rs.setFixedSize(640,480)
            self.image_label_rs.setStyleSheet("background-color: #222b33;")

    def button_clicked(self):
        if self.camera_button.isChecked():
            print("Button was clicked!")
        else:
            print("nothing")
    
    def onStateChanged(self):
        if self.checkbox.isChecked():
            self.thread_stop_event.clear()  # Clear the threading.Event() object
            self.th_cam1.startThread(True)  # Start the thread
            self.th_cam2.startThread(False)  # Stop the thread
            self.checkbox.setText("Камера переднего наблюдения")
        else:
            self.checkbox.setText("Камера заднего наблюдения")
            self.thread_stop_event.set()  # Signal the thread to stop when the button is checked
            self.th_cam1.startThread(False)  # Stop the thread
            self.th_cam2.startThread(True)  # Stop the thread

if __name__ == '__main__':
    app = QApplication(sys.argv)
    start_rviz = StartRviz()
    ex = LoginWindow()
    ex.show()
    app.exec()