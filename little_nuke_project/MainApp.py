import sys
import rospy
import os
os.environ['QT_API'] = 'PyQt5'
from qtpy import  QtWidgets
from geometry_msgs.msg import Twist
from PyQt5.QtWidgets import  QWidget, QLabel, QPushButton, qApp, QApplication, QTextEdit, QVBoxLayout, QTabWidget, QGridLayout, QCheckBox, QLineEdit, QDesktopWidget, QMessageBox, QRadioButton
from PyQt5.QtCore import  Qt,  pyqtSlot,  QTimer, QTime, QDate, QDateTime
from PyQt5.QtGui import  QPixmap, QIcon, QFont, QCursor
import threading
from camera_thread import ThreadCam
from start_rviz import StartRviz
import qdarktheme
import qtawesome as qta

# class LoginWindow(QWidget):
# 	def __init__(self):
# 		super().__init__()
# 		self.setWindowTitle('Login Form')
# 		self.resize(1000, 500)
# 		self.center()

# 		layout = QGridLayout()

# 		# choose_user = QLabel('Выбор пользователя')
# 		# layout.addWidget(choose_user, 0, 0, 1, 1)

# 		operator_radiobutton = QRadioButton("Operator")
# 		admin_radiobutton = QRadioButton("Administrartor")
# 		layout.addWidget(operator_radiobutton, 1, 0)
# 		layout.addWidget(admin_radiobutton, 1, 1)

# 		label_name = QLabel('<font size="4"> Username </font>')
# 		self.lineEdit_username = QLineEdit()
# 		self.lineEdit_username.setPlaceholderText('Please enter your username')
# 		layout.addWidget(label_name, 2, 0)
# 		layout.addWidget(self.lineEdit_username, 2, 1)

# 		label_password = QLabel('<font size="4"> Password </font>')
# 		self.lineEdit_password = QLineEdit()
# 		self.lineEdit_password.setPlaceholderText('Please enter your password')
# 		self.lineEdit_password.setEchoMode(QLineEdit.Password)
# 		layout.addWidget(label_password, 3, 0)
# 		layout.addWidget(self.lineEdit_password, 3, 1)

# 		button_login = QPushButton('Login')
# 		button_login.clicked.connect(self.check_password)
# 		layout.addWidget(button_login, 5, 0, 1, 5)
# 		layout.setRowMinimumHeight(2, 75)

# 		login_checkbox = QCheckBox(self)
# 		login_checkbox.setGeometry(0, 0, 100, 180)
# 		login_checkbox.setStyleSheet("QCheckBox::indicator"
# 							"{"
# 							"width :40px;"
# 							"height : 40px;"
# 							"}")
# 		login_checkbox.setText("Запомнить имя пользователя")
# 		layout.addWidget(login_checkbox, 4, 0, 1, 4)

# 		self.w = AppWindow()
# 		self.setLayout(layout)

# 	def check_password(self):
# 		msg = QMessageBox()
# 		msg.setWindowTitle('Error')
# 		msg.setFixedSize(300, 300)
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


