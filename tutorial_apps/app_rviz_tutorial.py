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
        self.frame.setHideButtonVisibility( False )

        self.manager = self.frame.getManager()
        
        # self.manager.makeTimeLabel()


        self.grid_display = self.manager.getRootDisplayGroup().getDisplayAt( 0 )
        layout = QVBoxLayout()
        layout.addWidget( self.frame )
        
        thickness_slider = QSlider( Qt.Horizontal )
        thickness_slider.setTracking( True )
        thickness_slider.setMinimum( 1 )
        thickness_slider.setMaximum( 1000 )
        thickness_slider.valueChanged.connect( self.onThicknessSliderChanged )
        layout.addWidget( thickness_slider )
        
        h_layout = QHBoxLayout()
        
        top_button = QPushButton( "Top View" )
        top_button.clicked.connect( self.onTopButtonClick )
        h_layout.addWidget( top_button )
        
        side_button = QPushButton( "Side View" )
        side_button.clicked.connect( self.onSideButtonClick )
        h_layout.addWidget( side_button )
        
        layout.addLayout( h_layout )
        
        self.setLayout( layout )

    def onThicknessSliderChanged( self, new_value ):
        if self.grid_display != None:
            self.grid_display.subProp( "Line Style" ).subProp( "Line Width" ).setValue( new_value / 1000.0 )


    def onTopButtonClick( self ):
        self.switchToView( "Top View" )
        
    def onSideButtonClick( self ):
        self.switchToView( "Side View" )

    def switchToView( self, view_name ):
        view_man = self.manager.getViewManager()
        for i in range( view_man.getNumViews() ):
            if view_man.getViewAt( i ).getName() == view_name:
                view_man.setCurrentFrom( view_man.getViewAt( i ))
                return
        print( "Did not find view named %s." % view_name )


if __name__ == '__main__':
    app = QApplication( sys.argv )

    myviz = MyViz()
    myviz.resize( 500, 500 )
    myviz.show()

    app.exec_()