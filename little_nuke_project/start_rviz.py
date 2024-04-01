import roslib; roslib.load_manifest('rviz_python_tutorial')
from rviz import bindings as rviz


class StartRviz():
    def __init__(self):
        self.frame = rviz.VisualizationFrame()
        self.frame.setSplashPath( "" )
        self.frame.initialize()
        reader = rviz.YamlConfigReader()
        config = rviz.Config()
        reader.readFile( config, "turtle_bot.rviz" )
        self.frame.load( config )
        self.frame.setMenuBar( None )
        self.frame.setStatusBar( None )
        self.frame.setEnabled(False)
        self.frame.setHideButtonVisibility( False )
        self.manager = self.frame.getManager()
        self.grid_display = self.manager.getRootDisplayGroup().getDisplayAt( 0 )