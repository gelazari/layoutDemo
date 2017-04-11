from PyQt4 import QtCore, QtGui
from widget_util import *

class SensorSection(QtGui.QFrame):
    def __init__(self, parent=None):
        super(SensorSection, self).__init__(parent)

        sensor_label = QtGui.QLabel("Sensor Section")
        sensor_button = QtGui.QPushButton("Sensor Button")

        sensor_layout = QtGui.QHBoxLayout(self)
        sensor_layout.addWidget(sensor_label, 0, QtCore.Qt.AlignCenter)
        sensor_layout.addWidget(sensor_button, 0 , QtCore.Qt.AlignCenter)

        self.setLayout(sensor_layout)
        self.setProperty("frameType", "sectionFrame")

        effect = QtGui.QGraphicsDropShadowEffect(self)
        effect.setOffset(0, 0)
        effect.setBlurRadius(2)
        effect.setColor(QtGui.QColor("#333333"))
        self.setGraphicsEffect(effect)

