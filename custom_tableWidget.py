from PyQt4 import QtCore, QtGui

class CustomTableWidget(QtGui.QTableWidget):
    def __init__(self, parent = None):
        super(CustomTableWidget, self).__init__(parent)
        self.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
        self.setFocusPolicy(QtCore.Qt.NoFocus)

    def selectRow(self, p_int):
       #do nothing
       return

    def editItem(self, QTableWidgetItem):
        # do nothing
        return
