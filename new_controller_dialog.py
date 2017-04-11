from PyQt4 import QtCore, QtGui
from custom_lineEdit import CustomLineEdit

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
