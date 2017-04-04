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

    def __init__(self, parent=None):
        super(Window, self).__init__()


        central_widget = self.createCentralFrame()
        top_widget = self.createTopFrame()
        left_widget = self.createLeftFrame()

        layout = SenseLayout()
        layout.addWidget( top_widget, SenseLayout.Top )
        layout.addWidget( left_widget, SenseLayout.Left)
        layout.addWidget( central_widget, SenseLayout.Middle )

        # Because SenseLayout doesn't call its super-class addWidget() it
        # doesn't take ownership of the widgets until setLayout() is called.
        # Therefore we keep a local reference to each label to prevent it being
        # garbage collected too soon.

        self.setLayout(layout)

        self.setWindowTitle("Sense Demo")

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
        controller_label = QtGui.QLabel("Controller Section")

        controller_button_first = QtGui.QPushButton("Controller button 1")
        controller_button_second = QtGui.QPushButton("Controller button 2")

        controller_layout = QtGui.QVBoxLayout(self)
        controller_layout.addWidget(controller_label, 0, QtCore.Qt.AlignCenter)
        controller_layout.addWidget(controller_button_first, 0, QtCore.Qt.AlignCenter)
        controller_layout.addWidget(controller_button_second, 0, QtCore.Qt.AlignCenter)

        sub_controller_frame = QtGui.QFrame(self)
        sub_controller_frame.setLayout(controller_layout)
        sub_controller_frame.setFixedWidth(200)
        sub_controller_frame.setStyleSheet("QFrame { background-color: green }")

        controller_section_layout = QtGui.QHBoxLayout(self)
        controller_section_layout.addWidget(sub_controller_frame)

        controller_frame = QtGui.QFrame(self)
        controller_frame.setFixedWidth(150)
        controller_frame.setLayout(controller_section_layout)
        controller_frame.setStyleSheet("QFrame { background-color: grey }")

        return controller_frame

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
        item.setTextAlignment(QtCore.Qt.AlignLeft)

        return item

    def createCentralFrame(self):
        central_widget = QtGui.QStackedWidget()
        central_widget.addWidget(self.createSection(Window.Sensor))
        central_widget.addWidget(self.createSection(Window.Controller))

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

        header = table.horizontalHeader()
        header.setResizeMode(1, QtGui.QHeaderView.Stretch)
        header.setResizeMode(2, QtGui.QHeaderView.Stretch)
        header.setResizeMode(3, QtGui.QHeaderView.Stretch)
        header.setResizeMode(4, QtGui.QHeaderView.Stretch)
        header.setResizeMode(5, QtGui.QHeaderView.Stretch)

        #header.setSectionResizeMode(QtGui.QHeaderView.Stretch)

        table.setHorizontalHeader(header)

        central_widget_layout = QtGui.QVBoxLayout()
        central_widget_layout.addWidget(central_widget)
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
        simulation_summary_label.setProperty("frameType", 'simulationSummaryLabel')

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
        #open_button.setFixedWidth(200)

        save_button = QtGui.QPushButton("Save")
        save_button.setObjectName("saveButton")
        save_button.setIcon( QtGui.QIcon(r'/Users/G_Laza/Desktop/mushroom.ico'))
        save_button.setIconSize( QtCore.QSize(56,56))
        #save_button.setFixedWidth(200)

        top_layout = QtGui.QHBoxLayout()
        top_layout.addWidget(open_button, 0 , QtCore.Qt.AlignLeft)
        top_layout.addWidget(save_button, 0 , QtCore.Qt.AlignLeft)
        top_layout.setContentsMargins(0,0,0,0)
        top_layout.setSpacing(10)
        top_layout.addStretch(0)
        top_layout.setMargin(0)

        top_frame = QtGui.QFrame()
        top_frame.setLayout(top_layout)
        top_frame.setContentsMargins(0,0,0,0)

        return top_frame

    def createLeftFrame(self):
        controller_button = QtGui.QPushButton("Controller")
        controller_button.setObjectName("controllerButton")
        controller_button.setIcon(QtGui.QIcon(r'/Users/G_Laza/Desktop/mushroom.ico'))
        controller_button.setIconSize(QtCore.QSize(56, 56))
        # controller_button.setFixedWidth(200)

        sensor_button = QtGui.QPushButton("Sensor")
        sensor_button.setObjectName("sensorButton")
        sensor_button.setIcon(QtGui.QIcon(r'/Users/G_Laza/Desktop/mushroom.ico'))
        sensor_button.setIconSize(QtCore.QSize(56, 56))
        # sensor_button.setFixedWidth(200)

        analysis_button = QtGui.QPushButton("Analysis")
        analysis_button.setObjectName("analysisButton")
        analysis_button.setIcon(QtGui.QIcon(r'/Users/G_Laza/Desktop/mushroom.ico'))
        analysis_button.setIconSize(QtCore.QSize(56, 56))
        # analysis_button.setFixedWidth(200)

        stackup_button = QtGui.QPushButton("StackUp")
        stackup_button.setObjectName("stackupButton")
        stackup_button.setIcon(QtGui.QIcon(r'/Users/G_Laza/Desktop/mushroom.ico'))
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
        left_frame.setFixedWidth(200)
        left_frame.setContentsMargins(0, 0, 0, 0)

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
        print(fh.read())
        window.setStyleSheet(fh.read())
    window.resize(QtGui.QApplication.desktop().size())
    window.show()
    sys.exit(app.exec_())   