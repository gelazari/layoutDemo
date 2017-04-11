from PyQt4 import QtCore, QtGui

class ItemWrapper(object):
    def __init__(self, i, p):
        self.item = i
        self.position = p


class SenseLayout(QtGui.QLayout):
    Left, Top, Bottom, Middle = range(4)
    MinimumSize, SizeHint = range(2)

    def __init__(self, parent=None, margin=0, spacing=-1):
        super(SenseLayout, self).__init__(parent)

        self.setMargin(margin)
        self.setSpacing(spacing)
        self.list = []

    def __del__(self):
        l = self.takeAt(0)
        while l:
            l = self.takeAt(0)

    def addItem(self, item):
        self.add(item, SenseLayout.West)

    def addWidget(self, widget, position):
        self.add(QtGui.QWidgetItem(widget), position)

    def expandingDirections(self):
        return QtCore.Qt.Horizontal | QtCore.Qt.Vertical

    def hasHeightForWidth(self):
        return False

    def count(self):
        return len(self.list)

    def itemAt(self, index):
        if index < len(self.list):
            return self.list[index].item

        return None

    def minimumSize(self):
        return self.calculateSize(SenseLayout.MinimumSize)

    def setGeometry(self, rect):
        center = None
        eastWidth = 0
        westWidth = 0
        northHeight = 0
        southHeight = 0
        centerHeight = 0

        super(SenseLayout, self).setGeometry(rect)

        for wrapper in self.list:
            item = wrapper.item
            position = wrapper.position

            if position == SenseLayout.Top:
                item.setGeometry(QtCore.QRect(rect.x(), northHeight,
                        rect.width(), item.sizeHint().height()))

                northHeight += item.geometry().height() + self.spacing()

            elif position == SenseLayout.Bottom:
                item.setGeometry(QtCore.QRect(item.geometry().x(),
                        item.geometry().y(), rect.width(),
                        item.sizeHint().height()))

                southHeight += item.geometry().height() + self.spacing()

                item.setGeometry(QtCore.QRect(rect.x(),
                        rect.y() + rect.height() - southHeight + self.spacing(),
                        item.geometry().width(), item.geometry().height()))

            elif position == SenseLayout.Middle:
                center = wrapper

        centerHeight = rect.height() - northHeight - southHeight

        for wrapper in self.list:
            item = wrapper.item
            position = wrapper.position

            if position == SenseLayout.Left:
                item.setGeometry(QtCore.QRect(rect.x() + westWidth,
                        northHeight, item.sizeHint().width(), centerHeight))

                westWidth += item.geometry().width() + self.spacing()

        if center:
            center.item.setGeometry(QtCore.QRect(westWidth, northHeight,
                    rect.width() - eastWidth - westWidth, centerHeight))

    def sizeHint(self):
        return self.calculateSize(SenseLayout.SizeHint)

    def takeAt(self, index):
        if index >= 0 and index < len(self.list):
            layoutStruct = self.list.pop(index)
            return layoutStruct.item

        return None

    def add(self, item, position):
        self.list.append(ItemWrapper(item, position))

    def calculateSize(self, sizeType):
        totalSize = QtCore.QSize()

        for wrapper in self.list:
            position = wrapper.position
            itemSize = QtCore.QSize()

            if sizeType == SenseLayout.MinimumSize:
                itemSize = wrapper.item.minimumSize()
            else: # sizeType == SenseLayout.SizeHint
                itemSize = wrapper.item.sizeHint()

            if position in (SenseLayout.Top, SenseLayout.Bottom, SenseLayout.Middle):
                totalSize.setHeight(totalSize.height() + itemSize.height())

            if position in (SenseLayout.Left, SenseLayout.Middle):
                totalSize.setWidth(totalSize.width() + itemSize.width())

        return totalSize


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
            test_frame = QtGui.QFrame(stackup_frame)
            test_layout = QtGui.QGridLayout(test_frame)
            test_layout.setContentsMargins(0,0,0,0)

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

            test_layout.setColumnStretch(0, 1)
            test_layout.setColumnStretch(1, 1)
            test_layout.setColumnStretch(2, 1)
            test_layout.setColumnStretch(3, 1)
            test_layout.setColumnStretch(4, 1)

            test_layout.addWidget(layer_label, 0, 0)
            test_layout.addWidget(material, 0, 1)
            test_layout.addWidget(rel_perm, 0, 2)
            test_layout.addWidget(thickness, 0, 3)
            test_layout.addWidget(grounded, 0, 4, QtCore.Qt.AlignCenter)

            test_frame.setProperty("frameType", "layerRowFrame")
            right_frame.addWidget(test_frame)

            self.layer_list.append(test_frame)

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

        effect = QtGui.QGraphicsDropShadowEffect(traces_frame)
        effect.setOffset(0, 0)
        effect.setBlurRadius(2)
        effect.setColor(QtGui.QColor("#333333"))
        traces_frame.setGraphicsEffect(effect)

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

        table.setShowGrid(False)
        table.verticalHeader().setVisible(False)
        table.resizeColumnsToContents()
        table.resizeRowsToContents()
        table.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        table.setSizePolicy(QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Minimum)

        header = table.horizontalHeader()
        header.setResizeMode(1, QtGui.QHeaderView.Stretch)
        header.setResizeMode(2, QtGui.QHeaderView.Stretch)
        header.setResizeMode(3, QtGui.QHeaderView.Stretch)
        header.setResizeMode(4, QtGui.QHeaderView.Stretch)
        header.setResizeMode(5, QtGui.QHeaderView.Stretch)

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

