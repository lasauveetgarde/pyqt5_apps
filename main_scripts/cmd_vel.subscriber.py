#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtCore import Qt

appStyle="""
QMainWindow{
     background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                 stop: 0 #ABAFE5, stop: 1 #8588B2);
}
"""

class MainWindow(QMainWindow):

    def __init__(self):

        super().__init__()
        self.setWindowTitle("My App")
        self.setStyleSheet(appStyle)
        self.widget = QLabel('Linear Velocity')
        font = self.widget.font()
        font.setPointSize(30)
        self.widget.setFont(font)
        self.setCentralWidget(self.widget)
        rospy.init_node('cmd_vel_subscriber', anonymous=True)
        rospy.Subscriber("cmd_vel", Twist, self.cmd_vel_callback)

    def cmd_vel_callback(self, msg):
        rospy.loginfo("Received linear X velocity: %f", msg.linear.x)
        self.linear_speed = str(round(msg.linear.x,4))
        self.value_changed()
    
    def value_changed(self):    
        self.widget.setText(self.linear_speed)

if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        app.exec()
    except rospy.ROSInterruptException:
        pass