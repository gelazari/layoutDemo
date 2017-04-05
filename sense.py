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

    Sensor, Controller = range(2)

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

        layout = SenseLayout()
        layout.setSpacing(0)
        layout.addWidget( top_widget, SenseLayout.Top )
        layout.addWidget( left_widget, SenseLayout.Left)
        layout.addWidget( central_widget, SenseLayout.Middle )

        self.setLayout(layout)
        self.setWindowTitle("Sense Demo")

    @QtCore.pyqtSlot(int, name='changeSection')
    def changeSection(self, section):
        if section == Window.Sensor:
            self._central_widget.setCurrentIndex(section)
        if section == Window.Controller:
            self._central_widget.setCurrentIndex(section)

    @QtCore.pyqtSlot(name="newController")
    def newControllerPressed(self):
        dialog = self.createNewControllerDialog()
        dialog.exec_();

    def createLabel(self, text):
        label = QtGui.QLabel(text)
        label.setFrameStyle(QtGui.QFrame.Box | QtGui.QFrame.Raised)
        return label

    def createSection(self, section):
        if section == Window.Sensor:
            return self.createSensorSection()
        elif section == Window.Controller:
            return self.createControllerSection()

    def createSensorSection(self):
        sensor_label = QtGui.QLabel("Sensor Section")

        sensor_button = QtGui.QPushButton("Sensor Button")

        sensor_layout = QtGui.QHBoxLayout(self)
        sensor_layout.addWidget(sensor_label, 0, QtCore.Qt.AlignCenter)
        sensor_layout.addWidget(sensor_button, 0 , QtCore.Qt.AlignCenter)

        sensor_frame = QtGui.QFrame(self)
        sensor_frame.setLayout(sensor_layout)
        sensor_frame.setStyleSheet("QFrame { background-color: yellow }")

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
        controller_frame.setStyleSheet("QFrame { background-color: #ededed;}")
        self.createNewControllerDialog()
        return controller_frame

    def createNewControllerDialog(self):
        dialog = QtGui.QDialog()
        form_layout = QtGui.QFormLayout()

        pf_label1 = QtGui.QLabel("pF")
        pf_label2 = QtGui.QLabel("pF")
        pf_label3 = QtGui.QLabel("pF")

        company_line = QtGui.QLineEdit()
        product_line = QtGui.QLineEdit()

        cmin_line = QtGui.QHBoxLayout()
        cmin_line.addWidget(QtGui.QLineEdit())
        cmin_line.addWidget(pf_label1)

        cmax_line = QtGui.QHBoxLayout()
        cmax_line.addWidget(QtGui.QLineEdit())
        cmax_line.addWidget(pf_label2)

        sensitivity_line = QtGui.QHBoxLayout()
        sensitivity_line.addWidget(QtGui.QLineEdit())
        sensitivity_line.addWidget(pf_label3)

        bits_of_adc_spinner = QtGui.QSpinBox()
        x_electrodes_spinner = QtGui.QSpinBox()
        y_electrodes_spinner = QtGui.QSpinBox()

        form_layout.addRow("Company", company_line)
        form_layout.addRow("Product", product_line)
        form_layout.addRow("Cmin", cmin_line)
        form_layout.addRow("Cmax", cmax_line)
        form_layout.addRow("Sensitivity", sensitivity_line)
        form_layout.addRow("Bits of ADC", bits_of_adc_spinner)
        form_layout.addRow("X Electrodes", x_electrodes_spinner)
        form_layout.addRow("Y Electrodes", y_electrodes_spinner)

        dialog.setLayout(form_layout)
        dialog.setWindowTitle("New Controller")

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
        self._central_widget.addWidget(self.createSection(Window.Sensor))
        self._central_widget.addWidget(self.createSection(Window.Controller))
        self._central_widget.setProperty("widgetType", "centralWidget")

        table = CustomTableWidget()
        table_item = QtGui.QTableWidgetItem()

        table.setRowCount(5)
        table.setColumnCount(6)
        table.setSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum )
        table.setHorizontalHeaderItem(0, self.createHeaderItem("Sensor"))
        table.setHorizontalHeaderItem(1, self.createHeaderItem("Controller"))
        table.setHorizontalHeaderItem(2, self.createHeaderItem("StackUp"))
        table.setHorizontalHeaderItem(3, self.createHeaderItem("Analysis"))
        table.setHorizontalHeaderItem(4, self.createHeaderItem("Traces"))
        table.setHorizontalHeaderItem(5, self.createHeaderItem("Pattern"))
        table.horizontalHeader().setProperty("headerType", "tableHeader")

        #add table items here
        table.setItem(0, 0, self.createTableWidgetItem("Item 1.1"))
        table.setItem(0, 1, self.createTableWidgetItem("Item 1.2"))
        table.setItem(1, 0, self.createTableWidgetItem("Item 2.1"))
        table.setItem(1, 1, self.createTableWidgetItem("Item 2.2"))
        table.setItem(2, 0, self.createTableWidgetItem("Item 3.1"))
        table.setItem(2, 1, self.createTableWidgetItem("Item 3.2"))
        table.setItem(3, 0, self.createTableWidgetItem("Item 4.1"))
        table.setItem(3, 1, self.createTableWidgetItem("Item 4.2"))

        #add spanning widget to right-most element of first row
        table.setItem(0,2,table_item)

        #span Right-Most Item of First Row Here
        table.setSpan(0,2,table.rowCount(), 1)
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

        simulation_summary_frame = QtGui.QFrame()
        simulation_summary_frame.setLayout(simulation_summary_layout)
        simulation_summary_frame.setProperty("frameType", "simulationSummaryFrame")

        return simulation_summary_frame

    def createTopFrame(self):
        open_button = QtGui.QPushButton("Open")
        open_button.setObjectName("openButton")
        open_button.setIcon( QtGui.QIcon(r'/Users/G_Laza/Desktop/mushroom.ico'))
        open_button.setIconSize( QtCore.QSize(56,56))
        open_button.setProperty("buttonType", "topPanelButton")
        open_button.setFixedWidth(175)
        open_button.setFixedHeight(150)

        save_button = QtGui.QPushButton("Save")
        save_button.setObjectName("saveButton")
        save_button.setIcon( QtGui.QIcon(r'/Users/G_Laza/Desktop/mushroom.ico'))
        save_button.setIconSize( QtCore.QSize(56,56))
        #save_button.setFixedWidth(200)

        top_layout = QtGui.QHBoxLayout()
        top_layout.addWidget(open_button, 0, QtCore.Qt.AlignLeft)
        top_layout.addWidget(save_button, 0, QtCore.Qt.AlignLeft)
        top_layout.setContentsMargins(0,0,0,0)
        top_layout.setSpacing(10)
        top_layout.addStretch(0)
        top_layout.setMargin(0)

        top_frame = QtGui.QFrame()
        top_frame.setLayout(top_layout)
        top_frame.setContentsMargins(0,0,0,0)
        top_frame.setProperty("frameType", "topFrame")

        top_frame.setFixedHeight(100)

        return top_frame

    def createLeftFrame(self):
        controller_button = QtGui.QPushButton("Controller")
        controller_button.setProperty("buttonType", "leftFrameButton")
        controller_button.setObjectName("controllerButton")
        controller_button.setIcon(QtGui.QIcon(r'/Users/G_Laza/Desktop/mushroom.ico'))
        controller_button.setIconSize(QtCore.QSize(56, 56))
        controller_button.setCheckable(True)
       # controller_button.clicked().connect(self.sectionChanged(0))
        controller_button.clicked.connect(lambda: self.changeSection(Window.Controller))
        # controller_button.setFixedWidth(200)

        sensor_button = QtGui.QPushButton("Sensor")
        sensor_button.setProperty("buttonType", "leftFrameButton")
        sensor_button.setObjectName("sensorButton")
        sensor_button.setIcon(QtGui.QIcon(r'/Users/G_Laza/Desktop/mushroom.ico'))
        sensor_button.setIconSize(QtCore.QSize(56, 56))
        sensor_button.setCheckable(True)
        sensor_button.clicked.connect(lambda: self.changeSection(Window.Sensor))
        # sensor_button.setFixedWidth(200)

        analysis_button = QtGui.QPushButton("Analysis")
        analysis_button.setProperty("buttonType", "leftFrameButton")
        analysis_button.setObjectName("analysisButton")
        analysis_button.setIcon(QtGui.QIcon(r'/Users/G_Laza/Desktop/mushroom.ico'))
        analysis_button.setCheckable(True)
        analysis_button.setIconSize(QtCore.QSize(56, 56))
        # analysis_button.setFixedWidth(200)

        stackup_button = QtGui.QPushButton("StackUp")
        stackup_button.setProperty("buttonType", "leftFrameButton")
        stackup_button.setObjectName("stackupButton")
        stackup_button.setIcon(QtGui.QIcon(r'/Users/G_Laza/Desktop/mushroom.ico'))
        stackup_button.setCheckable(True)
        stackup_button.setIconSize(QtCore.QSize(56, 56))
        # stackup_button.setFixedWidth(200)

        left_layout = QtGui.QVBoxLayout()
        left_layout.addWidget(controller_button, 0, QtCore.Qt.AlignTop)
        left_layout.addWidget(sensor_button, 0, QtCore.Qt.AlignTop)
        left_layout.addWidget(analysis_button, 0, QtCore.Qt.AlignTop)
        left_layout.addWidget(stackup_button, 0, QtCore.Qt.AlignTop)
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
        button_group.addButton(analysis_button)
        button_group.addButton(stackup_button)
        button_group.setExclusive(True)

        return left_frame

class CustomTableWidget(QtGui.QTableWidget):
    def __init__(self):
        super(CustomTableWidget, self).__init__()

    def selectRow(self, p_int):
       #do nothing
       return

    def editItem(self, QTableWidgetItem):
        # do nothing
        return

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

    #Left color: 17202b