class NewControllerDialog(QtGui.QDialog):
    Sensitivity, Bits_of_adc = range(2)

    def __init__(self, title, parent=None):
        super(NewControllerDialog, self).__init__(parent)

        top_frame = self.createTopFrame()
        bot_frame = self.createBotFrame()

        top_level_layout = QtGui.QVBoxLayout()
        top_level_layout.setSpacing(0)
        top_level_layout.setMargin(0)

        top_level_layout.addWidget(top_frame)
        top_level_layout.addWidget(bot_frame)

        self.setWindowTitle(title)
        self.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.setLayout(top_level_layout)

    def createTopFrame(self):

        top_frame = QtGui.QFrame(self)
        top_frame_layout = QtGui.QVBoxLayout()
        top_frame.setFixedHeight(200)

        img = QtGui.QLabel()
        img.setPixmap(QtGui.QPixmap("./images/new_controller.png"))

        nc_bold_label = QtGui.QLabel("New Controller")
        nc_bold_label.setProperty("labelType","newControllerLabel")

        info_label = QtGui.QLabel("Insert your specs. You will be able to edit or delete your controller once created.")
        info_label.setAlignment(QtCore.Qt.AlignCenter)
        info_label.setProperty("labelType", "newControllerInfoLabel")
        info_label.setWordWrap(True)

        top_frame_layout.addWidget(img, 0, QtCore.Qt.AlignTop | QtCore.Qt.AlignHCenter)
        top_frame_layout.addWidget(nc_bold_label, 0, QtCore.Qt.AlignTop | QtCore.Qt.AlignHCenter)
        top_frame_layout.addWidget(info_label, 0, QtCore.Qt.AlignTop | QtCore.Qt.AlignHCenter)
        top_frame.setLayout(top_frame_layout)

        top_frame.setStyleSheet("background-color: #ededed;")

        return top_frame

    def createBotFrame(self):
        bot_frame = QtGui.QFrame(self)
        bot_frame.setStyleSheet("background-color: #ffffff;")

        bot_frame_layout = QtGui.QHBoxLayout()

        self.general_label = QtGui.QLabel("GENERAL")
        self.empty_label = QtGui.QLabel(" ")
        self.company_label = QtGui.QLabel("Company")
        self.product_label = QtGui.QLabel("Product")

        self.technical_label = QtGui.QLabel("TECHNICAL")
        self.cmin_label = QtGui.QLabel("C min")
        self.cmax_label = QtGui.QLabel("C max ")

        self.electrodes_label = QtGui.QLabel("ELECTRODES")
        self.x_electrodes_label = QtGui.QLabel("x Electrodes")
        self.y_electrodes_label = QtGui.QLabel("y Electrodes")

        self.sensitivity_label = QtGui.QLabel("Sensitivity")
        self.bits_of_adc_label = QtGui.QLabel("Bits of ADC")

        self.company_label.setProperty("labelType", "fieldLabel")
        self.product_label.setProperty("labelType", "fieldLabel")
        self.cmin_label.setProperty("labelType", "fieldLabel")
        self.cmax_label.setProperty("labelType", "fieldLabel")
        self.x_electrodes_label.setProperty("labelType", "fieldLabel")
        self.y_electrodes_label.setProperty("labelType", "fieldLabel")
        self.sensitivity_label.setProperty("labelType", "fieldLabel")
        self.bits_of_adc_label.setProperty("labelType", "fieldLabel")

        self.general_label.setProperty("labelType", "sectionLabel")
        self.technical_label.setProperty("labelType", "sectionLabel")
        self.electrodes_label.setProperty("labelType", "sectionLabel")
        self.empty_label.setProperty("labelType", "sectionLabel")

        self.cmin_pf_label = QtGui.QLabel("pF")
        self.cmax_pf_label = QtGui.QLabel("pF")
        self.sensitivity_pf_label = QtGui.QLabel("pF")
        self.cmin_pf_label.setProperty("labelType", "pfLabel")
        self.cmax_pf_label.setProperty("labelType", "pfLabel")
        self.sensitivity_pf_label.setProperty("labelType", "pfLabel")

        self.sensitivity_border_label = QtGui.QLabel()
        self.sensitivity_border_label.setProperty("labelType", "ncBorderLabel")
        self.sensitivity_border_label.setFixedHeight(8)

        self.bits_of_adc_border_label = QtGui.QLabel()
        self.bits_of_adc_border_label.setProperty("labelType", "ncBorderLabel")
        self.bits_of_adc_border_label.setFixedHeight(8)

        self.company_field = CustomLineEdit()
        self.product_field = CustomLineEdit()
        self.cmin_field = CustomLineEdit()
        self.cmax_field = CustomLineEdit()
        self.x_electrodes_field = CustomLineEdit()
        self.y_electrodes_field = CustomLineEdit()
        self.sensitivity_field = CustomLineEdit(field = NewControllerDialog.Sensitivity)
        self.bits_of_adc_field = CustomLineEdit(field = NewControllerDialog.Bits_of_adc)

        self.company_field.setFixedHeight(24)
        self.product_field.setFixedHeight(24)
        self.cmin_field.setFixedHeight(24)
        self.cmax_field.setFixedHeight(24)
        self.x_electrodes_field.setFixedHeight(24)
        self.y_electrodes_field.setFixedHeight(24)
        self.sensitivity_field.setFixedHeight(24)
        self.bits_of_adc_field.setFixedHeight(24)

        cmin_layout = QtGui.QHBoxLayout()
        cmax_layout = QtGui.QHBoxLayout()
        sensitivity_layout = QtGui.QHBoxLayout()

        cmin_layout.addWidget(self.cmin_field)
        cmin_layout.addWidget(self.cmin_pf_label)
        cmax_layout.addWidget(self.cmax_field)
        cmax_layout.addWidget(self.cmax_pf_label)
        sensitivity_layout.addWidget(self.sensitivity_field)
        sensitivity_layout.addWidget(self.sensitivity_pf_label)

        left_row = QtGui.QFormLayout()
        right_row = QtGui.QFormLayout()

        left_row.setSpacing(12)
        right_row.setSpacing(12)

        left_row.addRow(self.general_label)
        left_row.addRow(self.company_label, self.company_field)
        left_row.addRow(self.technical_label)
        left_row.addRow(self.cmin_label, cmin_layout)
        left_row.addRow(self.cmax_label, cmax_layout)
        left_row.addRow(self.sensitivity_border_label)
        left_row.addRow(self.sensitivity_label, sensitivity_layout)

        right_row.addRow(self.empty_label)
        right_row.addRow(self.product_label, self.product_field)
        right_row.addRow(self.electrodes_label)
        right_row.addRow(self.x_electrodes_label, self.x_electrodes_field)
        right_row.addRow(self.y_electrodes_label, self.y_electrodes_field)
        right_row.addRow(self.bits_of_adc_border_label)
        right_row.addRow(self.bits_of_adc_label, self.bits_of_adc_field)

        bot_frame_layout.addLayout(left_row, 2)
        bot_frame_layout.addLayout(right_row, 2)
        bot_frame.setLayout(bot_frame_layout)

        return bot_frame

    def setBottomFieldVisibility(self, item):
        if item == NewControllerDialog.Sensitivity:
            self.bits_of_adc_border_label.setStyleSheet("border: 4px solid #ededed");
            self.bits_of_adc_label.setStyleSheet("color: #dcdcdc;")
            self.bits_of_adc_field.setStyleSheet("color: #dcdcdc;")

            self.sensitivity_pf_label.setStyleSheet("color: black;")
            self.sensitivity_label.setStyleSheet("color: black;")
            self.sensitivity_border_label.setStyleSheet("border: 4px solid #6533AC")
            self.sensitivity_field.setStyleSheet("color: blackl")

        elif item == NewControllerDialog.Bits_of_adc:
            self.sensitivity_border_label.setStyleSheet("border: 4px solid #ededed");
            self.sensitivity_label.setStyleSheet("color: #dcdcdc;")
            self.sensitivity_pf_label.setStyleSheet("color: #dcdcdc");
            self.sensitivity_field.setStyleSheet("color: #dcdcdc;")

            self.bits_of_adc_label.setStyleSheet("color: black;")
            self.bits_of_adc_field.setStyleSheet("color: black;")
            self.bits_of_adc_border_label.setStyleSheet("border: 4px solid #6533AC")

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

class CustomComboBox(QtGui.QComboBox):
    def __init__(self, parent=None):
        super(CustomComboBox, self).__init__(parent)
        self.setProperty("fieldType", "comboBox")

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
