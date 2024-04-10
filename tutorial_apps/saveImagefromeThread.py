import cv2
import sys
from PyQt5.QtWidgets import  QWidget, QLabel, QApplication, QPushButton, QVBoxLayout, QFileDialog, QSpinBox, QHBoxLayout, QComboBox
from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
import threading
from random import randint

class Thread(QThread):
	changePixmap = pyqtSignal(QImage)

	def __init__(self):
		super().__init__()
		self.should_run = False
		self.close_event = threading.Event()

	def run(self):
		self.cap = cv2.VideoCapture(0)
		while True:
			if self.should_run:
				ret, self.frame = self.cap.read()
				if ret:
					rgbImage = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
					h, w, ch = rgbImage.shape
					bytesPerLine = ch * w
					convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
					self.changePixmap.emit(convertToQtFormat)
				if self.close_event.is_set():
					self.cap.release()
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

class App(QWidget):
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

		self.thread = Thread()
		self.thread.start()
		self.thread.startThread(True)

		self.label = QLabel(self)
		self.label.resize(640, 480)

		self.button = QPushButton("Сохранение кадра", checkable=True)
		self.button.setChecked(self.button_is_checked)
		self.button.setFixedWidth(400)
		self.button.setFixedHeight(100)

		layout = QVBoxLayout(self)
		layout.addWidget(self.button)
		layout.addWidget(self.label)

		self.thread.changePixmap.connect(self.setImage)
		self.button.clicked.connect(self.the_button_was_clicked)
		self.w = AnotherWindow()
		self.w.save_button.clicked.connect(self.save_button_was_clicked)

	def the_button_was_clicked(self):
		if self.w.isVisible():
			self.w.hide()
		else:
			self.w.show()

	def save_button_was_clicked(self, image):
		self.frame = self.thread.frame
		self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
		image = QImage(self.frame, self.frame.shape[1], self.frame.shape[0], QImage.Format_RGB888)
		filename, _ = QFileDialog.getSaveFileName(self, "Save Photo", "", "JPEG Image (*.jpg)")
		if filename:
			image.save(filename, "jpg")

if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = App()
	ex.show()
	app.exec()