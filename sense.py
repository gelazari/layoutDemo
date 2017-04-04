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
                    rect.width() - westWidth, centerHeight))

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


class Window(QtGui.QMainWindow):

    Sensor, Controller = range(2)

    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        layout = SenseLayout(self)
        layout.addWidget( self.createCentralFrame(), SenseLayout.Middle)

        # Because SenseLayout doesn't call its super-class addWidget() it
        # doesn't take ownership of the widgets until setLayout() is called.
        # Therefore we keep a local reference to each label to prevent it being
        # garbage collected too soon.

        #label_n = self.createLabel("North")
        #layout.addWidget(label_n, SenseLayout.Top)
        #
        #label_w = self.createLabel("West")
        #layout.addWidget(label_w, SenseLayout.Left)
        #
        # label_s = self.createLabel("South")
        # layout.addWidget(label_s, SenseLayout.Bottom)

        central_widget = QtGui.QWidget()
        central_widget.setLayout(layout)

        self.setCentralWidget(central_widget)

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
        #header.setSectionResizeMode(QtGui.QHeaderView.Stretch)

        table.setHorizontalHeader(header)

        central_widget_layout = QtGui.QHBoxLayout()
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
    window.resize(QtGui.QApplication.desktop().size())
    window.show()
    sys.exit(app.exec_())   