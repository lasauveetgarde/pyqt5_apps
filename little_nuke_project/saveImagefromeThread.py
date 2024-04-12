import cv2
import sys
from PyQt5.QtWidgets import  QWidget, QLabel, QCheckBox, QDesktopWidget, QMessageBox, QLineEdit, QApplication, QPushButton, QVBoxLayout, QFileDialog, QSpinBox, QHBoxLayout, QComboBox, QGridLayout, QRadioButton
from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
import threading
from random import randint
import os
import datetime


class LoginWindow(QWidget):
	def __init__(self):
		super().__init__()
		self.setWindowTitle('Login Form')
		self.resize(1000, 500)
		self.center()

		layout = QGridLayout()

		# choose_user = QLabel('Выбор пользователя')
		# layout.addWidget(choose_user, 0, 0, 1, 1)

		operator_radiobutton = QRadioButton("Operator")
		admin_radiobutton = QRadioButton("Administrartor")
		layout.addWidget(operator_radiobutton, 1, 0)
		layout.addWidget(admin_radiobutton, 1, 1)

		label_name = QLabel('<font size="4"> Username </font>')
		self.lineEdit_username = QLineEdit()
		self.lineEdit_username.setPlaceholderText('Please enter your username')
		layout.addWidget(label_name, 2, 0)
		layout.addWidget(self.lineEdit_username, 2, 1)

		label_password = QLabel('<font size="4"> Password </font>')
		self.lineEdit_password = QLineEdit()
		self.lineEdit_password.setPlaceholderText('Please enter your password')
		self.lineEdit_password.setEchoMode(QLineEdit.Password)
		layout.addWidget(label_password, 3, 0)
		layout.addWidget(self.lineEdit_password, 3, 1)

		button_login = QPushButton('Login')
		button_login.clicked.connect(self.check_password)
		layout.addWidget(button_login, 5, 0, 1, 5)
		layout.setRowMinimumHeight(2, 75)

		login_checkbox = QCheckBox(self)
		login_checkbox.setGeometry(0, 0, 100, 180)
		login_checkbox.setStyleSheet("QCheckBox::indicator"
							"{"
							"width :40px;"
							"height : 40px;"
							"}")
		login_checkbox.setText("Запомнить имя пользователя")
		layout.addWidget(login_checkbox, 4, 0, 1, 4)

		self.main = AppWindow()
		self.setLayout(layout)

		self.main.logout_button.clicked.connect(self.logout_button_was_clicked)

	def check_password(self):
		msg = QMessageBox()
		msg.setWindowTitle('Error')
		msg.setFixedSize(300, 300)
		if self.lineEdit_username.text() == 'user' and self.lineEdit_password.text() == '0000':
			self.main.show()
			self.hide()
			self.lineEdit_password.clear()		
		else:
			msg.setText('Incorrect Password')
			msg.exec_()
		
	def center(self):
		qr = self.frameGeometry()
		cp = QDesktopWidget().availableGeometry().center()
		qr.moveCenter(cp)
		self.move(qr.topLeft())

	def logout_button_was_clicked(self):
		self.main.hide()
		self.show()	

class Thread(QThread):
	changePixmap = pyqtSignal(QImage)

	def __init__(self):
		super().__init__()
		self.should_run = False
		self.close_event = threading.Event()

	def run(self):
		self.cap = cv2.VideoCapture(0)
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
					p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
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
		self.save_button = QPushButton("Сохранить", checkable=True)

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
		self.cancle_button = QPushButton("Отмена", checkable=True)		

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

	def setImage(self, image):
		self.label.setPixmap(QPixmap.fromImage(image))

	def init_label(self):
		self.label.setPixmap(QPixmap())

	def initUI(self):

		self.button_is_checked = False
		self.thread = None

		self.setWindowTitle('Сохранение изображения')
		self.resize(1800, 1200)
		self.center()

		self.thread = Thread()
		self.thread.start()
		self.thread.startThread(True)

		self.label = QLabel(self)
		self.label.resize(1280, 720)

		self.save_snap_button = QPushButton("Сохранение кадра", checkable=True)
		self.save_snap_button.setChecked(self.button_is_checked)
		self.save_snap_button.setFixedWidth(700)
		self.save_snap_button.setFixedHeight(100)

		self.auto_save_snap_button = QPushButton("Не открывать диалог с данными кадра", checkable=True)
		self.auto_save_snap_button.setChecked(self.button_is_checked)
		self.auto_save_snap_button.setFixedWidth(700)
		self.auto_save_snap_button.setFixedHeight(100)

		self.logout_button = QPushButton("Выход", checkable=True)
		self.logout_button.setChecked(self.button_is_checked)
		self.logout_button.setFixedWidth(700)
		self.logout_button.setFixedHeight(100)

		layout = QVBoxLayout(self)
		layout.addWidget(self.save_snap_button)
		layout.addWidget(self.auto_save_snap_button)
		layout.addWidget(self.label)
		layout.addWidget(self.logout_button)

		self.thread.changePixmap.connect(self.setImage)
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
		self.frame = self.thread.frame
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
	ex = LoginWindow()
	ex.show()
	app.exec()