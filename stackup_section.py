from PyQt4 import QtCore, QtGui
from custom_combobox import CustomComboBox
from custom_lineEdit import CustomLineEdit
from widget_util import *

class StackUpSection(QtGui.QFrame):
    def __init__(self, parent=None):
        super(StackUpSection, self).__init__(parent)

        layout = QtGui.QVBoxLayout()
        layout.setContentsMargins(16, 8, 16, 8)

        effect = QtGui.QGraphicsDropShadowEffect(self)
        effect.setOffset(0, 0)
        effect.setBlurRadius(2)
        effect.setColor(QtGui.QColor("#333333"))
        self.setGraphicsEffect(effect)

        self.setProperty("frameType", "sectionFrame")

        top_row_layout = QtGui.QHBoxLayout()
        layer_num_label = QtGui.QLabel("Number of layers")
        layer_combo = CustomComboBox()
        for i in range(10):
            layer_combo.addItem(str(i + 1))

        add_material_button = self.createStackupAddMaterialButton("Add Material", "./images/stackup/add.svg")
        edit_button = self.createBorderOnlyStackupButtons("Edit", "./images/stackup/edit.svg")
        delete_button = self.createBorderOnlyStackupButtons("Delete", "./images/stackup/delete.svg")

        top_row_layout.addWidget(layer_num_label, 0, QtCore.Qt.AlignLeft)
        top_row_layout.addWidget(layer_combo, 0, QtCore.Qt.AlignLeft)
        top_row_layout.addWidget(add_material_button, 1, QtCore.Qt.AlignRight)
        top_row_layout.addWidget(edit_button, 0, QtCore.Qt.AlignRight)
        top_row_layout.addWidget(delete_button, 0, QtCore.Qt.AlignRight)
        top_row_layout.setContentsMargins(0, 0, 0, 0)

        bottom_layout = QtGui.QHBoxLayout()
        bottom_layout.setContentsMargins(0, 0, 0, 0)

        left_frame = QtGui.QFrame()
        left_frame.setFixedWidth(250)
        left_frame.setStyleSheet("background-color: black;")

        right_frame = QtGui.QVBoxLayout()
        right_frame.setContentsMargins(0, 0, 0, 0)
        right_frame.setSpacing(0)

        bottom_layout.addWidget(left_frame)

        border_label = QtGui.QLabel("")
        border_label.setFixedHeight(4)
        border_label.setStyleSheet("border: 2px solid #ededed;")

        empty_label = QtGui.QLabel("")
        material_label = QtGui.QLabel("MATERIAL")
        rel_perm_label = QtGui.QLabel("RELATIVE PERMITTIVETY")
        thickness_label = QtGui.QLabel("THICKNESS")
        gp_label = QtGui.QLabel("GROUNDED PLANE")

        material_label.setProperty("labelType", "stackUpDescLabel")
        rel_perm_label.setProperty("labelType", "stackUpDescLabel")
        thickness_label.setProperty("labelType", "stackUpDescLabel")
        gp_label.setProperty("labelType", "stackUpDescLabel")

        label_layout = QtGui.QGridLayout()
        label_layout.addWidget(empty_label, 0, 0, QtCore.Qt.AlignCenter)
        label_layout.addWidget(material_label, 0, 1, QtCore.Qt.AlignCenter)
        label_layout.addWidget(rel_perm_label, 0, 2, QtCore.Qt.AlignCenter)
        label_layout.addWidget(thickness_label, 0, 3, QtCore.Qt.AlignCenter)
        label_layout.addWidget(gp_label, 0, 4, QtCore.Qt.AlignCenter)
        label_layout.setColumnStretch(0, 1)
        label_layout.setColumnStretch(1, 1)
        label_layout.setColumnStretch(2, 1)
        label_layout.setColumnStretch(3, 1)
        label_layout.setColumnStretch(4, 1)

        layout.addLayout(top_row_layout)
        layout.addWidget(border_label)
        right_frame.addLayout(label_layout)

        self.layer_list = []

        for i in range(10):
            layer_frame = QtGui.QFrame(self)
            layer_frame_layout = QtGui.QGridLayout(layer_frame)
            layer_frame_layout.setContentsMargins(0, 0, 0, 0)

            layer_label = QtGui.QLabel("Layer " + str(i))
            layer_label.setObjectName("layer_label")
            material = CustomComboBox()
            material.setObjectName("material")
            material.addItem("Material 1")
            material.addItem("Material 2")
            material.addItem("Material 3")
            rel_perm = CustomLineEdit()
            rel_perm.setObjectName("rel_perm")
            thickness = QtGui.QLabel("4")
            thickness.setObjectName("thickness")
            thickness.setAlignment(QtCore.Qt.AlignCenter)
            grounded = QtGui.QCheckBox()
            grounded.setObjectName("grounded")

            layer_frame_layout.setColumnStretch(0, 1)
            layer_frame_layout.setColumnStretch(1, 1)
            layer_frame_layout.setColumnStretch(2, 1)
            layer_frame_layout.setColumnStretch(3, 1)
            layer_frame_layout.setColumnStretch(4, 1)

            layer_frame_layout.addWidget(layer_label, 0, 0)
            layer_frame_layout.addWidget(material, 0, 1)
            layer_frame_layout.addWidget(rel_perm, 0, 2)
            layer_frame_layout.addWidget(thickness, 0, 3)
            layer_frame_layout.addWidget(grounded, 0, 4, QtCore.Qt.AlignCenter)

            layer_frame.setProperty("frameType", "layerRowFrame")
            print(layer_frame.height())
            right_frame.addWidget(layer_frame)

            self.layer_list.append(layer_frame)

        bottom_layout.addLayout(right_frame)
        self.disableLayer(3)
        self.disableLayer(4)
        self.disableLayer(5)
        self.disableLayer(6)
        self.disableLayer(7)
        self.disableLayer(8)
        self.disableLayer(9)
        layout.addLayout(bottom_layout)

        self.setLayout(layout)

    def disableLayer(self, i):
        frame = self.layer_list[i]
        frame.setStyleSheet("background-color: #ededed")

        frame.findChild(QtGui.QLabel, "layer_label").setDisabled(True)
        frame.findChild(CustomComboBox, "material").setDisabled(True)
        frame.findChild(CustomLineEdit, "rel_perm").setDisabled(True)
        frame.findChild(QtGui.QLabel, "thickness").setDisabled(True)
        frame.findChild(QtGui.QCheckBox, "grounded").setDisabled(True)


    def enableLayer(self, i):
        frame = self.layer_list[i]
        frame.setStyleSheet("background-color: #ffffff")

        frame.findChild(QtGui.QLabel, "layer_label").setDisabled(False)
        frame.findChild(CustomComboBox, "material").setDisabled(False)
        frame.findChild(CustomLineEdit, "rel_perm").setDisabled(False)
        frame.findChild(QtGui.QLabel, "thickness").setDisabled(False)
        frame.findChild(QtGui.QCheckBox, "grounded").setDisabled(False)

    def createBorderOnlyStackupButtons(self, text, img):
        button = QtGui.QToolButton()
        button.setProperty("buttonType", "borderOnlyStackupButton")
        button.setFixedHeight(28)

        button.setObjectName(text+"Button")
        button.setText(text)
        button.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        button.setIcon(QtGui.QIcon(img))
        button.setIconSize(QtCore.QSize(20, 20))
        return button

    def createStackupAddMaterialButton(self, text, img):
        button = QtGui.QToolButton()
        button.setProperty("buttonType", "stackupAddMaterialButton")
        button.setFixedHeight(28)

        button.setObjectName(text+"Button")
        button.setText(text)
        button.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        button.setIcon(QtGui.QIcon(img))
        button.setIconSize(QtCore.QSize(20, 20))
        return button
