#!/usr/bin/python
# -*- coding: utf-8 -*-
""" 
GUI to preprocess raw data directly from TEM equipment.

It shows a time series and allows you to select points, either one by one or by a time window, and removes the selected points

Developed by: Oscar Castro-Artola. April, 2020. E-Mail:oscar.castro@unicach.mx"
"""
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QDialog,QApplication
from PyQt5.QtWidgets import QPushButton,QVBoxLayout
from PyQt5.QtWidgets import QGroupBox,QFileDialog
from PyQt5.QtWidgets import QLabel,QGridLayout
from PyQt5.QtWidgets import QLineEdit
from funcs_gui_MT_preproc import plot_file, get_info_labels
from funcs_gui_MT_preproc import clean_survey

class MainWindow(QDialog):
    # MAIN FUNCTION
    def __init__(self):
        super(MainWindow, self).__init__()
        self.resize(300,100)
        self.setWindowTitle(self.tr("Pre-Process raw TEM data"))
        self.grid = QGridLayout()
        self.setLayout(self.grid)

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

        # Group 04: Selecting survey to clean
        self.group_04 = QGroupBox("-- 3. Write cleaned data --", self)
        self.vbox_04 = QVBoxLayout()
        self.bot_write_file = QPushButton("Write file")
        self.bot_write_file.setDisabled(True)
        self.vbox_04.addWidget(self.bot_write_file)
        self.group_04.setLayout(self.vbox_04)

        # Group 05: Create confi file for the inversion
        self.group_05 = QGroupBox("-- 4. Inversion config file --", self)
        self.vbox_05 = QVBoxLayout()
        self.bot_config_file = QPushButton("Config file")
        self.bot_config_file.setDisabled(True)
        self.vbox_05.addWidget(self.bot_config_file)
        self.group_05.setLayout(self.vbox_05)

        # Add all groups within the grid
        self.grid.addWidget(self.group_01,1,1)
        self.grid.addWidget(self.group_02,1,2)
        self.grid.addWidget(self.group_03,2,1)
        self.grid.addWidget(self.group_04,3,1)
        self.grid.addWidget(self.group_05,4,1)

        # Connections
        self.bot_get_data_file.clicked.connect(self.update_labels)
        self.bot_get_data_file.clicked.connect(self.enable_bot_svy_nmb)
        self.bot_svy_nmb.clicked.connect(self.push_clean_button)
        self.bot_svy_nmb.clicked.connect(self.enable_write_file_but)
        self.bot_svy_nmb.clicked.connect(self.update_labels_writing)
        self.bot_write_file.clicked.connect(self.enable_config_but)

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

if __name__ == "__main__":
    import sys
    app = QApplication([])
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
