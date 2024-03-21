#!/usr/bin/env python

import roslib; roslib.load_manifest('rviz_python_tutorial')
import sys
from rviz import bindings as rviz
from PyQt5.QtWidgets import  QWidget, QHBoxLayout, QApplication, QVBoxLayout, QPushButton, QSlider
from PyQt5.QtCore import  Qt, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap

class MyViz( QWidget ):
    def __init__(self):
        QWidget.__init__(self)

        self.frame = rviz.VisualizationFrame()
        self.frame.setSplashPath( "" )
        self.frame.initialize()
        reader = rviz.YamlConfigReader()
        config = rviz.Config()
        reader.readFile( config, "rs.rviz" )
        self.frame.load( config )

        self.setWindowTitle( config.mapGetChild( "Title" ).getValue() )
        self.frame.setMenuBar(None)
        self.frame.setStatusBar( None )
        self.frame.setHideButtonVisibility( True )
        
        layout = QVBoxLayout()
        layout.addWidget( self.frame )        
        self.setLayout( layout )

if __name__ == '__main__':
    app = QApplication( sys.argv )

    myviz = MyViz()
    myviz.resize( 500, 500 )
    myviz.show()

    app.exec_()