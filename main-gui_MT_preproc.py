#!/usr/bin/python
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
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QWidget
from funcs_gui_MT_preproc import plot_file, get_info_labels
from funcs_gui_MT_preproc import clean_survey

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
        # Title
        self.title = QLabel("<h3>GUI to process invert and plot TEM data<\h3>",self)

        # Group 01: Select file to plot data
        self.group_01 = QGroupBox("-- 1. Selecting data --", self)
        self.vbox_01 = QVBoxLayout()
        self.bot_get_data_file = QPushButton("Select files")
        self.bot_get_data_file.setDisabled(False)
        self.vbox_01.addWidget(self.bot_get_data_file)
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
        self.vbox_02.addWidget(self.inf_01)
        self.vbox_02.addWidget(self.inf_02)
        self.vbox_02.addWidget(self.inf_04)
        self.vbox_02.addWidget(self.inf_03)
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
        self.vbox_04 = QVBoxLayout()
        self.bot_write_file = QPushButton("Write file")
        self.bot_write_file.setDisabled(True)
        self.vbox_04.addWidget(self.bot_write_file)
        self.group_04.setLayout(self.vbox_04)

        # Group 05: Create config file for the inversion
        self.group_05 = QGroupBox("-- 4. Inversion config file --", self)
        self.vbox_05 = QVBoxLayout()
        self.bot_config_file = QPushButton("Config file")
        self.bot_config_file.setDisabled(True)
        self.vbox_05.addWidget(self.bot_config_file)
        self.group_05.setLayout(self.vbox_05)

        # Add all groups within the grid
        self.grid.addWidget(self.title,1,1,1,3)
        self.grid.addWidget(self.group_01,2,1)
        self.grid.addWidget(self.group_02,2,2)
        self.grid.addWidget(self.group_03,3,1)
        self.grid.addWidget(self.group_04,4,1)
        self.grid.addWidget(self.group_05,5,1)
        self.grid.addWidget(self.bot_exit,9,3)

        # Connections
        self.bot_get_data_file.clicked.connect(self.update_labels)
        self.bot_get_data_file.clicked.connect(self.enable_bot_svy_nmb)
        self.bot_svy_nmb.clicked.connect(self.push_clean_button)
        self.bot_svy_nmb.clicked.connect(self.enable_write_file_but)
        self.bot_svy_nmb.clicked.connect(self.update_labels_writing)
        self.bot_config_file.clicked.connect(self.write_config_file)
        self.bot_write_file.clicked.connect(self.enable_config_but)
        self.bot_exit.clicked.connect(self.close)

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

    def enable_bot_svy_nmb(self):
        self.bot_svy_nmb.setDisabled(False)
        self.survey_number.setDisabled(False)

    def enable_write_file_but(self):
        self.bot_write_file.setDisabled(False)

    def enable_config_but(self):
        self.bot_config_file.setDisabled(False)

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

        self.box_01 = QGroupBox("-- Configuration file 1 --", self)
        self.box_layout01 = QGridLayout()
        prm01 = QLineEdit(self)
        prm01_l = QLabel("Parametro 1")
        prm01_l.setStyleSheet('color: green')
        prm02 = QLineEdit(self)
        prm02_l = QLabel("Parametro 2")
        prm02_l.setStyleSheet('color: green')
        prm03 = QLineEdit(self)
        prm03_l = QLabel("Parametro 3")
        prm03_l.setStyleSheet('color: green')
        prm04 = QLineEdit(self)
        prm04_l = QLabel("Parametro 4")
        prm04_l.setStyleSheet('color: green')
        prm05 = QLineEdit(self)
        prm05_l = QLabel("Parametro 5")
        prm05_l.setStyleSheet('color: green')
        prm06 = QLineEdit(self)
        prm06_l = QLabel("Parametro 6")
        prm06_l.setStyleSheet('color: green')
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
        self.box_layout01.addWidget(prm06,6,1)
        self.box_layout01.addWidget(prm06_l,6,2)
        self.box_01.setLayout(self.box_layout01)

        self.box_02 = QGroupBox("-- Configuration file 2 --", self)
        self.box_layout02 = QGridLayout()
        prm31 = QLineEdit(self)
        prm31_l = QLabel("Parametro 1")
        prm31_l.setStyleSheet('color: green')
        self.box_layout02.addWidget(prm31,1,1)
        self.box_layout02.addWidget(prm31_l,1,2)
        self.box_02.setLayout(self.box_layout02)

        self.bot_save_param = QPushButton("Save parameters",self)
#        self.bot_save_param.setFixedWidth(80)

        layout_cfg_win.addWidget(self.box_01,1,1)
        layout_cfg_win.addWidget(self.box_02,1,2)
        layout_cfg_win.addWidget(self.bot_save_param,2,1,1,3)
        cfg_edit_window.exec_()

if __name__ == "__main__":
    import sys
    app = QApplication([])
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
