from PyQt4 import QtCore, QtGui
from new_controller_dialog import NewControllerDialog
from custom_tableWidget import CustomTableWidget
from custom_combobox import CustomComboBox
from custom_lineEdit import CustomLineEdit
from widget_util import *

class ControllerSection(QtGui.QFrame):
    def __init__(self, parent=None):
        super(ControllerSection, self).__init__(parent)

        #Create frames
        controller_left_frame = QtGui.QFrame(self)
        controller_right_frame = QtGui.QFrame(self)

        #Create layouts and add content
        controller_left_layout = QtGui.QVBoxLayout(controller_left_frame)
        controller_left_layout.addWidget(self.createControllerComboBox(), 0, QtCore.Qt.AlignHCenter)
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
        combo_box = CustomComboBox()
        for i in range(2,7):
            combo_box.addItem("Fieldscale FcT520"+str(i))

        combo_box.setFixedWidth(250)

        return combo_box

    def createControllerButtons(self):
        add_controller_button = QtGui.QPushButton("Add Controller")
        add_controller_button.clicked.connect(lambda: self.newControllerPressed())
        edit_button = QtGui.QPushButton("Edit")
        delete_button = QtGui.QPushButton("Delete")

        add_controller_button.setProperty("buttonType","controllerAddControllerButton")
        edit_button.setProperty("buttonType","borderOnlyControllerButton")
        delete_button.setProperty("buttonType","borderOnlyControllerButton")

        add_controller_button.setFixedHeight(32)
        edit_button.setFixedHeight(32)
        delete_button.setFixedHeight(32)

        button_layout = QtGui.QHBoxLayout()
        button_layout.addWidget(add_controller_button)
        button_layout.addWidget(edit_button)
        button_layout.addWidget(delete_button)

        return button_layout

    def createControllerUnitTable(self):
        unit_table = QtGui.QFrame()
        unit_table.setProperty("tableType","controllerUnitTable")
        unit_table.setSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Maximum)
        unit_table_layout = QtGui.QVBoxLayout()
        unit_table_layout.setContentsMargins(0,0,0,0)

        header_frame = QtGui.QFrame()
        header_layout = QtGui.QGridLayout()
        parameters_label = QtGui.QLabel("Parameters")
        unit_label = QtGui.QLabel("Unit (p/l)")

        header_layout.addWidget(parameters_label,0,0)
        header_layout.addWidget(unit_label,0,1)

        header_layout.setColumnStretch(0,1)
        header_layout.setColumnStretch(1,1)

        header_frame.setLayout(header_layout)

        header_frame.setProperty("rowType","unitTableHeader")

        unit_table_layout.addWidget(header_frame)

        labels = ["Cmin","Cmax","Sensitivity"]
        values = ["1","2.5","0.0851"]
        for i in range(3):
            layer_frame = QtGui.QFrame(self)
            layer_frame_layout = QtGui.QGridLayout(layer_frame)
            layer_frame_layout.setContentsMargins(0, 0, 0, 0)

            item_label = QtGui.QLabel(labels[i])
            item_value = QtGui.QLabel(values[i])

            layer_frame_layout.setColumnStretch(0, 1)
            layer_frame_layout.setColumnStretch(1, 1)

            layer_frame_layout.addWidget(item_label, 0, 0)
            layer_frame_layout.addWidget(item_value, 0, 1)

            if i%2 != 0:
                layer_frame.setProperty("frameType", "alternateRowFrame")
            else:
                layer_frame.setProperty("frameType", "tableRowFrame")

            unit_table_layout.addWidget(layer_frame)

        unit_table.setLayout(unit_table_layout)
        return unit_table

    def createControllerElectrodeTable(self):
        electrode_table = QtGui.QFrame()
        electrode_table.setProperty("tableType","controllerElectrodeTable")

        electrode_table.setSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Maximum)
        electrode_table_layout = QtGui.QVBoxLayout()
        electrode_table_layout.setContentsMargins(0,0,0,0)

        header_frame = QtGui.QFrame()
        header_layout = QtGui.QGridLayout()
        electrodes_label = QtGui.QLabel("Electrodes")
        total_label = QtGui.QLabel("Total")
        active_label = QtGui.QLabel("Active")

        header_layout.addWidget(electrodes_label, 0, 0)
        header_layout.addWidget(total_label, 0, 1)
        header_layout.addWidget(active_label, 0, 2)

        header_layout.setColumnStretch(0,1)
        header_layout.setColumnStretch(1,1)
        header_layout.setColumnStretch(2,1)

        header_frame.setLayout(header_layout)

        header_frame.setProperty("rowType","electrodeTableHeader")

        electrode_table_layout.addWidget(header_frame)

        labels = ["X Electrodes", "Y Electrodes"]
        values = ["22", "30"]

        for i in range(2):
            layer_frame = QtGui.QFrame(self)
            layer_frame_layout = QtGui.QGridLayout(layer_frame)
            layer_frame_layout.setContentsMargins(0, 0, 0, 0)

            item_label = QtGui.QLabel(labels[i])
            item_value = QtGui.QLabel(values[i])

            layer_frame_layout.setColumnStretch(0, 1)
            layer_frame_layout.setColumnStretch(1, 1)
            layer_frame_layout.setColumnStretch(2, 1)

            layer_frame_layout.addWidget(item_label, 0, 0)
            layer_frame_layout.addWidget(item_value, 0, 1)
            layer_frame_layout.addWidget(self.createElectrodeTableCombo(),0,2)

            layer_frame.setProperty("frameType", "tableRowFrame")
            electrode_table_layout.addWidget(layer_frame)

        electrode_table.setLayout(electrode_table_layout)
        return electrode_table

    def createElectrodeTableCombo(self):
        box = CustomComboBox()
        for i in range(1, 4):
            box.addItem(str(i))

        return box

    @QtCore.pyqtSlot(name="newController")
    def newControllerPressed(self):
        dialog = self.createNewControllerDialog()
        dialog.exec_();