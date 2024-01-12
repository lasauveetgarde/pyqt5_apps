import sys
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget
from pyqtlet import L, MapWidget

class MapWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.mapWidget = MapWidget()
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.mapWidget)
        self.setLayout(self.layout)
        self.map = L.map(self.mapWidget)
        self.map.setView([59.9714983246993, 30.320694959125], 15)
        L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}', {'noWrap': 'true'}).addTo(self.map)
        self.marker = L.marker([59.9714983246993, 30.320694959125])
        self.circle = L.circle([59.9714983246993, 30.320694959125], 100)
        self.marker.bindPopup('LETI')
        self.map.addLayer(self.marker)
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = MapWindow()
    widget.setWindowTitle('PYQT5 Map Example')
    sys.exit(app.exec_())