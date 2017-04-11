from PyQt4 import QtCore, QtGui

class CustomComboBox(QtGui.QComboBox):
    def __init__(self, parent=None, handler = None):
        super(CustomComboBox, self).__init__(parent)
        self.setProperty("fieldType", "comboBox")
        if handler != None:
            self.connect(self, QtCore.SIGNAL("currentIndexChanged(const int)"), handler)

    def onSelection(self):
        print(self.currentIndex())

    def focusInEvent(self, QFocusEvent):
        QtGui.QComboBox.focusInEvent(self, QtGui.QFocusEvent(QtCore.QEvent.FocusIn))

        effect = QtGui.QGraphicsDropShadowEffect(self)
        effect.setOffset(0, 0)
        effect.setBlurRadius(15)
        effect.setColor(QtGui.QColor("#1053DA"))
        self.setGraphicsEffect(effect)

    def focusOutEvent(self, QFocusEvent):
        QtGui.QComboBox.focusOutEvent(self, QtGui.QFocusEvent(QtCore.QEvent.FocusOut))
        self.setGraphicsEffect(None)

    def activated(self, index):
        print(self.currentIndex())
        print(index)