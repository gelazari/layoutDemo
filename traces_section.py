from PyQt4 import QtCore, QtGui
from custom_checkbox import CustomCheckBox
from custom_lineEdit import CustomLineEdit
from widget_util import *

class TracesSection(QtGui.QFrame):
    def __init__(self, parent=None):
        super(TracesSection, self).__init__(parent)

        traces_layout = QtGui.QHBoxLayout()

        right_frame = QtGui.QFrame()
        right_frame_layout = QtGui.QVBoxLayout()
        right_frame_layout.setContentsMargins(12, 0, 0, 0)

        right_top_frame = QtGui.QFrame()
        right_top_frame.setProperty("frameType", "sectionFrame")
        right_top_frame.setSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Maximum)
        right_top_frame.setFixedWidth(250)
        right_top_layout = QtGui.QVBoxLayout()

        right_bot_frame = QtGui.QFrame()
        right_bot_layout = QtGui.QVBoxLayout()
        circuit_label = QtGui.QLabel()
        circuit_label.setPixmap(QtGui.QPixmap("./images/traces/circuit.png"))

        optional_label = QtGui.QLabel("Optional")
        optional_label.setProperty("labelType", "tracesDescLabel")

        dieelectric_label = QtGui.QLabel("Dieelectric Constant Er")
        dieelectric_label.setProperty("labelType", "tracesNormalLabel")
        dieelectric_field = CustomLineEdit()

        dieelectric_layout = QtGui.QGridLayout()
        dieelectric_layout.addWidget(dieelectric_label, 0, 0)
        dieelectric_layout.addWidget(dieelectric_field, 0, 1)
        dieelectric_layout.setColumnStretch(0, 1)
        dieelectric_layout.setColumnStretch(1, 1)

        resistance_checkbox = CustomCheckBox()
        resistance_checkbox.setProperty("checkBoxType", "tracesCheckBox")
        resistance_label = QtGui.QLabel("Resistance Computation")
        resistance_label.setProperty("labelType", "tracesNormalLabel")
        resistance_label.setAlignment(QtCore.Qt.AlignCenter)

        resistance_layout = QtGui.QGridLayout()
        resistance_layout.addWidget(resistance_checkbox, 0, 0)
        resistance_layout.addWidget(resistance_label, 0, 1)
        resistance_layout.setColumnStretch(1, 1)

        resistivity_layout = QtGui.QGridLayout()
        resistivity_label = QtGui.QLabel("Resistivity (p)")
        resistivity_label.setProperty("labelType", "tracesNormalLabel")

        resistivety_field = CustomLineEdit()
        resistivity_unit_label = QtGui.QLabel("W*m")
        resistivity_unit_label.setProperty("labelType", "tracesNormalLabel")

        resistivity_layout.addWidget(resistivity_label, 0, 0)
        resistivity_layout.addWidget(resistivety_field, 0, 1)
        resistivity_layout.addWidget(resistivity_unit_label, 0, 2)
        resistivity_layout.setColumnStretch(0, 2)
        resistivity_layout.setColumnStretch(1, 2)
        resistivity_layout.setColumnStretch(2, 1)

        left_frame = QtGui.QFrame()
        left_frame.setFixedWidth(250)
        left_frame.setProperty("frameType", "sectionFrame")  # Same styling
        left_frame_layout = QtGui.QVBoxLayout()

        left_top_layout = QtGui.QGridLayout()

        traces_label = QtGui.QLabel("TRACES")
        traces_label.setProperty("labelType", "tracesDescLabel")

        no_of_traces_label = QtGui.QLabel("No of traces")
        no_of_traces_label.setProperty("labelType", "tracesNormalLabel")

        width_label = QtGui.QLabel("Width (W)")
        width_label.setProperty("labelType", "tracesNormalLabel")

        thickness_label = QtGui.QLabel("Thickness (T)")
        thickness_label.setProperty("labelType", "tracesNormalLabel")

        no_of_traces_field = CustomLineEdit()
        width_field = CustomLineEdit()
        thickness_field = CustomLineEdit()

        left_top_layout.addWidget(no_of_traces_label, 0, 0)
        left_top_layout.addWidget(width_label, 1, 0)
        left_top_layout.addWidget(thickness_label, 2, 0)

        left_top_layout.addWidget(no_of_traces_field, 0, 1)
        left_top_layout.addWidget(width_field, 1, 1)
        left_top_layout.addWidget(thickness_field, 2, 1)

        left_top_layout.setColumnStretch(0, 2)
        left_top_layout.setColumnStretch(1, 1)
        left_top_layout.setColumnStretch(2, 1)

        spacing_margins_label = QtGui.QLabel("SPACING & MARGINS")
        spacing_margins_label.setProperty("labelType", "tracesDescLabel")
        spacing_label = QtGui.QLabel("Spacing (S)")
        spacing_label.setProperty("labelType", "tracesNormalLabel")

        margins_label = QtGui.QLabel("Margins")
        margins_label.setProperty("labelType", "tracesNormalLabel")

        spacing_field = CustomLineEdit()

        spacing_layout = QtGui.QGridLayout()
        spacing_layout.addWidget(spacing_label, 0, 0)
        spacing_layout.addWidget(spacing_field, 0, 1)

        spacing_layout.setColumnStretch(0, 2)
        spacing_layout.setColumnStretch(1, 1)
        spacing_layout.setColumnStretch(2, 1)

        margins_layout = QtGui.QGridLayout()
        margins_layout.setAlignment(QtCore.Qt.AlignCenter)

        x1_label = QtGui.QLabel("X1")
        x2_label = QtGui.QLabel("X2")
        y1_label = QtGui.QLabel("Y1")
        y2_label = QtGui.QLabel("Y2")

        x1_label.setAlignment(QtCore.Qt.AlignCenter)
        x2_label.setAlignment(QtCore.Qt.AlignCenter)
        y1_label.setAlignment(QtCore.Qt.AlignCenter)
        y2_label.setAlignment(QtCore.Qt.AlignCenter)

        x1_field = CustomLineEdit()
        x2_field = CustomLineEdit()
        y1_field = CustomLineEdit()
        y2_field = CustomLineEdit()

        margins_layout.addWidget(x1_label, 0, 0)
        margins_layout.addWidget(x2_label, 1, 0)
        margins_layout.addWidget(y1_label, 2, 0)
        margins_layout.addWidget(y2_label, 3, 0)

        margins_layout.addWidget(x1_field, 0, 1)
        margins_layout.addWidget(x2_field, 1, 1)
        margins_layout.addWidget(y1_field, 2, 1)
        margins_layout.addWidget(y2_field, 3, 1)

        margins_layout.setColumnStretch(0, 2)
        margins_layout.setColumnStretch(1, 1)
        margins_layout.setColumnStretch(2, 1)

        effect_left = QtGui.QGraphicsDropShadowEffect(self)
        effect_left.setOffset(0, 0)
        effect_left.setBlurRadius(2)
        effect_left.setColor(QtGui.QColor("#333333"))

        effect_right_top = QtGui.QGraphicsDropShadowEffect(self)
        effect_right_top.setOffset(0, 0)
        effect_right_top.setBlurRadius(2)
        effect_right_top.setColor(QtGui.QColor("#333333"))

        left_frame.setGraphicsEffect(effect_left)
        right_top_frame.setGraphicsEffect(effect_right_top)

        right_top_layout.addWidget(optional_label)
        right_top_layout.addWidget(createSpacer(4))
        right_top_layout.addLayout(dieelectric_layout)
        right_top_layout.addWidget(createSpacer(16))
        right_top_layout.addLayout(resistance_layout)
        right_top_layout.addWidget(createSpacer(2))
        right_top_layout.addLayout(resistivity_layout)
        right_top_layout.addWidget(createSpacer(4))
        right_top_frame.setLayout(right_top_layout)

        right_bot_layout.addWidget(circuit_label)
        right_bot_frame.setLayout(right_bot_layout)

        right_frame_layout.addWidget(right_top_frame, 0, QtCore.Qt.AlignTop)
        right_frame_layout.addWidget(right_bot_frame, 0, QtCore.Qt.AlignBottom)

        right_frame.setLayout(right_frame_layout)

        left_frame_layout.addWidget(traces_label)
        left_frame_layout.addLayout(left_top_layout)
        left_frame_layout.addWidget(spacing_margins_label)
        left_frame_layout.addLayout(spacing_layout)
        left_frame_layout.addWidget(margins_label)
        left_frame_layout.addLayout(margins_layout)
        left_frame.setLayout(left_frame_layout)

        traces_layout.addWidget(left_frame)
        traces_layout.addWidget(right_frame)
        self.setLayout(traces_layout)

