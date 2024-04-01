import sys
import rospy
from geometry_msgs.msg import Twist
from PyQt5.QtWidgets import  QWidget, QLabel, QHBoxLayout, QPushButton, QApplication, QVBoxLayout, QTabWidget, QGridLayout, QCheckBox, QLineEdit, QMessageBox, QDesktopWidget
from PyQt5.QtCore import  Qt,  pyqtSlot
from PyQt5.QtGui import  QPixmap, QIcon, QFont
import threading
from camera_thread import ThreadCam
from start_rviz import StartRviz
import qdarktheme

# class LoginWindow(QWidget):
# 	def __init__(self):
# 		super().__init__()
# 		self.setWindowTitle('Login Window')
# 		self.resize(600, 300)
# 		self.center()
# 		layout = QGridLayout()

# 		label_name = QLabel('<font size="4"> Username </font>')
# 		self.lineEdit_username = QLineEdit()
# 		self.lineEdit_username.setPlaceholderText('Please enter your username')
# 		layout.addWidget(label_name, 0, 0)
# 		layout.addWidget(self.lineEdit_username, 0, 1)

# 		label_password = QLabel('<font size="4"> Password </font>')
# 		self.lineEdit_password = QLineEdit()
# 		self.lineEdit_password.setPlaceholderText('Please enter your password')
# 		self.lineEdit_password.setEchoMode(QLineEdit.Password)
# 		layout.addWidget(label_password, 1, 0)
# 		layout.addWidget(self.lineEdit_password, 1, 1)

# 		button_login = QPushButton('Login')
# 		button_login.clicked.connect(self.check_password)
# 		layout.addWidget(button_login, 2, 0, 1, 2)
# 		layout.setRowMinimumHeight(20, 150)
			
# 		self.w = App()
# 		self.w.resize(1500,1000)
# 		self.setLayout(layout)

# 	def check_password(self):
# 		msg = QMessageBox()
# 		if self.lineEdit_username.text() == 'user' and self.lineEdit_password.text() == '0000':
# 			self.w.show()
# 			self.close()
# 		else:
# 			msg.setText('Incorrect Password')
# 			msg.exec_()
				  
# 	def center(self):
# 		qr = self.frameGeometry()
# 		cp = QDesktopWidget().availableGeometry().center()
# 		qr.moveCenter(cp)
# 		self.move(qr.topLeft())

			   
class App(QWidget):
	def __init__(self):
		super().__init__()
		self.initUI()
		rospy.init_node('subscriber', anonymous = True)
		rospy.Subscriber("/cmd_vel", Twist, self.cmd_vel_callback)
		rospy.Subscriber("/cmd_vel", Twist, self.cmd_angle_callback)

	def setImageRow1(self, image):
		self.image_label_cam.setPixmap(QPixmap.fromImage(image))

	def setImageRow2(self, image):
		self.image_label_rs.setPixmap(QPixmap.fromImage(image))

	def initUI(self):
					
			self.button_is_checked = False
			self.thread_stop_event = threading.Event() # Create a threading.Event() object
			self.thread_stop_event.clear()

			self.setWindowTitle('User interface')
			self.center()

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

			layout = QVBoxLayout()
			self.setLayout(layout)

			rviz = start_rviz.frame
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
								"}")
			self.checkbox.setText("Камера переднего наблюдения")
			self.checkbox.stateChanged.connect(self.onStateChanged)
			
			self.velocity_line = QLineEdit('Linear Speed')
			self.velocity_line.setAlignment(Qt.AlignCenter)
			self.velocity_line.setFont(QFont('Arial', 15))
			self.velocity_line.setReadOnly(True)
			
			self.angle_line = QLineEdit('Angle Speed')
			self.angle_line.setAlignment(Qt.AlignCenter)
			self.angle_line.setFont(QFont('Arial', 15))
			self.angle_line.setReadOnly(True)

			self.image_tab_layout = QGridLayout()
			self.image_tab_layout.addWidget(self.camera_button, 0, 0, alignment=Qt.AlignLeft)
			self.image_tab_layout.addWidget(self.image_label_cam, 1, 0, alignment=Qt.AlignLeft)
			self.image_tab_layout.addWidget(self.image_label_rs, 2, 0, alignment=Qt.AlignLeft)
			self.image_tab_layout.addWidget(self.checkbox, 0, 1, alignment=Qt.AlignLeft)
			self.image_tab_layout.addWidget(self.velocity_line, 1,1, alignment=Qt.AlignLeft)
			self.image_tab_layout.addWidget(self.angle_line, 2,1, alignment=Qt.AlignLeft)

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
	
	def center(self):
		qr = self.frameGeometry()
		cp = QDesktopWidget().availableGeometry().center()
		qr.moveCenter(cp)
		self.move(qr.topLeft())

	def cmd_vel_callback(self, msg):
		self.linear_speed = str(round(msg.linear.x,4))
		self.value_vel_changed()
	
	def value_vel_changed(self):    
		self.velocity_line.setText(self.linear_speed)

	def cmd_angle_callback(self, msg):
		self.angle_speed = str(round(msg.angular.z,4))
		self.value_angle_changed()
	
	def value_angle_changed(self):    
		self.angle_line.setText(self.angle_speed)

if __name__ == '__main__':
	try:
		app = QApplication(sys.argv)
		qdarktheme.setup_theme("light", custom_colors={"primary": "#85a39f"})
		start_rviz = StartRviz()
		ex = App()
		ex.show()
		app.exec()
	except rospy.ROSInterruptException:
		pass