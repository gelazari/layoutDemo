from PyQt4 import QtCore, QtGui

class CustomLineEdit(QtGui.QLineEdit):
    def __init__(self, parent=None, field = None):
        super(CustomLineEdit, self).__init__(parent)
        self.field = field
        self.setProperty("fieldType", "lineEdit")

    def focusInEvent(self, QFocusEvent):
        QtGui.QLineEdit.focusInEvent(self, QtGui.QFocusEvent(QtCore.QEvent.FocusIn))

        if self.field != None:
            self.parent().parent().setBottomFieldVisibility(self.field)
            effect = QtGui.QGraphicsDropShadowEffect(self)
            effect.setOffset(0, 0)
            effect.setBlurRadius(10)
            effect.setColor(QtGui.QColor("#6533AC"))
            self.setGraphicsEffect(effect)
        else:
            effect = QtGui.QGraphicsDropShadowEffect(self)
            effect.setOffset(0, 0)
            effect.setBlurRadius(10)
            effect.setColor(QtGui.QColor("#1053DA"))
            self.setGraphicsEffect(effect)

    def focusOutEvent(self, QFocusEvent):
        QtGui.QLineEdit.focusOutEvent(self, QtGui.QFocusEvent(QtCore.QEvent.FocusOut))
        self.setGraphicsEffect(None)
