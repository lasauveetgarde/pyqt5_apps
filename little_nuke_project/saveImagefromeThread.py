import cv2
import sys
from PyQt5.QtWidgets import  QWidget, QLabel, QCheckBox, QDesktopWidget, QMessageBox, QLineEdit, QApplication, QPushButton, QVBoxLayout, QFileDialog, QSpinBox, QHBoxLayout, QComboBox, QGridLayout, QRadioButton
from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
import threading
from random import randint
import os
import datetime
from start_rviz import StartRviz

# class LoginWindow(QWidget):
# 	def __init__(self):
# 		super().__init__()
# 		self.setWindowTitle('Login Form')
# 		self.resize(1000, 500)
# 		self.center()

# 		layout = QGridLayout()
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

# 		self.main = AppWindow()
# 		self.setLayout(layout)

# 		self.main.logout_button.clicked.connect(self.logout_button_was_clicked)

# 	def check_password(self):
# 		msg = QMessageBox()
# 		msg.setWindowTitle('Error')
# 		msg.setFixedSize(300, 300)
# 		if self.lineEdit_username.text() == 'user' and self.lineEdit_password.text() == '0000':
# 			self.main.show()
# 			self.hide()
# 			self.lineEdit_password.clear()		
# 		else:
# 			msg.setText('Incorrect Password')
# 			msg.exec_()
		
# 	def center(self):
# 		qr = self.frameGeometry()
# 		cp = QDesktopWidget().availableGeometry().center()
# 		qr.moveCenter(cp)
# 		self.move(qr.topLeft())

# 	def logout_button_was_clicked(self):
# 		self.main.hide()
# 		self.show()	

class Thread(QThread):
	changePixmap = pyqtSignal(QImage)

	def __init__(self,width, height, idx):
		super().__init__()
		self.should_run = False
		self.close_event = threading.Event()
		self.width = width
		self.height = height
		self.cam_idx = idx
	
	def run(self):
		self.cap = cv2.VideoCapture(self.cam_idx)
		fourcc = cv2.VideoWriter_fourcc('X','V','I','D')
		video_timestamp_folder = datetime.datetime.now().strftime("%Y%m%d")
		video_timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
		folder_name = ('Результаты' + '/' + 'Видео' + '/' + video_timestamp_folder)
		os.makedirs(folder_name, exist_ok=True)
		videoWriter = cv2.VideoWriter(folder_name + '/' + video_timestamp + '.avi', fourcc, 30.0, (640,480)) 
		while True:
			if self.should_run:
				ret, self.frame = self.cap.read()
				if ret:
					rgbImage = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
					h, w, ch = rgbImage.shape
					bytesPerLine = ch * w
					convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
					p = convertToQtFormat.scaled(0.5*self.width,0.7*self.height, Qt.KeepAspectRatio)
					self.changePixmap.emit(p)
					videoWriter.write(rgbImage)

				if self.close_event.is_set():
					self.cap.release()
					videoWriter.release()
					self.close_event.clear()
					break

	def startThread(self, should_run):
		self.should_run = should_run
		if self.should_run:
			self.start()
	
	def setSise(self, width, height):
		self.width = width
		self.height = height

	
