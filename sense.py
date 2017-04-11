from PyQt4 import QtCore, QtGui
from custom_checkbox import CustomCheckBox
from custom_combobox import CustomComboBox
from custom_lineEdit import CustomLineEdit
from custom_tableWidget import CustomTableWidget
from new_controller_dialog import NewControllerDialog
from senseLayout import SenseLayout

class Window(QtGui.QWidget):

    Controller, Sensor, Pattern, StackUp, Traces, Analysis = range(6)

    sectionChanged = QtCore.pyqtSignal(int, name='sectionChanged')

    def __init__(self, parent=None):
        super(Window, self).__init__()

        _central_stacked_widget = 0


        # Because SenseLayout doesn't call its super-class addWidget() it
        # doesn't take ownership of the widgets until setLayout() is called.
        # Therefore we keep a local reference to each label to prevent it being
        # garbage collected too soon.
        central_widget = self.createCentralFrame()
        top_widget = self.createTopFrame()
        left_widget = self.createLeftFrame()
        status_bar = self.createStatusBar()

        layout = SenseLayout()
        layout.setSpacing(0)
        layout.addWidget( top_widget, SenseLayout.Top )
        layout.addWidget( left_widget, SenseLayout.Left)
        layout.addWidget( central_widget, SenseLayout.Middle )
        layout.addWidget(status_bar, SenseLayout.Bottom)
        self.setLayout(layout)
        self.setWindowTitle("Sense Demo")

    @QtCore.pyqtSlot(int, name='changeSection')
    def changeSection(self, section):
        self._central_widget.setCurrentIndex(section)

    @QtCore.pyqtSlot(name="newController")
    def newControllerPressed(self):
        dialog = self.createNewControllerDialog()
        dialog.exec_();

    def createStatusBar(self):
        status_bar = QtGui.QStatusBar()
        status_bar.setProperty("frameType", "statusBar")
        status_bar.showMessage("Fieldscale Sense")
        return status_bar

    def createLabel(self, text):
        label = QtGui.QLabel(text)
        label.setFrameStyle(QtGui.QFrame.Box | QtGui.QFrame.Raised)
        return label

    def createSection(self, section):
        if section == Window.Sensor:
            return self.createSensorSection()
        elif section == Window.Controller:
            return self.createControllerSection()
        elif section == Window.StackUp:
            return self.createStackUpSection()
        elif section == Window.Pattern:
            return self.createPatternSection()
        elif section == Window.Traces:
            return self.createTracesSection()
        elif section == Window.Analysis:
            return self.createAnalysisSection()

    def createSensorSection(self):
        sensor_label = QtGui.QLabel("Sensor Section")

        sensor_button = QtGui.QPushButton("Sensor Button")

        sensor_layout = QtGui.QHBoxLayout(self)
        sensor_layout.addWidget(sensor_label, 0, QtCore.Qt.AlignCenter)
        sensor_layout.addWidget(sensor_button, 0 , QtCore.Qt.AlignCenter)

        sensor_frame = QtGui.QFrame(self)
        sensor_frame.setLayout(sensor_layout)
        sensor_frame.setProperty("frameType", "sectionFrame")

        effect = QtGui.QGraphicsDropShadowEffect(sensor_frame)
        effect.setOffset(0, 0)
        effect.setBlurRadius(2)
        effect.setColor(QtGui.QColor("#333333"))
        sensor_frame.setGraphicsEffect(effect)

        return sensor_frame

    def createControllerSection(self):

        #Create frames
        controller_frame = QtGui.QFrame(self)
        controller_left_frame = QtGui.QFrame(controller_frame)
        controller_right_frame = QtGui.QFrame(controller_frame)

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

        controller_frame.setLayout(controller_section_layout)
        controller_frame.setProperty("frameType", "sectionFrame")

        effect = QtGui.QGraphicsDropShadowEffect(controller_frame)
        effect.setOffset(0, 0)
        effect.setBlurRadius(2)
        effect.setColor(QtGui.QColor("#333333"))
        controller_frame.setGraphicsEffect(effect)

        self.createNewControllerDialog()
        return controller_frame

    def createStackUpSection(self):
        stackup_frame = QtGui.QFrame(self)
        layout = QtGui.QVBoxLayout()
        layout.setContentsMargins(16,8,16,8)

        effect = QtGui.QGraphicsDropShadowEffect(stackup_frame)
        effect.setOffset(0, 0)
        effect.setBlurRadius(2)
        effect.setColor(QtGui.QColor("#333333"))
        stackup_frame.setGraphicsEffect(effect)

        stackup_frame.setProperty("frameType", "sectionFrame")

        top_row_layout = QtGui.QHBoxLayout()
        layer_num_label = QtGui.QLabel("Number of layers")
        layer_combo = CustomComboBox()

        add_material_button = self.createStackupAddMaterialButton("Add Material", "./images/stackup/add.svg")
        edit_button = self.createBorderOnlyStackupButtons("Edit", "./images/stackup/edit.svg")
        delete_button = self.createBorderOnlyStackupButtons("Delete", "./images/stackup/delete.svg")

        top_row_layout.addWidget(layer_num_label, 0, QtCore.Qt.AlignLeft)
        top_row_layout.addWidget(layer_combo, 0, QtCore.Qt.AlignLeft)
        top_row_layout.addWidget(add_material_button, 1, QtCore.Qt.AlignRight)
        top_row_layout.addWidget(edit_button, 0, QtCore.Qt.AlignRight)
        top_row_layout.addWidget(delete_button, 0, QtCore.Qt.AlignRight)
        top_row_layout.setContentsMargins(0,0,0,0)

        bottom_layout = QtGui.QHBoxLayout()
        bottom_layout.setContentsMargins(0,0,0,0)

        left_frame = QtGui.QFrame()
        left_frame.setFixedWidth(250)
        left_frame.setStyleSheet("background-color: black;")

        right_frame = QtGui.QVBoxLayout()
        right_frame.setContentsMargins(0,0,0,0)
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

        material_label.setProperty("labelType","stackUpDescLabel")
        rel_perm_label.setProperty("labelType","stackUpDescLabel")
        thickness_label.setProperty("labelType","stackUpDescLabel")
        gp_label.setProperty("labelType","stackUpDescLabel")

        label_layout = QtGui.QGridLayout()
        label_layout.addWidget(empty_label, 0, 0, QtCore.Qt.AlignCenter)
        label_layout.addWidget(material_label, 0, 1, QtCore.Qt.AlignCenter)
        label_layout.addWidget(rel_perm_label, 0, 2, QtCore.Qt.AlignCenter)
        label_layout.addWidget(thickness_label, 0, 3, QtCore.Qt.AlignCenter)
        label_layout.addWidget(gp_label, 0, 4, QtCore.Qt.AlignCenter)
        label_layout.setColumnStretch(0,1)
        label_layout.setColumnStretch(1,1)
        label_layout.setColumnStretch(2,1)
        label_layout.setColumnStretch(3,1)
        label_layout.setColumnStretch(4,1)

        layout.addLayout(top_row_layout)
        layout.addWidget(border_label)
        right_frame.addLayout(label_layout)

        self.layer_list = []

        for i in range(10):
            layer_frame = QtGui.QFrame(stackup_frame)
            layer_frame_layout = QtGui.QGridLayout(layer_frame)
            layer_frame_layout.setContentsMargins(0,0,0,0)

            layer_label = QtGui.QLabel("Layer "+str(i))
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

        stackup_frame.setLayout(layout)
        return stackup_frame

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

    def createPatternSection(self):
        pattern_frame = QtGui.QFrame(self)

        effect = QtGui.QGraphicsDropShadowEffect(pattern_frame)
        effect.setOffset(0, 0)
        effect.setBlurRadius(2)
        effect.setColor(QtGui.QColor("#333333"))
        pattern_frame.setGraphicsEffect(effect)

        return pattern_frame

    def createTracesSection(self):
        traces_frame = QtGui.QFrame(self)
        traces_layout = QtGui.QHBoxLayout()

        right_frame = QtGui.QFrame()
        right_frame_layout = QtGui.QVBoxLayout()
        right_frame_layout.setContentsMargins(12,0,0,0)

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
        dieelectric_label.setProperty("labelType","tracesNormalLabel")
        dieelectric_field = CustomLineEdit()

        dieelectric_layout = QtGui.QGridLayout()
        dieelectric_layout.addWidget(dieelectric_label,0,0)
        dieelectric_layout.addWidget(dieelectric_field,0,1)
        dieelectric_layout.setColumnStretch(0,1)
        dieelectric_layout.setColumnStretch(1,1)

        resistance_checkbox = CustomCheckBox()
        resistance_checkbox.setProperty("checkBoxType","tracesCheckBox")
        resistance_label = QtGui.QLabel("Resistance Computation")
        resistance_label.setProperty("labelType","tracesBoldLabel")
        resistance_label.setAlignment(QtCore.Qt.AlignCenter)

        resistance_layout = QtGui.QGridLayout()
        resistance_layout.addWidget(resistance_checkbox,0,0)
        resistance_layout.addWidget(resistance_label,0,1)
        resistance_layout.setColumnStretch(1,1)

        resistivity_layout = QtGui.QGridLayout()
        resistivity_label = QtGui.QLabel("Resistivity (p)")
        resistivity_label.setProperty("labelType","tracesNormalLabel")

        resistivety_field = CustomLineEdit()
        resistivity_unit_label = QtGui.QLabel("W*m")
        resistivity_unit_label.setProperty("labelType", "tracesNormalLabel")

        resistivity_layout.addWidget(resistivity_label,0,0)
        resistivity_layout.addWidget(resistivety_field,0,1)
        resistivity_layout.addWidget(resistivity_unit_label,0,2)
        resistivity_layout.setColumnStretch(0,2)
        resistivity_layout.setColumnStretch(1,2)
        resistivity_layout.setColumnStretch(2,1)

        left_frame = QtGui.QFrame()
        left_frame.setFixedWidth(250)
        left_frame.setProperty("frameType", "sectionFrame") #Same styling
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

        left_top_layout.setColumnStretch(0,2)
        left_top_layout.setColumnStretch(1,1)
        left_top_layout.setColumnStretch(2,1)

        spacing_margins_label = QtGui.QLabel("SPACING & MARGINS")
        spacing_margins_label.setProperty("labelType", "tracesDescLabel")
        spacing_label = QtGui.QLabel("Spacing (S)")
        spacing_label.setProperty("labelType", "tracesNormalLabel")

        margins_label = QtGui.QLabel("Margins")
        margins_label.setProperty("labelType", "tracesNormalLabel")

        spacing_field = CustomLineEdit()

        spacing_layout = QtGui.QGridLayout()
        spacing_layout.addWidget(spacing_label,0,0)
        spacing_layout.addWidget(spacing_field,0,1)

        spacing_layout.setColumnStretch(0,2)
        spacing_layout.setColumnStretch(1,1)
        spacing_layout.setColumnStretch(2,1)

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

        margins_layout.addWidget(x1_label,0,0)
        margins_layout.addWidget(x2_label,1,0)
        margins_layout.addWidget(y1_label,2,0)
        margins_layout.addWidget(y2_label,3,0)

        margins_layout.addWidget(x1_field,0,1)
        margins_layout.addWidget(x2_field,1,1)
        margins_layout.addWidget(y1_field,2,1)
        margins_layout.addWidget(y2_field,3,1)

        margins_layout.setColumnStretch(0,2)
        margins_layout.setColumnStretch(1,1)
        margins_layout.setColumnStretch(2,1)

        effect_left = QtGui.QGraphicsDropShadowEffect(traces_frame)
        effect_left.setOffset(0, 0)
        effect_left.setBlurRadius(2)
        effect_left.setColor(QtGui.QColor("#333333"))

        effect_right_top = QtGui.QGraphicsDropShadowEffect(traces_frame)
        effect_right_top.setOffset(0, 0)
        effect_right_top.setBlurRadius(2)
        effect_right_top.setColor(QtGui.QColor("#333333"))

        left_frame.setGraphicsEffect(effect_left)
        right_top_frame.setGraphicsEffect(effect_right_top)

        right_top_layout.addWidget(optional_label)
        right_top_layout.addWidget(self.createSpacer(4))
        right_top_layout.addLayout(dieelectric_layout)
        right_top_layout.addWidget(self.createSpacer(16))
        right_top_layout.addLayout(resistance_layout)
        right_top_layout.addWidget(self.createSpacer(2))
        right_top_layout.addLayout(resistivity_layout)
        right_top_layout.addWidget(self.createSpacer(4))
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
        traces_frame.setLayout(traces_layout)
        return traces_frame
    
    def createAnalysisSection(self):
        analysis_frame = QtGui.QFrame(self)

        effect = QtGui.QGraphicsDropShadowEffect(analysis_frame)
        effect.setOffset(0, 0)
        effect.setBlurRadius(2)
        effect.setColor(QtGui.QColor("#333333"))
        analysis_frame.setGraphicsEffect(effect)

        return analysis_frame

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

    def createControllerUnitTable(self):
        unit_table = CustomTableWidget()
        unit_table.setColumnCount(2)
        unit_table.setRowCount(3)

        unit_table.setHorizontalHeaderItem(0, self.createHeaderItem("Parameters"))
        unit_table.setHorizontalHeaderItem(1, self.createHeaderItem("Unit (p/l)"))

        unit_table.horizontalHeader().setProperty("headerType", "tableHeader")

        unit_table.setItem(0, 0, self.createTableWidgetItem("Cmin"))
        unit_table.setItem(0, 1, self.createTableWidgetItem("1"))
        unit_table.setItem(1, 0, self.createTableWidgetItem("Cmax"))
        unit_table.setItem(1, 1, self.createTableWidgetItem("2.5"))
        unit_table.setItem(2, 0, self.createTableWidgetItem("Sensitivity"))
        unit_table.setItem(2, 1, self.createTableWidgetItem("0.0851"))

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

        electrode_table.setHorizontalHeaderItem(0, self.createHeaderItem("Electrodes"))
        electrode_table.setHorizontalHeaderItem(1, self.createHeaderItem("Total"))
        electrode_table.setHorizontalHeaderItem(2, self.createHeaderItem("Active"))

        electrode_table.setItem(0,0, self.createTableWidgetItem("X Electrodes"))
        electrode_table.setItem(0,1, self.createTableWidgetItem("22"))
        electrode_table.setCellWidget(0,2, self.createElectrodeTableCombo())
        electrode_table.setItem(1,0, self.createTableWidgetItem("Y Electrodes"))
        electrode_table.setItem(1,1, self.createTableWidgetItem("30"))
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

    def createHeaderItem(self, text):
        item = QtGui.QTableWidgetItem(text)
        item.setFlags(QtCore.Qt.NoItemFlags)
        item.setFlags(item.flags() ^ QtCore.Qt.ItemIsEditable)
        item.setTextAlignment(QtCore.Qt.AlignCenter)

        return item

    def createTableWidgetItem(self, text):
        item = QtGui.QTableWidgetItem(text)
        item.setFlags(QtCore.Qt.NoItemFlags)
        item.setFlags(item.flags() ^ QtCore.Qt.ItemIsEditable)
        item.setForeground( QtGui.QColor.fromRgb(0,0,0) )
        item.setTextAlignment(QtCore.Qt.AlignCenter)

        return item

    def createCentralFrame(self):
        self._central_widget = QtGui.QStackedWidget()
        self._central_widget.addWidget(self.createSection(Window.Controller))
        self._central_widget.addWidget(self.createSection(Window.Sensor))
        self._central_widget.addWidget(self.createSection(Window.Pattern))
        self._central_widget.addWidget(self.createSection(Window.StackUp))
        self._central_widget.addWidget(self.createSection(Window.Traces))
        self._central_widget.addWidget(self.createSection(Window.Analysis))

        self._central_widget.setProperty("widgetType", "centralWidget")

        table = CustomTableWidget()

        table.setRowCount(7)
        table.setColumnCount(6)
        table.setHorizontalHeaderItem(0, self.createHeaderItem("Sensor"))
        table.setHorizontalHeaderItem(1, self.createHeaderItem("Controller"))
        table.setHorizontalHeaderItem(2, self.createHeaderItem("StackUp"))
        table.setHorizontalHeaderItem(3, self.createHeaderItem("Analysis"))
        table.setHorizontalHeaderItem(4, self.createHeaderItem("Traces"))
        table.setHorizontalHeaderItem(5, self.createHeaderItem("Pattern"))
        table.horizontalHeader().setProperty("headerType", "tableHeader")

        #add table items here
        for i in range(7):
            for j in range(6):
                table.setItem(i, j, self.createTableWidgetItem("Item " + str(i) + " " + str(j)))

        '''
        #add spanning widget to right-most element of first row
        table.setItem(0,2,table_item)

        #span Right-Most Item of First Row Here
        table.setSpan(0,2,table.rowCount(), 1)
        '''

        table.setShowGrid(False)
        table.verticalHeader().setVisible(False)
        table.resizeColumnsToContents()
        table.resizeRowsToContents()
        table.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)

        header = table.horizontalHeader()
        header.setResizeMode(1, QtGui.QHeaderView.Stretch)
        header.setResizeMode(2, QtGui.QHeaderView.Stretch)
        header.setResizeMode(3, QtGui.QHeaderView.Stretch)
        header.setResizeMode(4, QtGui.QHeaderView.Stretch)
        header.setResizeMode(5, QtGui.QHeaderView.Stretch)

        #header.setSectionResizeMode(QtGui.QHeaderView.Stretch)

        table.setHorizontalHeader(header)

        central_widget_layout = QtGui.QVBoxLayout()
        central_widget_layout.addWidget(self._central_widget)
        central_widget_layout.addWidget( self.createSimulationSummaryFrame() )
        central_widget_layout.setSpacing(0)
        central_widget_layout.setMargin(0)
        central_widget_layout.setContentsMargins(0,0,0,0)
        central_widget_layout.addWidget(table)

        central_frame = QtGui.QFrame()
        central_frame.setLayout(central_widget_layout)

        return central_frame

    def createSimulationSummaryFrame(self):
        simulation_summary_label = QtGui.QLabel("Simulation Summary")
        simulation_summary_label.setFrameStyle(QtGui.QFrame.NoFrame)
        simulation_summary_label.setProperty("labelType", "simulationSummaryLabel")

        simulation_summary_layout = QtGui.QHBoxLayout()
        simulation_summary_layout.addWidget(simulation_summary_label, 0, QtCore.Qt.AlignCenter)
        simulation_summary_layout.setContentsMargins(0,0,0,0)
        simulation_summary_layout.setMargin(0)
        simulation_summary_layout.setSpacing(0)

        simulation_summary_frame = QtGui.QFrame()
        simulation_summary_frame.setFixedHeight(30)
        simulation_summary_frame.setLayout(simulation_summary_layout)
        simulation_summary_frame.setProperty("frameType", "simulationSummaryFrame")

        return simulation_summary_frame

    def createIdentityButton(self, text):
        button = QtGui.QToolButton()
        button.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        button.setText(text)
        button.setIcon(QtGui.QIcon("./images/top_buttons/identity.svg"))
        button.setIconSize(QtCore.QSize(24, 24))
        button.setProperty("buttonType", "identityButton")
        button.setObjectName("identityButton")

        return button

    def createTopFrameButton(self, text, img):
        button = QtGui.QToolButton()
        button.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        button.setText(text)
        button.setProperty("buttonType", "topFrameButton")
        button.setObjectName(text+"Button")
        button.setIcon(QtGui.QIcon(img))
        button.setIconSize(QtCore.QSize(24, 24))
        button.setFixedHeight(65)

        return button

    def createTopFrame(self):
        logo_button = QtGui.QPushButton("")
        logo_button.setObjectName("logoButton")
        logo_button.setIcon( QtGui.QIcon(r'./images/logo.png'))
        logo_button.setIconSize( QtCore.QSize(175,75))
        logo_button.setProperty("buttonType", "topPanelButton")
        logo_button.setFixedWidth(175)
        logo_button.setFixedHeight(65)

        open_button = self.createTopFrameButton("Open", "./images/top_buttons/open.svg")
        save_button = self.createTopFrameButton("Save", "./images/top_buttons/save.svg")
        save_as_button = self.createTopFrameButton("Save As", "./images/top_buttons/save.svg")
        new_button = self.createTopFrameButton("New", "./images/top_buttons/new.svg")
        share_button = self.createTopFrameButton("Share", "./images/top_buttons/share.svg")
        preview_button = self.createBorderOnlyButton("Preview")
        preview_button.setFixedWidth(100)
        identity_button = self.createIdentityButton("Adam")

        top_layout = QtGui.QHBoxLayout()
        top_layout.addWidget(logo_button, 0, QtCore.Qt.AlignLeft)
        top_layout.addWidget(open_button, 0, QtCore.Qt.AlignLeft)
        top_layout.addWidget(save_button, 0, QtCore.Qt.AlignLeft)
        top_layout.addWidget(save_as_button, 0, QtCore.Qt.AlignLeft)
        top_layout.addWidget(new_button, 0, QtCore.Qt.AlignLeft)
        top_layout.addWidget(share_button, 0, QtCore.Qt.AlignLeft)
        top_layout.addWidget(preview_button, 0, QtCore.Qt.AlignLeft)
        top_layout.addWidget(identity_button, 1, QtCore.Qt.AlignRight)
        top_layout.setContentsMargins(0,0,0,0)
        top_layout.setSpacing(10)
        top_layout.addStretch(0)
        top_layout.setMargin(0)

        top_frame = QtGui.QFrame()
        top_frame.setLayout(top_layout)
        top_frame.setContentsMargins(0,0,0,0)
        top_frame.setProperty("frameType", "topFrame")

        top_frame.setFixedHeight(75)

        return top_frame

    def createSolveButton(self):
        button = QtGui.QToolButton()
        button.setText("Solve")
        button.setProperty("buttonType", "solveButton")
        button.setObjectName("solveButton")

        button.setFixedWidth(100)

        return button

    def createBorderOnlyButton(self, text):
        button = QtGui.QToolButton()
        button.setProperty("buttonType", "borderOnlyButton")
        button.setObjectName(text+"Button")
        button.setText(text)

        return button

    def createBottomLeftButton(self, text):
        button = QtGui.QToolButton()
        button.setProperty("buttonType", "bottomLeftButton")
        button.setObjectName(text+"Button")
        button.setText(text)

        return button

    def createLeftFrameButton(self, text, img, onclick_section, spaces = 4):
        spacePadding = ""
        for i in range(spaces):
            spacePadding += " "

        button = QtGui.QToolButton()
        button.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        button.setText(spacePadding+text)
        button.setProperty("buttonType", "leftFrameButton")
        button.setObjectName(text+"Button")
        button.setIcon(QtGui.QIcon(img))
        button.setIconSize(QtCore.QSize(24, 24))
        button.setCheckable(True)
        button.clicked.connect(lambda: self.changeSection(onclick_section))
        button.setFixedWidth(175)

        return button

    def createLeftFrame(self):
        controller_button = self.createLeftFrameButton("Controller", "./images/left_buttons/controller.svg", Window.Controller)
        sensor_button = self.createLeftFrameButton("Sensor", "./images/left_buttons/sensor.svg", Window.Sensor)
        pattern_button = self.createLeftFrameButton("Pattern", "./images/left_buttons/pattern.svg", Window.Pattern)
        stackup_button = self.createLeftFrameButton("StackUp", "./images/left_buttons/stackup.svg", Window.StackUp)
        traces_button = self.createLeftFrameButton("Traces", "./images/left_buttons/traces.svg", Window.Traces)
        analysis_button = self.createLeftFrameButton("Analysis", "./images/left_buttons/analysis.svg", Window.Analysis)
        solve_button = self.createSolveButton()
        solve_on_cloud_button = self.createBorderOnlyButton("Solve on Cloud")
        solve_on_cloud_button.setFixedWidth(150)

        or_label = QtGui.QLabel("or")
        or_label.setProperty("labelType", "orLabel")

        bottom_label = QtGui.QLabel("Licensed software developed by Fieldscale. All rights reserved 2017")
        bottom_label.setProperty("labelType", "bottomLabel")
        bottom_label.setWordWrap(True)
        bottom_label.setAlignment(QtCore.Qt.AlignHCenter)

        about_help_layout = QtGui.QHBoxLayout()
        about = self.createBottomLeftButton("About")
        help = self.createBottomLeftButton("Help")
        about_help_layout.addWidget(about)
        about_help_layout.addWidget(help)

        left_layout = QtGui.QVBoxLayout()
        left_layout.addWidget(controller_button, 0, QtCore.Qt.AlignTop)
        left_layout.addWidget(sensor_button, 0, QtCore.Qt.AlignTop)
        left_layout.addWidget(pattern_button, 0, QtCore.Qt.AlignTop)
        left_layout.addWidget(stackup_button, 0, QtCore.Qt.AlignTop)
        left_layout.addWidget(traces_button, 0, QtCore.Qt.AlignTop)
        left_layout.addWidget(analysis_button, 0, QtCore.Qt.AlignTop)
        left_layout.addWidget(solve_button, 1, QtCore.Qt.AlignBottom | QtCore.Qt.AlignHCenter)
        left_layout.addWidget(or_label, 0, QtCore.Qt.AlignBottom | QtCore.Qt.AlignHCenter)
        left_layout.addWidget(solve_on_cloud_button, 0, QtCore.Qt.AlignBottom | QtCore.Qt.AlignHCenter)
        left_layout.addWidget(bottom_label, 0, QtCore.Qt.AlignBottom | QtCore.Qt.AlignHCenter)
        left_layout.addLayout(about_help_layout)

        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(10)
        left_layout.addStretch(0)
        left_layout.setMargin(0)

        left_frame = QtGui.QFrame()
        left_frame.setLayout(left_layout)
        left_frame.setFixedWidth(175)
        left_frame.setContentsMargins(0, 0, 0, 0)
        left_frame.setProperty("frameType", "leftFrame")

        button_group = QtGui.QButtonGroup(left_frame)
        button_group.addButton(controller_button)
        button_group.addButton(sensor_button)
        button_group.addButton(pattern_button)
        button_group.addButton(stackup_button)
        button_group.addButton(traces_button)
        button_group.addButton(analysis_button)
        button_group.setExclusive(True)

        return left_frame

    def createSpacer(self, height = 8):
        spacer = QtGui.QLabel("")
        spacer.setFixedHeight(height)
        return spacer


if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    window = Window()
    qss_file = './style.qss'
    with open(qss_file, "r") as fh:
        window.setStyleSheet(fh.read())
    window.style().unpolish(window)
    window.style().polish(window)
    window.update()
    window.resize(QtGui.QApplication.desktop().size())
    window.show()
    sys.exit(app.exec_())

#gittest
