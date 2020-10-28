#!/home/oscar/anaconda3/bin/python
#ksajfsakdfb
# -*- coding: utf-8 -*-
""" 
GUI to preprocess raw data directly from TEM equipment.

It shows a time series and allows you to select points, either one by one or by a time window, and removes the selected points

Developed by: Oscar Castro-Artola. April, 2020. E-Mail:oscar.castro@unicach.mx"
"""
#from PyQt5.QtGui import *
from PyQt5.QtWidgets import QDialog,QApplication
from PyQt5.QtWidgets import QPushButton,QVBoxLayout
from PyQt5.QtWidgets import QGroupBox,QFileDialog
from PyQt5.QtWidgets import QLabel,QGridLayout
from PyQt5.QtWidgets import QLineEdit,QCheckBox
from PyQt5.QtWidgets import QWidget,QButtonGroup
from funcs_gui_MT_preproc import plot_file, get_info_labels
from funcs_gui_MT_preproc import clean_survey, write_data_all_datafile
import matplotlib.pyplot as plt

class MainWindow(QDialog):
    # MAIN FUNCTION
    def __init__(self):
        super(MainWindow, self).__init__()
        self.resize(300,100)
        self.setWindowTitle(self.tr("GUI"))
        self.grid = QGridLayout()
        self.setLayout(self.grid)
         # Exit button
        self.bot_exit = QPushButton("Exit",self)
        self.bot_exit.setFixedWidth(80)
        self.bot_close_all = QPushButton("Close all figures")
        # Title
