from PyQt4 import QtCore, QtGui

def createHeaderItem(text):
    item = QtGui.QTableWidgetItem(text)
    item.setFlags(QtCore.Qt.NoItemFlags)
    item.setFlags(item.flags() ^ QtCore.Qt.ItemIsEditable)
    item.setTextAlignment(QtCore.Qt.AlignCenter)

    return item


def createTableWidgetItem(text):
    item = QtGui.QTableWidgetItem(text)
    item.setFlags(QtCore.Qt.NoItemFlags)
    item.setFlags(item.flags() ^ QtCore.Qt.ItemIsEditable)
    item.setForeground(QtGui.QColor.fromRgb(0, 0, 0))
    item.setTextAlignment(QtCore.Qt.AlignCenter)

    return item

def createSpacer(height = 8):
    spacer = QtGui.QLabel("")
    spacer.setFixedHeight(height)
    return spacer