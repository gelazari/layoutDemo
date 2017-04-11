from PyQt4 import QtCore, QtGui

class CustomCheckBox(QtGui.QCheckBox):
    def __init__(self, parent=None):
        super(CustomCheckBox, self).__init__(parent)