class AnotherWindow(QWidget):
	def __init__(self):
		super().__init__()
		self.setWindowTitle('Сохранение изображения')
		self.setFixedSize(600,400)
		self.center()

		self.save_image_layout = QHBoxLayout()

		self.image_text_layout = QVBoxLayout()
		self.num_kt_label = QLabel("№ КТ:")
		self.num_opora_label = QLabel("№ Опоры:")
		self.element_label = QLabel("Элемент:")
		self.num_element_label = QLabel("№ элемента:")
		self.save_button = QPushButton("Сохранить")

		self.image_widgets_layout = QVBoxLayout()
		self.num_kt_spinbox = QSpinBox(minimum=1, maximum=100, value=1)
		self.num_kt_spinbox.setFixedSize(350, 50)

		self.num_opora_spinbox = QSpinBox(minimum=1, maximum=100, value=1)
		self.num_opora_spinbox.setFixedSize(350, 50)

		self.element_combox = QComboBox()
		self.element_combox.setFixedSize(350, 50)
		self.element_combox.addItem("Балка")
		self.element_combox.addItem("Болт")
		self.element_combox.addItem("Гайка")
		self.element_combox.addItem("Гребень")

		self.num_element_spinbox = QSpinBox(minimum=1, maximum=100, value=1)
		self.num_element_spinbox.setFixedSize(350, 50)
		self.cancle_button = QPushButton("Отмена")	

		self.image_text_layout.addWidget(self.num_kt_label)
		self.image_text_layout.addWidget(self.num_opora_label)
		self.image_text_layout.addWidget(self.element_label)
		self.image_text_layout.addWidget(self.num_element_label)
		self.image_text_layout.addWidget(self.save_button, alignment=Qt.AlignBottom)

		self.image_widgets_layout.addWidget(self.num_kt_spinbox, alignment=Qt.AlignCenter)
		self.image_widgets_layout.addWidget(self.num_opora_spinbox, alignment=Qt.AlignCenter)
		self.image_widgets_layout.addWidget(self.element_combox, alignment=Qt.AlignCenter)
		self.image_widgets_layout.addWidget(self.num_element_spinbox, alignment=Qt.AlignCenter)
		self.image_widgets_layout.addWidget(self.cancle_button, alignment=Qt.AlignBottom)

		self.save_image_layout.addLayout(self.image_text_layout)
		self.save_image_layout.addLayout(self.image_widgets_layout)

		self.setLayout(self.save_image_layout)
		self.cancle_button.clicked.connect(self.cancle_button_was_clicked)
	
	def cancle_button_was_clicked(self):
		self.hide()

	def center(self):
		qr = self.frameGeometry()
		cp = QDesktopWidget().availableGeometry().center()
		qr.moveCenter(cp)
		self.move(qr.topLeft())


