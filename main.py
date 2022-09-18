# This is a sample Python script.
import sys
import pickle
import pandas as pd
import numpy as np
from PyQt5 import QtGui, QtCore, uic, QtWidgets
from PyQt5.QtWidgets import *
import pyqtgraph as pg
from loggerpkg import logger

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

form_class = uic.loadUiType("./resource/aptSiseGraph.ui")[0]

class WindowClass(QMainWindow, form_class):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # initialize
        self.siseDF             = pd.DataFrame()
        self.xData              = list()
        self.yData              = list()

        self.checkedIcon        = QtGui.QIcon('./resource/checkbox_checked.png')
        self.uncheckedIcon      = QtGui.QIcon('./resource/checkbox_unchecked.png')

        # connect functions
        self.lw_region.itemClicked.connect(self.lw_region_itemClicked)
        self.lw_apt.itemClicked.connect(self.lw_apt_itemClicked)
        self.pb_openCSV.clicked.connect(self.pb_openCSVClicked)

        # layout
        self.pw = pg.PlotWidget(title='Basic Plot')
        self.vl_Graph.addWidget(self.pw)

        # data
        x = [0, 1, 2, 3, 4]
        y = [0, 1, 2, 3, 4]

        # style
        self.pw.setBackground('w')
        self.pw.setTitle('매매/전세')
        self.pw.setLabel('left', '금액(만원)')
        self.pw.setLabel('bottom', '년/월')
        self.pw.showGrid(x=True, y=True)
        self.pw.addLegend()

        self.pw.plot(x, y, pen=pg.mkPen('r'),name='default plot', skipFiniteCheck=True)

    def extractData(self):
        self.xData      = self.siseDF.columns.to_list()
        self.Region     = self.siseDF.index.levels[0].to_list()
        self.index      = self.siseDF.index.to_list()
        self.insertRegionList()
        self.updateAptList()

    def insertRegionList(self):
        for region in self.Region :
            listWidgetItem = QListWidgetItem(self.uncheckedIcon, '{}'.format(region))
            self.lw_region.addItem(listWidgetItem)

    def updateAptList(self):
        selectedItems   = self.lw_region.selectedItems()
        self.lw_apt.clear()

        # 여기는 성능이 느려질 수 있으니 추후 개선 필요
        for region, aptName, sellType in self.index :
            for item in selectedItems:
                if item.text() == region :
                    listWidgetItem = QListWidgetItem(self.uncheckedIcon, '{},{}'.format(region, aptName))
                    self.lw_apt.addItem(listWidgetItem)

    def plotGraph(self):
        selectedItems = self.lw_apt.selectedItems()
        for item in selectedItems :
            targetList  = item.text().split(',')
            # plot
            try :
                self.pw.plot(self.xData, self.siseDF.loc[(targetList[0], targetList[1], 'sale')].tolist(), pen=pg.mkPen('r'), name=item, skipFiniteCheck=True)
            except Exception as e :
                log.error(e)
                pass


#################################slot###############################

    def lw_region_itemClicked(self, item):
        selectedItems   = self.lw_region.selectedItems()
        if item in selectedItems :
            item.setIcon(self.checkedIcon)
        else :
            item.setIcon(self.uncheckedIcon)
        self.updateAptList()

    def lw_apt_itemClicked(self, item):
        selectedItems   = self.lw_apt.selectedItems()
        if item in selectedItems :
            item.setIcon(self.checkedIcon)
        else :
            item.setIcon(self.uncheckedIcon)

        self.plotGraph()

    def pb_openCSVClicked(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', './', filter='*.csv')

        if fname[0]:
            self.siseDF     = pd.read_csv(fname[0])
            self.siseDF.rename(columns={'Unnamed: 0': '지역명'}, inplace=True)
            self.siseDF.rename(columns={'Unnamed: 1': '아파트'}, inplace=True)
            self.siseDF.rename(columns={'Unnamed: 2': '시세종류'}, inplace=True)
            self.siseDF.set_index(['지역명', '아파트', '시세종류'], inplace=True)
            self.siseDF.fillna(0, inplace=True)
            self.siseDF = self.siseDF.fillna(0.0).astype(int)
            print(self.siseDF)
        if len(self.siseDF) > 0 :
            self.extractData()
            self.plotGraph()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    log = logger.make_logger()

    log.debug('start')
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    log.debug('end')
    sys.exit(app.exec_())

