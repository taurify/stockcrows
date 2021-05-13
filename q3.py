# coding=<utf-8>
"""StockCrow UI."""

import random
import sys

import assets.datagen
from assets.datagen import CompanyData

# import time
# import numpy as np
# import PyQt5
# import matplotlib as mpl
# mpl.rcParams["MPLBACKEND"] = "Qt5Agg"
import matplotlib.dates as mdates
from matplotlib.backends.qt_compat import QtCore, QtWidgets, QtGui
from PyQt5.QtGui import QIcon

if QtCore.qVersion() >= "5.":  # , NavigationToolbar2QT as NavigationToolbar
    from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
# else:  # Could be disabled completely
#     from matplotlib.backends.backend_qt4agg import (
#         FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure


class ApplicationWindow(QtWidgets.QMainWindow):
    """Main window interface."""

    def __init__(self, companies):
        """Initialize window, most of it is generated code."""
        super().__init__()
        # Init window
        self.resize(800, 600)  # Set window size
        self._win = QtWidgets.QWidget()
        self.setCentralWidget(self._win)
        self._win.setObjectName("MainWindow")
        self.setWindowTitle("StockCrows")  # Set window title
        self.setWindowIcon(QIcon('assets/crow.svg'))

        # Layout magic
        layout = QtWidgets.QVBoxLayout(self._win)
        hbox1 = QtWidgets.QHBoxLayout()
        hbox2 = QtWidgets.QHBoxLayout()
        hbox3 = QtWidgets.QHBoxLayout()
        hbox4 = QtWidgets.QHBoxLayout()
        layout.addLayout(hbox1)
        layout.addLayout(hbox2)
        layout.addLayout(hbox3)
        layout.addLayout(hbox4)

        # Site title
        self.label1 = QtWidgets.QLabel()
        hbox1.addStretch()
        hbox1.addWidget(self.label1)
        hbox1.addStretch()
        self.label1.setGeometry(QtCore.QRect(340, 70, 331, 71))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label1.setFont(font)
        self.label1.setScaledContents(True)
        self.label1.setObjectName("label1")

        # Index image
        self.image_index = QtWidgets.QLabel()
        hbox2.addStretch()
        hbox2.addWidget(self.image_index)
        hbox2.addStretch()
        self.image_index.setGeometry(QtCore.QRect(79, 70, 191, 181))
        self.image_index.setText("")  # Need?
        self.image_index.setPixmap(QtGui.QPixmap("assets/crow.jpeg"))
        self.image_index.setObjectName("image_index")
        self.image_index.setScaledContents(False)

        # Stock combobox
        self.comboBox_select_stock = QtWidgets.QComboBox()
        hbox3.addWidget(self.comboBox_select_stock)
        self.comboBox_select_stock.setGeometry(QtCore.QRect(150, 280, 96, 29))
        self.comboBox_select_stock.setObjectName("comboBox_select_stock")

        companies = [CompanyData("Aktsiad")] + companies
        for _ in companies:  # Add stock names to combobox
            self.comboBox_select_stock.addItem(_.name)

        # Choose investor combo box
        self.comboBox_choose_investor = CheckableComboBox()
        hbox4.addWidget(self.comboBox_choose_investor)
        self.comboBox_choose_investor.setObjectName("comboBox_choose_investor")
        self.comboBox_choose_investor.addItem(" ")
        item = self.comboBox_choose_investor.model().item(self.comboBox_choose_investor.count() - 1, 0)
        item.setFlags(QtCore.Qt.NoItemFlags)

        for i in range(10):
            self.comboBox_choose_investor.add_item(f"Investor {i + 1}")
            item = self.comboBox_choose_investor.model().item(self.comboBox_choose_investor.count() - 1, 0)
            item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            item.setCheckState(QtCore.Qt.Unchecked)

        # Time combo box
        time_labels = ["", "Nädal", "Kuu", "Aasta"]
        self.comboBox_select_time = QtWidgets.QComboBox()
        hbox3.addWidget(self.comboBox_select_time)
        self.comboBox_select_time.setGeometry(QtCore.QRect(350, 280, 96, 29))
        self.comboBox_select_time.setObjectName("comboBox_select_time")

        for _ in time_labels:  # Add time units to combobox
            self.comboBox_select_time.addItem(_)

        # Button
        self.button_show = QtWidgets.QPushButton()
        hbox3.addWidget(self.button_show)
        self.button_show.setGeometry(QtCore.QRect(530, 280, 106, 30))
        self.button_show.setObjectName("button_show")
        self.button_show.clicked.connect(self.pressed)

        # Plot
        self.companies = companies
        self.static_canvas = PlotCanvas(width=5, height=4, data=self.companies[0].data, title=self.companies[0].name)
        layout.addWidget(self.static_canvas)

        self.retranslate_ui(self._win)
        QtCore.QMetaObject.connectSlotsByName(self._win)

    def retranslate_ui(self, window):
        """Auto generated, change label texts."""
        _translate = QtCore.QCoreApplication.translate
        window.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.button_show.setText(_translate("MainWindow", "Näita"))
        self.label1.setText(_translate("MainWindow", "Welcome to StockCrows"))

    def pressed(self):
        """Update on show button click."""
        i = self.comboBox_select_stock.currentIndex()
        j = self.comboBox_select_time.currentIndex()
        ticked = self.comboBox_choose_investor.get_ticks()
        if len(ticked) < 10:
            for _ in range(10 - len(ticked)):
                ticked.append(False)
        self.static_canvas.set_data(self.get_data_range(i, j, ticked), self.companies[i].name, ticked)

    def get_data_range(self, i: int, j: int, ticked: list):
        """Select all, last week, last month or last year."""
        data = []
        for a in range(0, 10):
            data.append([])
            if not ticked[a]:
                continue
            sub2 = self.companies[i]
            m = len(sub2.data[a])
            if j == 1:
                b = min(7, m)
            elif j == 2:
                b = min(30, m)
            elif j == 3:
                b = min(365, m)
            else:
                b = m
            n = max(b // 200, 1)
            for k in range(-b, -1, n):
                sub = self.companies[i].data[a][k]
                data[a].append(sub)
        return data


class PlotCanvas(FigureCanvas):
    """Extend matplotlib plots."""
    investors = ['Investor 1', 'Investor 2', 'Investor 3', 'Investor 4', 'Investor 5',
                 'Investor 6', 'Investor 7', 'Investor 8', 'Investor 9', 'Investor 10']
    colors2 = ["aqua", "aquamarine", "black", "blue", "brown", "chartreuse", "chocolate", "coral",
               "crimson", "cyan", "darkblue", "darkgreen", "fuchsia", "goldenrod", "green", "indigo",
               "khaki", "lavender", "lightgreen", "lime", "magenta", "maroon", "navy", "olive", "orange",
               "orangered", "orchid", "plum", "purple", "red", "salmon", "sienna", "tan", "teal",
               "turquoise", "violet", "yellow", "yellowgreen"]
    colors3 = ["b", "g", "r", "c", "m", "y", "k"]

    def __init__(self, parent=None, width=5, height=4, dpi=100, data=None, title=""):
        if data is None:  # Guard hack for mutable default parameter
            data = [[]]
        x = []
        y = []
        self.axes = []
        self.title = title
        self.legend = []

        FigureCanvas.__init__(self, Figure(figsize=(width, height), dpi=dpi))
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.axes = self.figure.add_subplot(1, 1, 1)
        self.plot(x, y)

    def plot(self, x, y):
        s = f"{PlotCanvas.colors2[random.randint(0, len(PlotCanvas.colors2) - 1)]}"
        self.axes.plot(x, y, s)
        self.axes.legend(self.legend)

        # X-axis time formatting
        locator = mdates.AutoDateLocator()
        formatter = mdates.ConciseDateFormatter(locator)
        self.axes.xaxis.set_major_locator(locator)
        self.axes.xaxis.set_major_formatter(formatter)

        self.axes.set_title(self.title)
        self.axes.set_ylim(0, 200)

        self.draw()

    def set_data(self, data, title, ticked):
        self.figure.clear()
        self.axes = self.figure.add_subplot(1, 1, 1)

        self.title = title
        self.legend = []
        for a in range(10):
            if ticked[a]:
                self.legend.append(PlotCanvas.investors[a])

        for a in range(10):
            if not ticked[a]:
                continue
            y = [_[1] for _ in data[a]]
            x = [_[0] for _ in data[a]]

            self.plot(x, y)


class CheckableComboBox(QtWidgets.QComboBox):
    def __init__(self):
        super(CheckableComboBox, self).__init__()
        self.view().pressed.connect(self.handle)
        self.setModel(QtGui.QStandardItemModel(self))
        self.items = []

    def handle(self, index):
        item = self.model().itemFromIndex(index)
        if item.checkState() == QtCore.Qt.Checked:
            item.setCheckState(QtCore.Qt.Unchecked)
        else:
            item.setCheckState(QtCore.Qt.Checked)

    def add_item(self, item):
        super().addItem(item)
        _item = self.model().item(self.count() - 1, 0)
        self.items.append(_item)

    def get_ticks(self):
        ticks = []
        for each in self.items:
            ticks.append(each.checkState() == QtCore.Qt.Checked)
        return ticks


if __name__ == "__main__":
    # Check whether there is already a running QApplication (e.g., if running from an IDE).
    # ../venv/bin/python3 q3.py
    namelist = ["ARCO VARA AKTSIAD", "BALTIKA LIHTAKTSIAD", "COOP PANK AKTSIAD", "EFTEN REAL ESTATE FUND 3 AKTSIAD",
                "EKSPRESS GRUPP AKTSIAD", "ESTONIAN JAPAN TRADING COMPANY AS", "HARJU ELEKTER AKTSIA",
                "LHV GROUP LIHTAKTSIA", "LINDA NEKTAR LIHTAKTSIA", "MERKO EHITUS AKTSIA", "NORDECON LIHTAKTSIA",
                "NORDIC FIBREBOARD AKTSIA", "PRFOODS AKTSIA", "PRO KAPITAL GRUPP AKTSIA", "SAUNUM GROUP AKTSIA",
                "SILVANO FASHION GROUP AKTSIA", "TALLINK GRUPP AKTSIA", "TALLINNA KAUBAMAJA GRUPP AKTSIA",
                "TALLINNA SADAM AKTSIA", "TALLINNA VESI A-AKTSIA", "TRIGON PROPERTY DEVELOPMENT AKTSIA"]
    company_data = assets.datagen.generate_company_data(namelist)  # Or read assets file

    qapp = QtWidgets.QApplication.instance()  # Y need u?
    if not qapp:
        qapp = QtWidgets.QApplication(sys.argv)

    app = ApplicationWindow(company_data)
    app.show()
    app.activateWindow()
    app.raise_()
    qapp.exec_()