class AppWindow(QWidget):
	def __init__(self):
		super().__init__()
		self.initUI()

	def setImageMain(self, image):
		self.main_image_label.setPixmap(QPixmap.fromImage(image))

	def setImageUP(self, image):
		self.up_image_label.setPixmap(QPixmap.fromImage(image))

	def setImageBack(self, image):
		self.back_image_label.setPixmap(QPixmap.fromImage(image))

	def init_label(self):
		self.label.setPixmap(QPixmap())

	def initUI(self):

		self.button_is_checked = False
		self.main_thread = None

		self.setWindowTitle('Сохранение изображения')
		self.desktop = QApplication.desktop()
		self.screenRect = self.desktop.screenGeometry()
		self.height = self.screenRect.height()
		self.width = self.screenRect.width()
		self.showMaximized() 
		self.center()

		self.main_thread = Thread(self.width, self.height, 0)
		self.main_thread.changePixmap.connect(self.setImageMain)

		self.back_thread = Thread(self.width, self.height, 4)
		self.back_thread.changePixmap.connect(self.setImageBack)

		self.up_thread = Thread(self.width, self.height, 6)
		self.up_thread.changePixmap.connect(self.setImageUP)

		self.main_thread.start()
		self.main_thread.startThread(True)
		self.back_thread.start()
		self.back_thread.startThread(True)
		self.up_thread.start()
		self.up_thread.startThread(True)

		self.rviz = start_rviz.frame
		self.rviz.setFixedWidth(0.4*self.width)
		self.rviz.setFixedHeight(0.5*self.height)

		self.label = QLabel(self)
		self.label.resize(self.width, self.height)

		self.save_snap_button = QPushButton("Сохранение кадра")
		self.save_snap_button.setChecked(self.button_is_checked)
		self.save_snap_button.setFixedWidth(700)
		self.save_snap_button.setFixedHeight(100)

		self.auto_save_snap_button = QPushButton("Не открывать диалог с данными кадра")
		self.auto_save_snap_button.setChecked(self.button_is_checked)
		self.auto_save_snap_button.setFixedWidth(700)
		self.auto_save_snap_button.setFixedHeight(100)

		self.logout_button = QPushButton("Выход")
		self.logout_button.setChecked(self.button_is_checked)
		self.logout_button.setFixedWidth(700)
		self.logout_button.setFixedHeight(100)

		"""
		Индикаторы состояния робота
		"""
		self.indicator_state_ledBar = QHBoxLayout()
		self.state_indicator = QLabel("<font size='11' color='white' face='Verdana'>Готово</font>")
		self.state_indicator.setAlignment(Qt.AlignCenter)
		self.state_indicator.setFixedSize(0.1*self.width, 200)
		self.state_indicator.setStyleSheet("QLabel {color: green; background-color: rgb(17, 48, 17);border: 10px; border-style: outset; border-color: #a8aab1; border-radius: 50%; padding: 20px;}")
		self.indicator_state_ledBar.addWidget(self.state_indicator, alignment=Qt.AlignCenter)

		self.gorizont_indicator = QLabel("")
		self.gorizont_indicator.setFixedSize(0.1*self.width, 200)
		self.gorizont_indicator.setStyleSheet("QLabel {color: green; background-color: rgb(17, 48, 17);border: 10px; border-style: outset; border-color: #a8aab1; border-radius: 50%; padding: 20px;}")
		self.indicator_state_ledBar.addWidget(self.gorizont_indicator, alignment=Qt.AlignCenter)

		self.movement_indicator = QLabel("")
		self.movement_indicator.setFixedSize(0.1*self.width, 200)
		self.movement_indicator.setStyleSheet("QLabel {color: green; background-color: rgb(50, 205, 55);border: 10px; border-style: outset; border-color: #a8aab1; border-radius: 50%; padding: 20px;}")
		self.indicator_state_ledBar.addWidget(self.movement_indicator, alignment=Qt.AlignCenter)

		self.nomination_indicator = QLabel("")
		self.nomination_indicator.setFixedSize(0.1*self.width, 200)
		self.nomination_indicator.setStyleSheet("QLabel {color: green; background-color: rgb(50, 205, 55);border: 10px; border-style: outset; border-color: #a8aab1; border-radius: 50%; padding: 20px;}")
		self.indicator_state_ledBar.addWidget(self.nomination_indicator, alignment=Qt.AlignCenter)

		self.state_line = QHBoxLayout()
		self.state_indicator_line = QLineEdit()
		self.state_indicator_line.setFixedSize(0.4*self.width, 100)
		self.state_indicator_line.setReadOnly(True)
		self.state_line.addWidget(self.state_indicator_line, alignment=Qt.AlignCenter)

		self.indicator_ledBar = QHBoxLayout()
		self.moving_indicator = QLabel("")
		self.moving_indicator.setFixedSize(0.133*self.width, 200)
		self.moving_indicator.setStyleSheet("QLabel {color: green; background-color: rgb(17, 48, 17);border: 10px; border-style: outset; border-color: #a8aab1; border-radius: 50%; padding: 20px;}")
		self.indicator_ledBar.addWidget(self.moving_indicator, alignment=Qt.AlignCenter)

		self.outrigger_indicator = QLabel("")
		self.outrigger_indicator.setFixedSize(0.133*self.width, 200)
		self.outrigger_indicator.setStyleSheet("QLabel {color: green; background-color: rgb(17, 48, 17);border: 10px; border-style: outset; border-color: #a8aab1; border-radius: 50%; padding: 20px;}")
		self.indicator_ledBar.addWidget(self.outrigger_indicator, alignment=Qt.AlignCenter)

		self.girder_indicator = QLabel("")
		self.girder_indicator.setFixedSize(0.133*self.width, 200)
		self.girder_indicator.setStyleSheet("QLabel {color: green; background-color: rgb(50, 205, 55);border: 10px; border-style: outset; border-color: #a8aab1; border-radius: 50%; padding: 20px;}")
		self.indicator_ledBar.addWidget(self.girder_indicator, alignment=Qt.AlignCenter)

		layout = QGridLayout(self)
		self.image_layout = QVBoxLayout(self)
		self.botton_map_layout = QVBoxLayout(self)

		self.main_image_label = QLabel()
		self.main_image_label.setFixedSize(0.5*self.width,0.5*self.height)
		self.up_image_label = QLabel()
		self.up_image_label.setFixedSize(0.25*self.width,0.4*self.height)
		self.back_image_label = QLabel()
		self.back_image_label.setFixedSize(0.25*self.width,0.4*self.height)

		self.else_image_labels = QHBoxLayout(self)
		self.image_layout.addWidget(self.main_image_label, alignment=Qt.AlignTop)
		self.else_image_labels.addWidget(self.up_image_label)
		self.else_image_labels.addWidget(self.back_image_label)

		self.image_layout.addLayout(self.else_image_labels)
		layout.addLayout(self.image_layout, 0, 0)

		self.botton_map_layout.addWidget(self.rviz, alignment=Qt.AlignTop | Qt.AlignCenter)
		self.botton_layout = QHBoxLayout(self)
		self.save_botton_layout = QVBoxLayout(self)
		self.save_botton_layout.addWidget(self.auto_save_snap_button)
		self.save_botton_layout.addWidget(self.save_snap_button)
		self.botton_layout.addLayout(self.save_botton_layout)
		self.botton_layout.addWidget(self.logout_button)
		self.botton_map_layout.addLayout(self.indicator_state_ledBar)
		self.botton_map_layout.addLayout(self.state_line)
		self.botton_map_layout.addLayout(self.indicator_ledBar)
		self.botton_map_layout.addLayout(self.botton_layout)

		layout.addLayout(self.botton_map_layout, 0, 1, 1 ,1 )

		self.save_snap_button.clicked.connect(self.the_button_was_clicked)
		self.auto_save_snap_button.clicked.connect(self.save_button_was_clicked)

		self.w = AnotherWindow()
		self.w.save_button.clicked.connect(self.save_button_was_clicked)

		self.value_num_kt_spinbox = self.w.num_kt_spinbox.value()
		self.w.num_kt_spinbox.valueChanged.connect(self.print_save_image_value)

		self.value_num_opora_spinbox = self.w.num_opora_spinbox.value()
		self.w.num_opora_spinbox.valueChanged.connect(self.print_save_image_value)

		self.value_element_combox = self.w.element_combox.currentText()

		self.value_num_element_spinbox = self.w.num_element_spinbox.value()
		self.w.num_element_spinbox.valueChanged.connect(self.print_save_image_value)

	def the_button_was_clicked(self):
		if self.w.isVisible():
			self.w.hide()

		else:
			self.w.show()

	def print_save_image_value(self):
		self.value_num_kt_spinbox = self.w.num_kt_spinbox.value()
		self.value_num_opora_spinbox = self.w.num_opora_spinbox.value()
		self.value_element_combox = self.w.element_combox.currentText()
		self.value_num_element_spinbox = self.w.num_element_spinbox.value()

	def save_button_was_clicked(self, image):
		self.frame = self.main_thread.frame
		self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
		image = QImage(self.frame, self.frame.shape[1], self.frame.shape[0], QImage.Format_RGB888)
		folder_name = "Результаты" + "/" + "Кадры" + "/" + "КТ №" + str(self.value_num_kt_spinbox) + "/" + "Опора №" + str(self.value_num_opora_spinbox) + "/" + self.value_element_combox + "/" + self.value_element_combox + " №" + str(self.value_num_element_spinbox)
		os.makedirs(folder_name, exist_ok=True)
		timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
		filename = folder_name + "/" + "П_" + timestamp + "_КТ №" + str(self.value_num_kt_spinbox) + ".jpg"
		image.save(filename, "jpg")

	def center(self):
		qr = self.frameGeometry()
		cp = QDesktopWidget().availableGeometry().center()
		qr.moveCenter(cp)
		self.move(qr.topLeft())

if __name__ == '__main__':
	app = QApplication(sys.argv)
	start_rviz = StartRviz()
	ex = AppWindow()
	ex.show()
	app.exec()