#        self.title = QLabel("<h3>GUI to process invert and plot TEM data<\h3>",self)
        self.title = QLabel("<h3>GUI to invert 1D TEM data<\h3>",self)

        # Group 01: Select file to plot data
        self.group_01 = QGroupBox("-- 1. Config and select data --", self)
        self.vbox_01 = QGridLayout()
        self.coil_len = QLineEdit()
        self.coil_lab = QLabel("Tx-Rx length [m]") 
        self.ramp_len = QLineEdit()
        self.ramp_len.setFixedWidth(100)
        self.coil_len.setFixedWidth(100)
        self.ramp_lab = QLabel("Ramp time [s]") 
        self.bot_get_data_file = QPushButton("Select files")
        self.bot_get_data_file.setDisabled(False)
        self.vbox_01.addWidget(self.coil_len,1,1)
        self.vbox_01.addWidget(self.coil_lab,1,2)
        self.vbox_01.addWidget(self.ramp_len,2,1)
        self.vbox_01.addWidget(self.ramp_lab,2,2)
        self.vbox_01.addWidget(self.bot_get_data_file,6,1,1,2)
        self.bot_get_data_file.clicked.connect(self.select_file)
        self.group_01.setLayout(self.vbox_01)

        # Group 02: Show information from the file
        self.group_02 = QGroupBox("-- File information --", self)
        self.vbox_02 = QVBoxLayout()
        self.inf_01 = QLabel() # File name
        self.inf_01.setFixedWidth(200)
        self.inf_01.setStyleSheet('color: navy')
        self.inf_01.setText("Filename: ")
        self.inf_02 = QLabel() # Number of surveys
        self.inf_02.setStyleSheet('color: navy')
        self.inf_02.setText("Number of surveys: ")
        self.inf_03 = QLabel() # Survey to write
        self.inf_03.setStyleSheet('color: navy')
        self.inf_03.setText("Survey to write: ")
        self.inf_04 = QLabel() # Noise survey exist?
        self.inf_04.setStyleSheet('color: navy')
        self.inf_04.setText("Noise file: ")
        self.inf_05 = QLabel() # Data file
        self.inf_05.setStyleSheet('color: red')
        self.inf_05.setText("Data file status: Not written ")
        self.inf_06 = QLabel() # Data file
        self.inf_06.setStyleSheet('color: red')
        self.inf_06.setText("Inversion method: Not set")
        self.inf_07 = QLabel() # Data file
        self.inf_07.setStyleSheet('color: red')
        self.inf_07.setText("Inversion parameters: Not set")
        self.vbox_02.addWidget(self.inf_01)
        self.vbox_02.addWidget(self.inf_02)
        self.vbox_02.addWidget(self.inf_04)
        self.vbox_02.addWidget(self.inf_03)
        self.vbox_02.addWidget(self.inf_05)
        self.vbox_02.addWidget(self.inf_06)
        self.vbox_02.addWidget(self.inf_07)
        self.group_02.setLayout(self.vbox_02)

        # Group 03: Selecting survey to clean
        self.group_03 = QGroupBox("-- 2. Select survey to clean --", self)
        self.vbox_03 = QGridLayout()
        self.survey_number = QLineEdit()
        self.survey_number.setDisabled(True)
        self.survey_number.setFixedWidth(50)
        self.bot_svy_nmb = QPushButton("Let's clean it!")
        self.bot_svy_nmb.setDisabled(True)
        self.bot_svy_nmb.setFixedWidth(100)
        self.vbox_03.addWidget(self.survey_number,1,1)
        self.vbox_03.addWidget(self.bot_svy_nmb,1,2)
        self.group_03.setLayout(self.vbox_03)

        # Group 04: Writing file
        self.group_04 = QGroupBox("-- 3. Write cleaned data --", self)
        self.vbox_04 = QGridLayout()
        self.err_fixed_chkbx = QCheckBox("Use discrepancy from data",self)
        self.err_fixed_chkbx.setChecked(True)
        self.err_val = QLineEdit("0.01")
        self.fix_err_lab = QLabel("Fixed value:")
        self.err_val.setDisabled(True)
        self.err_val.setFixedWidth(80)
        self.vbox_04.addWidget(self.err_fixed_chkbx,1,1)
        self.vbox_04.addWidget(self.err_val,3,1)
        self.vbox_04.addWidget(self.fix_err_lab,2,1)
        self.bot_write_file = QPushButton("Write file")
        self.bot_write_file.setDisabled(True)
        self.vbox_04.addWidget(self.bot_write_file,4,1)
        self.group_04.setLayout(self.vbox_04)

        # Group 05: Create config file for the inversion
        self.group_05 = QGroupBox("-- 4. Inversion parameters --", self)
        self.vbox_05 = QGridLayout()
        self.invtype_lab = QLabel("Select inversion method:") 
        self.invtype_occ1 = QCheckBox("Occam-R1",self)
        self.invtype_occ2 = QCheckBox("Occam-R2",self)
        self.invtype_mrq = QCheckBox("Marquardt",self)
        self.invtype_eq = QCheckBox("Equivalents",self)
        self.bot_config_file = QPushButton("Config parameters")
        self.bot_config_file.setDisabled(True)
        self.vbox_05.addWidget(self.invtype_lab,1,1)
        self.vbox_05.addWidget(self.invtype_occ1,2,1)
        self.vbox_05.addWidget(self.invtype_occ2,2,2)
        self.vbox_05.addWidget(self.invtype_mrq,3,1)
        self.vbox_05.addWidget(self.invtype_eq,3,2)
        self.vbox_05.addWidget(self.bot_config_file,4,1,1,2)
        self.group_05.setLayout(self.vbox_05)

        # Group 06: run-inversion button
        self.group_06 = QGroupBox("-- 5. Run inversion --", self)
        self.vbox_06 = QGridLayout()
        self.bot_run_inv = QPushButton("Run inversion")
        self.bot_run_inv.setDisabled(True)
        self.vbox_06.addWidget(self.bot_run_inv,1,1)
        self.group_06.setLayout(self.vbox_06)

        # Add all groups within the grid
        self.grid.addWidget(self.title,1,1,1,2)
        self.grid.addWidget(self.group_01,2,1)
        self.grid.addWidget(self.group_02,2,2,1,1)
        self.grid.addWidget(self.group_03,3,1)
        self.grid.addWidget(self.group_04,4,1)
        self.grid.addWidget(self.group_05,5,1)
        self.grid.addWidget(self.group_06,6,1)
        self.grid.addWidget(self.bot_exit,9,3)
        self.grid.addWidget(self.bot_close_all,9,2)

        # Connections
        self.bot_get_data_file.clicked.connect(self.update_labels)
        self.bot_get_data_file.clicked.connect(self.enable_bot_svy_nmb)
        self.bot_svy_nmb.clicked.connect(self.push_clean_button)
        self.bot_svy_nmb.clicked.connect(self.enable_write_file_but)
        self.bot_svy_nmb.clicked.connect(self.update_labels_writing)
        self.bot_config_file.clicked.connect(self.write_config_file)
        self.bot_write_file.clicked.connect(self.enable_config_but)
        self.bot_write_file.clicked.connect(self.write_data_file)
        self.bot_write_file.clicked.connect(self.update_lab_data_written)
        self.bot_exit.clicked.connect(self.close)
        self.bot_close_all.clicked.connect(self.close_all_fig)
        self.invtype_occ1.stateChanged.connect(self.toggle_chkbx_info)
        self.invtype_occ2.stateChanged.connect(self.toggle_chkbx_info)
        self.invtype_mrq.stateChanged.connect(self.toggle_chkbx_info)
        self.invtype_eq.stateChanged.connect(self.toggle_chkbx_info)
        self.invtype_occ1.stateChanged.connect(self.update_lab_inv_type)
        self.invtype_occ2.stateChanged.connect(self.update_lab_inv_type)
        self.invtype_mrq.stateChanged.connect(self.update_lab_inv_type)
        self.invtype_eq.stateChanged.connect(self.update_lab_inv_type)
        self.err_fixed_chkbx.stateChanged.connect(self.toggle_chkbx_err)
        self.bot_config_file.clicked.connect(self.enable_bot_run_inv)
        self.bot_config_file.clicked.connect(self.update_lab_inv_param)
        
        self.bg  =QButtonGroup()
        self.bg.addButton(self.invtype_occ1,1)
        self.bg.addButton(self.invtype_occ2,2)
        self.bg.addButton(self.invtype_mrq,3)
        self.bg.addButton(self.invtype_eq,4)

    def update_lab_inv_type(self):
        self.inf_06.setStyleSheet('color: green')
        if invtype == "occ1":
            self.inf_06.setText("Inversion method: Occam R1")
        elif invtype == "occ2":
            self.inf_06.setText("Inversion method: Occam R2")
        elif invtype == "mrq":
            self.inf_06.setText("Inversion method: Marquardt")
        elif invtype == "eq":
            self.inf_06.setText("Inversion method: Equivalents")

    def update_lab_data_written(self):
        self.inf_05.setStyleSheet('color: green')
        self.inf_05.setText("Data file status: Written ")

    def update_lab_inv_param(self):
        self.inf_07.setStyleSheet('color: green')
        self.inf_07.setText("Inversion parameters: Ready")

    def toggle_chkbx_err(self):
        if self.err_fixed_chkbx.isChecked():
            self.err_val.setDisabled(True)
        else:
            self.err_val.setDisabled(False)

    def toggle_chkbx_info(self):
        global invtype
        if self.invtype_occ1.isChecked():
            invtype = "occ1"
        elif self.invtype_occ2.isChecked():
            invtype = "occ2"
        elif self.invtype_mrq.isChecked():
            invtype = "mrq"
        elif self.invtype_eq.isChecked():
            invtype = "eq"

    def close_all_fig(self):
        plt.close('all')

    def select_file(self):
        global fileName
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, nada = QFileDialog.getOpenFileName(self,"Select files to plot"\
                , ""\
                ," Universal Sounding Format Files (*.usf)"\
                , options=options)
        if fileName:
            flg1 = plot_file(fileName)
        if flg1 == 1:
            self.inf_04.setStyleSheet('color: navy')
            self.inf_04.setText("Noise file: Yes")
        elif flg1 == 0:
            self.inf_04.setStyleSheet('color: red')
            self.inf_04.setText("Noise file: No")

    def update_labels(self):
        ns = get_info_labels(fileName)
        ofn = fileName.split("/")[-1].split(".")[0]
        self.inf_01.setText("Filename: %s" % ofn)
        self.inf_02.setText("Number of surveys: %02d" % ns)

    def enable_bot_run_inv(self):
        self.bot_run_inv.setDisabled(False)

    def enable_bot_svy_nmb(self):
        self.bot_svy_nmb.setDisabled(False)
        self.survey_number.setDisabled(False)

    def enable_write_file_but(self):
        self.bot_write_file.setDisabled(False)

    def enable_config_but(self):
        self.bot_config_file.setDisabled(False)

    def write_data_file(self):
        coillen = float(self.coil_len.text())
        ramplen = float(self.ramp_len.text())
        if not self.err_fixed_chkbx.isChecked():
            err_fixed_val = float(self.err_val.text())
        else:
            err_fixed_val = []
        write_data_all_datafile(coillen, ramplen, val=err_fixed_val)

    def push_clean_button(self):
        global raw_svy_nmb
        raw_svy_nmb = int(self.survey_number.text())
        clean_survey(raw_svy_nmb)
    
    def update_labels_writing(self):
        self.inf_03.setText("Survey to write: %02d" % raw_svy_nmb)

    def write_config_file(self):
        cfg_edit_window = QDialog(self)
        cfg_edit_window.setWindowTitle(self.tr("Inversion parameters"))
        cfg_edit_window.resize(200,30)
        layout_cfg_win = QGridLayout(cfg_edit_window)

        if invtype == "occ1":
            self.box_01 = QGroupBox("-- Occam R1 Parameters --", self)
            self.box_layout01 = QGridLayout()
            prm01 = QLineEdit(self)
            prm01_l = QLabel("Number of layers")
            prm01_l.setStyleSheet('color: green')
            prm02 = QLineEdit(self)
            prm02_l = QLabel("Thickness of first layer [m]")
            prm02_l.setStyleSheet('color: green')
            prm03 = QLineEdit(self)
            prm03_l = QLabel("Depth of last layer [m]")
            prm03_l.setStyleSheet('color: green')
            prm04 = QLineEdit(self)
            prm04_l = QLabel("Resistivity of layers [ohm-m]")
            prm04_l.setStyleSheet('color: green')
            prm05 = QLineEdit(self)
            prm05_l = QLabel("Maximum number os iterations")
            prm05_l.setStyleSheet('color: green')
            self.box_layout01.addWidget(prm01,1,1)
            self.box_layout01.addWidget(prm01_l,1,2)
            self.box_layout01.addWidget(prm02,2,1)
            self.box_layout01.addWidget(prm02_l,2,2)
            self.box_layout01.addWidget(prm03,3,1)
            self.box_layout01.addWidget(prm03_l,3,2)
            self.box_layout01.addWidget(prm04,4,1)
            self.box_layout01.addWidget(prm04_l,4,2)
            self.box_layout01.addWidget(prm05,5,1)
            self.box_layout01.addWidget(prm05_l,5,2)
            self.box_01.setLayout(self.box_layout01)
        elif invtype == "occ2":
            self.box_01 = QGroupBox("-- Occam R2 Parameters --", self)
            self.box_layout01 = QGridLayout()
            prm01 = QLineEdit(self)
            prm01_l = QLabel("Number of layers")
            prm01_l.setStyleSheet('color: green')
            prm02 = QLineEdit(self)
            prm02_l = QLabel("Thickness of first layer [m]")
            prm02_l.setStyleSheet('color: green')
            prm03 = QLineEdit(self)
            prm03_l = QLabel("Depth of last layer [m]")
            prm03_l.setStyleSheet('color: green')
            prm04 = QLineEdit(self)
            prm04_l = QLabel("Resistivity of layers [ohm-m]")
            prm04_l.setStyleSheet('color: green')
            prm05 = QLineEdit(self)
            prm05_l = QLabel("Maximum number os iterations")
            prm05_l.setStyleSheet('color: green')
            self.box_layout01.addWidget(prm01,1,1)
            self.box_layout01.addWidget(prm01_l,1,2)
            self.box_layout01.addWidget(prm02,2,1)
            self.box_layout01.addWidget(prm02_l,2,2)
            self.box_layout01.addWidget(prm03,3,1)
            self.box_layout01.addWidget(prm03_l,3,2)
            self.box_layout01.addWidget(prm04,4,1)
            self.box_layout01.addWidget(prm04_l,4,2)
            self.box_layout01.addWidget(prm05,5,1)
            self.box_layout01.addWidget(prm05_l,5,2)
            self.box_01.setLayout(self.box_layout01)
        elif invtype == "mrq":
            self.box_01 = QGroupBox("-- Marquardt --", self)
            self.box_layout01 = QGridLayout()
            prm01 = QLineEdit(self)
            prm01_l = QLabel("Number of layers")
            prm01_l.setStyleSheet('color: green')
            prm02 = QLineEdit(self)
            prm02_l = QLabel("Thickness of first layer [m]")
            prm02_l.setStyleSheet('color: green')
            prm03 = QLineEdit(self)
            prm03_l = QLabel("Depth of last layer [m]")
            prm03_l.setStyleSheet('color: green')
            prm04 = QLineEdit(self)
            prm04_l = QLabel("Resistivity of layers [ohm-m]")
            prm04_l.setStyleSheet('color: green')
            prm05 = QLineEdit(self)
            prm05_l = QLabel("Maximum number os iterations")
            prm05_l.setStyleSheet('color: green')
            self.box_layout01.addWidget(prm01,1,1)
            self.box_layout01.addWidget(prm01_l,1,2)
            self.box_layout01.addWidget(prm02,2,1)
            self.box_layout01.addWidget(prm02_l,2,2)
            self.box_layout01.addWidget(prm03,3,1)
            self.box_layout01.addWidget(prm03_l,3,2)
            self.box_layout01.addWidget(prm04,4,1)
            self.box_layout01.addWidget(prm04_l,4,2)
            self.box_layout01.addWidget(prm05,5,1)
            self.box_layout01.addWidget(prm05_l,5,2)
            self.box_01.setLayout(self.box_layout01)
        elif invtype == "eq":
            self.box_01 = QGroupBox("-- Equivalents --", self)
            self.box_layout01 = QGridLayout()
            prm01 = QLineEdit(self)
            prm01_l = QLabel("Number of layers")
            prm01_l.setStyleSheet('color: green')
            prm02 = QLineEdit(self)
            prm02_l = QLabel("Thickness of first layer [m]")
            prm02_l.setStyleSheet('color: green')
            prm03 = QLineEdit(self)
            prm03_l = QLabel("Depth of last layer [m]")
            prm03_l.setStyleSheet('color: green')
            prm04 = QLineEdit(self)
            prm04_l = QLabel("Resistivity of layers [ohm-m]")
            prm04_l.setStyleSheet('color: green')
            prm05 = QLineEdit(self)
            prm05_l = QLabel("Maximum number os iterations")
            prm05_l.setStyleSheet('color: green')
            self.box_layout01.addWidget(prm01,1,1)
            self.box_layout01.addWidget(prm01_l,1,2)
            self.box_layout01.addWidget(prm02,2,1)
            self.box_layout01.addWidget(prm02_l,2,2)
            self.box_layout01.addWidget(prm03,3,1)
            self.box_layout01.addWidget(prm03_l,3,2)
            self.box_layout01.addWidget(prm04,4,1)
            self.box_layout01.addWidget(prm04_l,4,2)
            self.box_layout01.addWidget(prm05,5,1)
            self.box_layout01.addWidget(prm05_l,5,2)
            self.box_01.setLayout(self.box_layout01)
    
        self.bot_save_param = QPushButton("Save parameters",self)
        self.bot_save_param2 = QPushButton('Save parameters && Exit',self)
        self.bot_save_param2.clicked.connect(cfg_edit_window.close)
        layout_cfg_win.addWidget(self.box_01,1,1,1,2)
        layout_cfg_win.addWidget(self.bot_save_param,2,1)
        layout_cfg_win.addWidget(self.bot_save_param2,2,2)
        cfg_edit_window.exec_()


if __name__ == "__main__":
    import sys
    app = QApplication([])
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
