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
from funcs_gui_MT_preproc import plot_file, get_info_labels

class MainWindow(QDialog):
    # MAIN FUNCTION
    def __init__(self):
        super(MainWindow, self).__init__()
        self.resize(300,100)
        self.setWindowTitle(self.tr("Pre-Process raw TEM data"))
        self.grid = QGridLayout()
        self.setLayout(self.grid)
        # Group 01: Select file to plot data
        self.group_01 = QGroupBox("-- Selecting data --", self)
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
        self.inf_01.setStyleSheet('color: navy')
        self.inf_01.setText("Filename: ")
        self.inf_02 = QLabel() # Number of surveys
        self.inf_02.setStyleSheet('color: navy')
        self.inf_02.setText("Number of surveys: ")
        self.vbox_02.addWidget(self.inf_01)
        self.vbox_02.addWidget(self.inf_02)
        self.group_02.setLayout(self.vbox_02)
        # Add all groups within the grid
        self.grid.addWidget(self.group_01,1,1)
        self.grid.addWidget(self.group_02,2,1)
        # Connections
        self.bot_get_data_file.clicked.connect(self.update_labels)

    def select_file(self):
        global fileName
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, nada = QFileDialog.getOpenFileName(self,"Select files to plot"\
                , ""\
                ," Universal Sounding Format Files (*.usf)"\
                , options=options)
        if fileName:
            plot_file(fileName)

    def update_labels(self):
        ns = get_info_labels(fileName)
        ofn = fileName.split("/")[-1].split(".")[0]
        self.inf_01.setText("Filename: %s" % ofn)
        self.inf_02.setText("Number of surveys: %02d" % ns)

if __name__ == "__main__":
    import sys
    app = QApplication([])
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