class AppWindow(QtWidgets.QWidget):
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
		self.setWindowIcon(QIcon('little_nuke_project/trans.jpg'))

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
		self.image_label_cam.setFixedSize(900,720)
		# self.image_label_cam.setStyleSheet("background-color: #222b33;")
		self.image_label_rs = QLabel()
		self.image_label_rs.setFixedSize(480,480)
		# self.image_label_rs.setStyleSheet("background-color: #222b33;")

		layout = QVBoxLayout()
		self.setLayout(layout)

		self.rviz = start_rviz.frame
		self.rviz.setMinimumSize(420, 470)
		self.rviz.resize(self.rviz.sizeHint())

		self.logging_tab = QWidget()
		self.image_tab = QWidget()
		self.service_tab = QWidget()

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

		self.some_button = QPushButton('Test Button')
		self.some_button.clicked.connect(self.clicked_some_button)

		self.logging_area = QTextEdit()
		self.logging_area.setFixedSize(640,1100)
		self.logging_area.setReadOnly(True)
		self.logging_area.insertPlainText("Информация (логирование) состояний робота\n")

		self.info_area = QTextEdit()
		self.info_area.setFixedSize(640,1200)
		self.info_area.setReadOnly(True)
		self.info_area.insertPlainText("Инструкция по работе с мобильной платформой\n")

		"""
		Создание вывода времени и даты
		"""

		self.time_indicator_label = QVBoxLayout()
		self.time_label = QLabel()
		self.time_label.setAlignment(Qt.AlignCenter|Qt.AlignRight)
		self.date_label = QLabel()
		self.date_label.setAlignment(Qt.AlignCenter|Qt.AlignRight)
		self.timer = QTimer(self)
		self.timer.timeout.connect(self.showTime)
		self.timer.timeout.connect(self.showDate)
		self.timer.start(1000)
		self.time_indicator_label.addWidget(self.time_label, alignment=Qt.AlignRight)
		self.time_indicator_label.addWidget(self.date_label, alignment=Qt.AlignRight)

		"""
		Индикаторы состояния робота
		"""

		self.indicator_ledBar = QVBoxLayout()
		self.moving_indicator = QLabel("")
		self.moving_indicator_label = QLabel("Разрешение на движение")
		self.moving_indicator.setFixedSize(100, 100)
		self.moving_indicator.setStyleSheet("QLabel {color: green; background-color: rgb(17, 48, 17);border: 5px; border-style: outset; border-color: #a8aab1; border-radius: 50%; padding: 10px;}")
		self.indicator_ledBar.addWidget(self.moving_indicator_label, alignment=Qt.AlignCenter | Qt.AlignBottom)
		self.indicator_ledBar.addWidget(self.moving_indicator, alignment=Qt.AlignCenter)

		self.outrigger_indicator = QLabel("")
		self.outrigger_indicator_label = QLabel("Аутригеры")
		self.outrigger_indicator.setFixedSize(100, 100)
		self.outrigger_indicator.setStyleSheet("QLabel {color: green; background-color: rgb(50, 205, 50);border: 5px; border-style: outset; border-color: #a8aab1; border-radius: 50%; padding: 10px;}")
		self.indicator_ledBar.addWidget(self.outrigger_indicator_label, alignment=Qt.AlignCenter | Qt.AlignBottom)
		self.indicator_ledBar.addWidget(self.outrigger_indicator, alignment=Qt.AlignCenter)

		self.girder_indicator = QLabel("")
		self.girder_indicator_label = QLabel("Мачта поднята")
		self.girder_indicator.setFixedSize(100, 100)
		self.girder_indicator.setStyleSheet("QLabel {color: green; background-color: rgb(50, 205, 50);border: 5px; border-style: outset; border-color: #a8aab1; border-radius: 50%; padding: 10px;}")
		self.indicator_ledBar.addWidget(self.girder_indicator_label, alignment=Qt.AlignCenter | Qt.AlignBottom)
		self.indicator_ledBar.addWidget(self.girder_indicator, alignment=Qt.AlignCenter)

		self.power_indicator = QLabel("")
		self.power_indicator_label = QLabel("Заряд аккумялятора, 0%")
		self.power_indicator.setFixedSize(100, 100)
		self.power_indicator.setStyleSheet("QLabel {color: green; background-color: rgb(17, 48, 17);border: 5px; border-style: outset; border-color: #a8aab1; border-radius: 50%; padding: 10px;}")
		self.indicator_ledBar.addWidget(self.power_indicator_label, alignment=Qt.AlignCenter | Qt.AlignBottom)
		self.indicator_ledBar.addWidget(self.power_indicator, alignment=Qt.AlignCenter)

		self.logout_button = QPushButton('Log Out')
		self.logout_button.setFixedSize(160, 80)
		self.indicator_ledBar.addWidget(self.logout_button, alignment=Qt.AlignCenter)

		"""
		Добавление слоев в основное окно 
		"""

		self.image_tab_layout = QGridLayout()
		self.image_tab_layout.addLayout(self.time_indicator_label, 0, 1)
		self.image_tab_layout.addLayout(self.indicator_ledBar, 1, 1, 2, 1)
		self.image_tab_layout.addWidget(self.image_label_cam, 1, 0, alignment=Qt.AlignLeft)
		self.image_tab_layout.addWidget(self.image_label_rs, 2, 0, alignment=Qt.AlignLeft)
		self.image_tab_layout.addWidget(self.checkbox, 0, 0, alignment=Qt.AlignLeft)
		self.image_tab_layout.addWidget(self.rviz, 2, 0, alignment=Qt.AlignRight)
		self.image_tab.setLayout(self.image_tab_layout)

		"""
		Создание вкладки для логирования и получения информации по работе с роботом
		"""

		self.logging_tab_layout = QGridLayout()
		self.logging_tab.setLayout(self.logging_tab_layout)
		self.logging_tab_layout.addWidget(self.some_button,0,0)
		self.logging_tab_layout.addWidget(self.logging_area,1,0)
		self.logging_tab_layout.addWidget(self.info_area, 1, 1)

		"""
		Создание сервисной вкладки
		"""

		self.service_tab_layout = QGridLayout()
		self.service_tab.setLayout(self.service_tab_layout)
		self.service_tab_layout.addLayout(self.info_tab_layout, 0,0)

		"""
		Создание TAB для пользовательского интерфейса
		"""

		tabwidget = QTabWidget()
		tabwidget.addTab(self.image_tab, "Info")
		tabwidget.addTab(self.logging_tab, "Logging")
		tabwidget.addTab(self.service_tab, "Service")

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
			current_time = QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss")
			log_message = f"<font color='red'>{current_time}</font> Turned to front camera<br>"
			self.logging_area.insertHtml(log_message)
			self.auto_scrolling()

		else:
			self.checkbox.setText("Камера заднего наблюдения")
			self.thread_stop_event.set()  # Signal the thread to stop when the button is checked
			self.th_cam1.startThread(False)  # Stop the thread
			self.th_cam2.startThread(True)  # Stop the thread
			current_time = QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss")
			log_message = f"<font color='red'>{current_time}</font> Turned to back camera<br>"
			self.logging_area.insertHtml(log_message)
			self.auto_scrolling()

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

	def clicked_some_button(self):
		current_time = QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss")
		log_message = f"<font color='red'>{current_time}</font> Test button was clicked<br>"
		self.logging_area.insertHtml(log_message)
		self.auto_scrolling()
		
	def auto_scrolling (self):
		self.scrollbar = self.logging_area.verticalScrollBar()
		self.scrollbar.setValue(self.scrollbar.maximum())

if __name__ == '__main__':
	try:
		app = QApplication(sys.argv)
		qdarktheme.setup_theme(custom_colors={"primary": "#bf4584"})
		start_rviz = StartRviz()
		ex = AppWindow()
		ex.show()
		app.exec()
	except rospy.ROSInterruptException:
		pass