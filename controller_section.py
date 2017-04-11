from PyQt4 import QtCore, QtGui
from new_controller_dialog import NewControllerDialog
from custom_tableWidget import CustomTableWidget
from widget_util import *

class ControllerSection(QtGui.QFrame):
    def __init__(self, parent=None):
        super(ControllerSection, self).__init__(parent)

        #Create frames
        controller_left_frame = QtGui.QFrame(self)
        controller_right_frame = QtGui.QFrame(self)

        #Create layouts and add content
        controller_left_layout = QtGui.QVBoxLayout(controller_left_frame)
        controller_left_layout.addWidget(self.createControllerComboBox())
        controller_left_layout.addWidget(self.createControllerUnitTable())

        controller_right_layout = QtGui.QVBoxLayout(controller_right_frame)
        controller_right_layout.addLayout(self.createControllerButtons())
        controller_right_layout.addWidget(self.createControllerElectrodeTable())

        controller_section_layout = QtGui.QHBoxLayout(self)

        #Add left and right frames to main controller frame
        controller_section_layout.addWidget(controller_left_frame)
        controller_section_layout.addWidget(controller_right_frame)

        self.setLayout(controller_section_layout)
        self.setProperty("frameType", "sectionFrame")

        effect = QtGui.QGraphicsDropShadowEffect(self)
        effect.setOffset(0, 0)
        effect.setBlurRadius(2)
        effect.setColor(QtGui.QColor("#333333"))
        self.setGraphicsEffect(effect)

    def createNewControllerDialog(self):
        dialog = NewControllerDialog("New Controller", self)
        return dialog

    def createControllerComboBox(self):
        combo_box = QtGui.QComboBox()
        for i in range(2,7):
            combo_box.addItem("Fieldscale FcT520"+str(i))

        combo_box.setFixedWidth(250)

        return combo_box

    def createControllerButtons(self):
        add_controller_button = QtGui.QPushButton("Add Controller")
        add_controller_button.clicked.connect(lambda: self.newControllerPressed())
        edit_button = QtGui.QPushButton("Edit")
        delete_button = QtGui.QPushButton("Delete")

        button_layout = QtGui.QHBoxLayout()
        button_layout.addWidget(add_controller_button)
        button_layout.addWidget(edit_button)
        button_layout.addWidget(delete_button)

        return button_layout

    def createControllerUnitTable(self):
        unit_table = CustomTableWidget()
        unit_table.setColumnCount(2)
        unit_table.setRowCount(3)

        unit_table.setHorizontalHeaderItem(0, createHeaderItem("Parameters"))
        unit_table.setHorizontalHeaderItem(1, createHeaderItem("Unit (p/l)"))

        unit_table.horizontalHeader().setProperty("headerType", "tableHeader")

        unit_table.setItem(0, 0, createTableWidgetItem("Cmin"))
        unit_table.setItem(0, 1, createTableWidgetItem("1"))
        unit_table.setItem(1, 0, createTableWidgetItem("Cmax"))
        unit_table.setItem(1, 1, createTableWidgetItem("2.5"))
        unit_table.setItem(2, 0, createTableWidgetItem("Sensitivity"))
        unit_table.setItem(2, 1, createTableWidgetItem("0.0851"))

        unit_table.setShowGrid(False)
        unit_table.verticalHeader().setVisible(False)
        unit_table.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)

        header = unit_table.horizontalHeader()
        header.setResizeMode(1, QtGui.QHeaderView.Stretch)
        header.setResizeMode(2, QtGui.QHeaderView.Stretch)

        unit_table.setFixedHeight(250)

        return unit_table

    def createControllerElectrodeTable(self):
        electrode_table = CustomTableWidget()
        electrode_table.setColumnCount(3)
        electrode_table.setRowCount(2)

        electrode_table.setHorizontalHeaderItem(0, createHeaderItem("Electrodes"))
        electrode_table.setHorizontalHeaderItem(1, createHeaderItem("Total"))
        electrode_table.setHorizontalHeaderItem(2, createHeaderItem("Active"))

        electrode_table.setItem(0,0, createTableWidgetItem("X Electrodes"))
        electrode_table.setItem(0,1, createTableWidgetItem("22"))
        electrode_table.setCellWidget(0,2, self.createElectrodeTableCombo())
        electrode_table.setItem(1,0, createTableWidgetItem("Y Electrodes"))
        electrode_table.setItem(1,1, createTableWidgetItem("30"))
        electrode_table.setCellWidget(1,2, self.createElectrodeTableCombo())

        electrode_table.setShowGrid(False)
        electrode_table.verticalHeader().setVisible(False)
        electrode_table.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        electrode_table.horizontalHeader().setProperty("headerType", "tableHeader")

        header = electrode_table.horizontalHeader()
        header.setResizeMode(1, QtGui.QHeaderView.Stretch)
        header.setResizeMode(2, QtGui.QHeaderView.Stretch)

        electrode_table.setFixedHeight(250)

        return electrode_table

    def createElectrodeTableCombo(self):
        box = QtGui.QComboBox()
        for i in range(1, 4):
            box.addItem(str(i))

        return box

    @QtCore.pyqtSlot(name="newController")
    def newControllerPressed(self):
        dialog = self.createNewControllerDialog()
        dialog.exec_();