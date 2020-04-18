#!/usr/bin/python
# -*- coding: utf-8 -*-
""" 
GUI to preprocess raw data directly from TEM equipment.

It shows a time series and allows you to select points, either one by one or by a time window, and removes the selected points
"""
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QDialog,QApplication
from PyQt5.QtWidgets import QPushButton,QVBoxLayout
from PyQt5.QtWidgets import QGroupBox,QFileDialog







class MainWindow(QDialog):
    # MAIN FUNCTION
    def __init__(self):
        super(MainWindow, self).__init__()
        self.resize(300,100)
        self.setWindowTitle(self.tr("Pre-Process raw TEM data"))
        self.group_1 = QGroupBox("-- Selecting data --", self)
        self.vbox_1 = QVBoxLayout()
        self.bot_get_data_file = QPushButton("Choose your fucking files")
        self.bot_get_data_file.setDisabled(False)
        self.vbox_1.addWidget(self.bot_get_data_file)
        self.bot_get_data_file.clicked.connect(self.get_data)
        self.group_1.setLayout(self.vbox_1)

    def get_data(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"Select files to plot"\
                , ""\
                ,"All Files (*);;Python Files (*.py)"\
                , options=options)
        if fileName:
            print(fileName)


if __name__ == "__main__":
    import sys
    app = QApplication([])
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
