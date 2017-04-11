from PyQt4 import QtCore, QtGui
from widget_util import *

class PatternSection(QtGui.QFrame):
    def __init__(self, parent=None):
        super(PatternSection, self).__init__(parent)

        effect = QtGui.QGraphicsDropShadowEffect(self)
        effect.setOffset(0, 0)
        effect.setBlurRadius(2)
        effect.setColor(QtGui.QColor("#333333"))
        self.setGraphicsEffect(effect)
