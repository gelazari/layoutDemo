from widget_util import *

from custom_tableWidget import CustomTableWidget
from controller_section import ControllerSection
from stackup_section import StackUpSection
from traces_section import TracesSection
from sensor_section import SensorSection
from analysis_section import AnalysisSection
from pattern_section import PatternSection
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
            return SensorSection(self)
        elif section == Window.Controller:
            return ControllerSection(self)
        elif section == Window.StackUp:
            return StackUpSection(self)
        elif section == Window.Pattern:
            return PatternSection(self)
        elif section == Window.Traces:
            return TracesSection(self)
        elif section == Window.Analysis:
            return AnalysisSection(self)

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
        table.setHorizontalHeaderItem(0, createHeaderItem("Sensor"))
        table.setHorizontalHeaderItem(1, createHeaderItem("Controller"))
        table.setHorizontalHeaderItem(2, createHeaderItem("StackUp"))
        table.setHorizontalHeaderItem(3, createHeaderItem("Analysis"))
        table.setHorizontalHeaderItem(4, createHeaderItem("Traces"))
        table.setHorizontalHeaderItem(5, createHeaderItem("Pattern"))
        table.horizontalHeader().setProperty("headerType", "tableHeader")
        table.setSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)

        #add table items here
        for i in range(7):
            for j in range(6):
                table.setItem(i, j, createTableWidgetItem("Item " + str(i) + " " + str(j)))

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
