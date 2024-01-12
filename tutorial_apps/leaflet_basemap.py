import sys
import json
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget, QLabel
from PyQt5 import QtWebEngineWidgets

from ipyleaflet import Map, Marker, LayersControl, basemaps
from ipywidgets import HTML, IntSlider
from ipywidgets.embed import embed_data


class MapWindow(QWidget):
    def __init__(self, base_coords):
        self.base_coords = base_coords
        # Setting up the widgets and layout
        super().__init__()
        self.layout = QVBoxLayout()
        self.title = QLabel("<b>This is my title</b>")
        self.layout.addWidget(self.title)

        self.web = QtWebEngineWidgets.QWebEngineView(self)

        s1 = IntSlider(max=200, value=100)
        s2 = IntSlider(value=40)
        self.map = Map(center=self.base_coords, basemaps=basemaps.Esri.WorldTopoMap, zoom=10)

        self.marker = Marker(location=self.base_coords)
        self.marker.popup = HTML(value='This is my marker')
        self.map.add_layer(self.marker)

        data = embed_data(views=[s1, s2, self.map])
        self.layout.addWidget(self.web)
        self.setLayout(self.layout)

        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    base_coords = [45.783119, 3.123364]
    widget = MapWindow(base_coords)
    widget.resize(900, 800)
    sys.exit(app.exec_())
