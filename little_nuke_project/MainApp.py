import sys
import rospy
import os
os.environ['QT_API'] = 'PyQt5'
from qtpy import  QtWidgets
from geometry_msgs.msg import Twist
from PyQt5.QtWidgets import  QWidget, QLabel, qApp, QApplication, QPlainTextEdit, QVBoxLayout, QTabWidget, QGridLayout, QCheckBox, QLineEdit, QDesktopWidget
from PyQt5.QtCore import  Qt,  pyqtSlot,  QTimer, QTime, QDate
from PyQt5.QtGui import  QPixmap, QIcon, QFont, QCursor
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

		"""
		Объявление видеопотоков с трех камер видеонаблюдения
		"""

		self.th_cam1 = ThreadCam(0, self)
		self.th_cam1.changePixmap.connect(self.setImageRow1)
		self.th_cam2 = ThreadCam(6, self)
		self.th_cam2.changePixmap.connect(self.setImageRow1)
		self.th_cam3 = ThreadCam(8, self)
		self.th_cam3.changePixmap.connect(self.setImageRow2)

		self.th_cam1.wait()
		self.th_cam2.wait()
		self.th_cam3.start()

		"""
		Создание рамок для отображения с двух камер
		"""

		self.image_label_cam = QLabel()
		self.image_label_cam.setFixedSize(640,480)
		self.image_label_cam.setStyleSheet("background-color: #222b33;")
		self.image_label_rs = QLabel()
		self.image_label_rs.setFixedSize(640,480)
		self.image_label_rs.setStyleSheet("background-color: #222b33;")

		layout = QVBoxLayout()
		self.setLayout(layout)

		rviz = start_rviz.frame
		self.rviz_tab = QWidget()
		self.image_tab = QWidget()

		"""
		Переключение камеры
		"""

		self.checkbox = QCheckBox(self)
		self.checkbox.setGeometry(0, 0, 100, 180)
		self.checkbox.setStyleSheet("QCheckBox::indicator"
							"{"
							"width :40px;"
							"height : 40px;"
							"}")
		self.checkbox.setText("Камера переднего наблюдения")
		self.checkbox.stateChanged.connect(self.onStateChanged)
		
		"""
		Блок вывода информации с ROS
		"""

		self.info_tab_layout = QGridLayout()

		def create_info_label(label_text, alignment, font, width, height, readonly):
			label = QLineEdit(label_text)
			label.setAlignment(alignment)
			label.setFont(font)
			label.setFixedWidth(width)
			label.setFixedHeight(height)
			label.setReadOnly(readonly)
			return label

		self.velocity_line = create_info_label('Linear Speed', Qt.AlignCenter, QFont('Arial', 8), 300, 150, True)
		self.angle_line = create_info_label('Angle Speed', Qt.AlignCenter, QFont('Arial', 8), 300, 150, True)
		self.smth1 = create_info_label('1', Qt.AlignCenter, QFont('Arial', 8), 300, 150, True)
		self.smth2 = create_info_label('2', Qt.AlignCenter, QFont('Arial', 8), 300, 150, True)
		self.smth3 = create_info_label('3', Qt.AlignCenter, QFont('Arial', 8), 300, 150, True)
		self.smth4 = create_info_label('4', Qt.AlignCenter, QFont('Arial', 8), 300, 150, True)

		self.info_tab_layout.addWidget(self.velocity_line, 0,0, alignment=Qt.AlignLeft)
		self.info_tab_layout.addWidget(self.angle_line, 0,1, alignment=Qt.AlignLeft)
		self.info_tab_layout.addWidget(self.smth1, 1,0, alignment=Qt.AlignLeft)
		self.info_tab_layout.addWidget(self.smth2, 1,1, alignment=Qt.AlignLeft)
		self.info_tab_layout.addWidget(self.smth3, 2,0, alignment=Qt.AlignLeft)
		self.info_tab_layout.addWidget(self.smth4, 2,1, alignment=Qt.AlignLeft)


		"""
		Окно логирования информации о роботе
		"""

		self.logging_area = QPlainTextEdit()
		self.logging_area.setFixedSize(640,480)
		self.logging_area.insertPlainText("Информация (логирование) состояний робота\n")

		"""
		Создание вывода времени и даты
		"""

		self.time_indicator_label = QVBoxLayout()
		self.time_label = QLabel()
		self.time_label.setAlignment(Qt.AlignCenter)
		self.date_label = QLabel()
		self.date_label.setAlignment(Qt.AlignCenter)
		self.timer = QTimer(self)
		self.timer.timeout.connect(self.showTime)
		self.timer.timeout.connect(self.showDate)
		self.timer.start(1000)
		self.time_indicator_label.addWidget(self.time_label)
		self.time_indicator_label.addWidget(self.date_label)

		"""
		Индикаторы состояния робота
		"""

		self.indicator_ledBar = QVBoxLayout()
		self.moving_indicator = QLabel("")
		self.moving_indicator.setFixedSize(100, 100)
		self.moving_indicator.setStyleSheet("QLabel {color: green; background-color: rgb(50, 205, 50);border: 3px; border-style: outser; border-radius: 50%; padding: 10px;}")
		self.indicator_ledBar.addWidget(self.moving_indicator)

		self.girder_indicator = QLabel("")
		self.girder_indicator.setFixedSize(100, 100)
		self.girder_indicator.setStyleSheet("QLabel {color: green; background-color: rgb(178, 34, 34);border: 3px; border-style: outser; border-radius: 50%; padding: 10px;}")
		self.indicator_ledBar.addWidget(self.girder_indicator)

		self.controller_indicator = QLabel("")
		self.controller_indicator.setFixedSize(100, 100)
		self.controller_indicator.setStyleSheet("QLabel {color: green; background-color: rgb(0, 0, 139);border: 3px; border-style: outser; border-radius: 50%; padding: 10px;}")
		self.indicator_ledBar.addWidget(self.controller_indicator)

		self.power_indicator = QLabel("")
		self.power_indicator.setFixedSize(100, 100)
		self.power_indicator.setStyleSheet("QLabel {color: green; background-color: rgb(255, 215, 0);border: 3px; border-style: outser; border-radius: 50%; padding: 10px;}")
		self.indicator_ledBar.addWidget(self.power_indicator)

		"""
		Добавление слоев в основное окно 
		"""

		self.image_tab_layout = QGridLayout()
		self.image_tab_layout.addLayout(self.info_tab_layout, 1, 1)
		self.image_tab_layout.addLayout(self.time_indicator_label, 0, 2)
		self.image_tab_layout.addLayout(self.indicator_ledBar, 1, 2)
		self.image_tab_layout.addWidget(self.image_label_cam, 1, 0, alignment=Qt.AlignLeft)
		self.image_tab_layout.addWidget(self.image_label_rs, 2, 0, alignment=Qt.AlignLeft)
		self.image_tab_layout.addWidget(self.checkbox, 0, 1, alignment=Qt.AlignLeft)
		self.image_tab_layout.addWidget(self.logging_area, 2, 1)
		self.image_tab.setLayout(self.image_tab_layout)

		"""
		Создание вкладки для RViz и добавление слоя с отображением
		"""

		self.rviz_tab_layout = QGridLayout()
		self.rviz_tab_layout.addWidget(rviz)
		self.rviz_tab.setLayout(self.rviz_tab_layout)

		"""
		Создание TAB для пользовательского интерфейса
		"""

		tabwidget = QTabWidget()
		tabwidget.addTab(self.image_tab, "InfoWindow")
		tabwidget.addTab(self.rviz_tab, "MapWindow")

		layout.addWidget(tabwidget)

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
		window_width = self.width()
		window_height = self.height()
		screen_geometry = QDesktopWidget().availableGeometry(QCursor.pos())
		screen_width = screen_geometry.width()
		screen_height = screen_geometry.height()
		self.move((int(screen_width - window_width) // 2), (int(screen_height - window_height) // 2))

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
		qdarktheme.setup_theme("light", custom_colors={"primary": "#85a39f"})
		start_rviz = StartRviz()
		ex = App()
		ex.show()
		app.exec()
	except rospy.ROSInterruptException:
		pass