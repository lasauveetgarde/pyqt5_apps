#!/usr/bin/env python3

import roslib; roslib.load_manifest('rviz_python_tutorial')
import sys
from rviz import bindings as rviz
from PyQt5.QtWidgets import  QWidget, QApplication, QVBoxLayout, QLabel, QTabWidget
from PyQt5.QtCore import  Qt, pyqtSlot

class StartRviz():
    def __init__(self):
        self.frame = rviz.VisualizationFrame()
        self.frame.setSplashPath( "" )
        self.frame.initialize()
        reader = rviz.YamlConfigReader()
        config = rviz.Config()
        reader.readFile( config, "rs.rviz" )
        self.frame.load( config )
        self.frame.setMenuBar( None )
        self.frame.setStatusBar( None )
        self.frame.setHideButtonVisibility( False )
        self.manager = self.frame.getManager()
        self.grid_display = self.manager.getRootDisplayGroup().getDisplayAt( 0 )

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Rviz demostration')
        self.resize(1800, 1200)

        rviz = start_rviz.frame
        layout = QVBoxLayout()
        self.setLayout(layout)
        label = QLabel("Smth else")
        tabwidget = QTabWidget()
        tab1 = QWidget()

        self.rviz_frame = QLabel()
        tab1_layout = QVBoxLayout()
        tab1_layout.addWidget(rviz)
        
        tab1.setLayout(tab1_layout)

        tabwidget.addTab(tab1, "Rviz window")
        tabwidget.addTab(label, "New tab")
        layout.addWidget(tabwidget)

if __name__ == '__main__':
    app = QApplication( sys.argv )
    start_rviz = StartRviz()
    AppWindow = App ()
    AppWindow.show()
    app.exec_()