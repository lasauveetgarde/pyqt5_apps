import sys
import rospy
import os
os.environ['QT_API'] = 'PyQt5'
from qtpy import QtGui, QtWidgets, QtCore
from geometry_msgs.msg import Twist
from PyQt5.QtWidgets import  QWidget, QLabel, qApp, QToolBar, QMainWindow, QHBoxLayout, QAction, QFileDialog, QPushButton, QApplication, QPlainTextEdit, QVBoxLayout, QTabWidget, QGridLayout, QCheckBox, QLineEdit, QMessageBox, QDesktopWidget, QStyle
from PyQt5.QtCore import  Qt,  pyqtSlot,  QTimer, QTime, QDate
from PyQt5.QtGui import  QPixmap, QIcon, QFont
import threading
from camera_thread import ThreadCam
from start_rviz import StartRviz
import qdarktheme
import qtawesome as qta

class App(QtWidgets.QWidget):
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
		
		self.info_tab_layout = QGridLayout()
		self.info_tab_layout.setVerticalSpacing(1) 

		# self.linear_speed_label = QLabel('Линейная скорость')
		self.velocity_line = QLineEdit('Linear Speed')
		self.velocity_line.setAlignment(Qt.AlignCenter)
		self.velocity_line.setFont(QFont('Arial', 15))
		self.velocity_line.setFixedSize(400, 100)
		self.velocity_line.setReadOnly(True)
		
		self.angle_line = QLineEdit('Angle Speed')
		self.angle_line.setAlignment(Qt.AlignCenter)
		self.angle_line.setFont(QFont('Arial', 15))
		self.angle_line.setFixedSize(400, 100)
		self.angle_line.setReadOnly(True)

		self.smth1 = QLineEdit('Linear Speed')
		self.smth1.setAlignment(Qt.AlignCenter)
		self.smth1.setFont(QFont('Arial', 15))
		self.smth1.setFixedSize(400, 100)
		self.smth1.setReadOnly(True)
		
		self.smth2 = QLineEdit('Angle Speed')
		self.smth2.setAlignment(Qt.AlignCenter)
		self.smth2.setFont(QFont('Arial', 15))
		self.smth2.setFixedSize(400, 100)
		self.smth2.setReadOnly(True)

		self.smth3 = QLineEdit('Linear Speed')
		self.smth3.setAlignment(Qt.AlignCenter)
		self.smth3.setFont(QFont('Arial', 15))
		self.smth3.setFixedSize(400, 100)
		self.smth3.setReadOnly(True)
		
		self.smth4 = QLineEdit('Angle Speed')
		self.smth4.setAlignment(Qt.AlignCenter)
		self.smth4.setFont(QFont('Arial', 15))
		self.smth4.setFixedSize(400, 100)
		self.smth4.setReadOnly(True)

		self.info_tab_layout.addWidget(self.velocity_line, 0,0, alignment=Qt.AlignLeft)
		self.info_tab_layout.addWidget(self.angle_line, 0,1, alignment=Qt.AlignLeft)
		self.info_tab_layout.addWidget(self.smth1, 1,0, alignment=Qt.AlignLeft)
		self.info_tab_layout.addWidget(self.smth2, 1,1, alignment=Qt.AlignLeft)
		self.info_tab_layout.addWidget(self.smth3, 2,0, alignment=Qt.AlignLeft)
		self.info_tab_layout.addWidget(self.smth4, 2,1, alignment=Qt.AlignLeft)
		
		self.logging_area = QPlainTextEdit()
		self.logging_area.insertPlainText("Информация (логирование) состояний робота\n")

		self.time_label = QLabel()
		self.time_label.setAlignment(Qt.AlignCenter)
		self.date_label = QLabel()
		self.date_label.setAlignment(Qt.AlignCenter)
		self.timer = QTimer(self)
		self.timer.timeout.connect(self.showTime)
		self.timer.timeout.connect(self.showDate)
		self.timer.start(1000)

		self.led_label = QLabel()
		self.led_label.setStyleSheet('''Qlabel{background-color: rgb(0,234,0); border-radius: 25px; border: 3px groove gray; border-style: outser; }''')

		self.image_tab_layout = QGridLayout()
		self.image_tab_layout.addLayout(self.info_tab_layout, 1, 1)
		self.image_tab_layout.addWidget(self.image_label_cam, 1, 0, alignment=Qt.AlignLeft)
		self.image_tab_layout.addWidget(self.image_label_rs, 2, 0, alignment=Qt.AlignLeft)
		self.image_tab_layout.addWidget(self.checkbox, 0, 1, alignment=Qt.AlignLeft)
		self.image_tab_layout.addWidget(self.logging_area, 2, 1)
		self.image_tab_layout.addWidget(self.time_label, 0, 2, alignment=Qt.AlignTop)
		self.image_tab_layout.addWidget(self.date_label, 0, 2, alignment=Qt.AlignBottom)
		self.image_tab_layout.addWidget(self.led_label, 1, 2)

		self.image_tab.setLayout(self.image_tab_layout)

		self.rviz_tab_layout = QGridLayout()
		self.rviz_tab_layout.addWidget(rviz)
		self.rviz_tab.setLayout(self.rviz_tab_layout)

		tabwidget = QTabWidget()
		tabwidget.addTab(self.image_tab, "InfoWindow")
		tabwidget.addTab(self.rviz_tab, "MapWindow")

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

	def showTime(self):
		current_time = QTime.currentTime()
		label_time = current_time.toString('hh:mm:ss')
		self.time_label.setText(label_time)

	def showDate(self):
		current_date = QDate.currentDate()
		label_date = current_date.toString('dd.MM.yyyy')
		self.date_label.setText(label_date)

if __name__ == '__main__':
	try:
		app = QApplication(sys.argv)
		qdarktheme.setup_theme(custom_colors={"primary": "#85a39f"})
		start_rviz = StartRviz()
		ex = App()
		ex.show()
		app.exec()
	except rospy.ROSInterruptException:
		pass