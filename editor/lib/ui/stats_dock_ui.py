# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'stats_dock.ui'
#
# Created: Tue Mar 15 20:43:50 2016
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_StatsDock(object):
    def setupUi(self, StatsDock):
        StatsDock.setObjectName("StatsDock")
        StatsDock.resize(320, 120)
        StatsDock.setMinimumSize(QtCore.QSize(320, 120))
        StatsDock.setMaximumSize(QtCore.QSize(524287, 524287))
        StatsDock.setBaseSize(QtCore.QSize(0, 0))
        StatsDock.setAllowedAreas(QtCore.Qt.AllDockWidgetAreas)
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setMinimumSize(QtCore.QSize(320, 80))
        self.dockWidgetContents.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.verticalLayoutWidget = QtGui.QWidget(self.dockWidgetContents)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 321, 91))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.verticalLayoutWidget.setFont(font)
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setSizeConstraint(QtGui.QLayout.SetMaximumSize)
        self.verticalLayout.setContentsMargins(10, -1, 0, -1)
        self.verticalLayout.setObjectName("verticalLayout")
        self.mainLabel = QtGui.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.mainLabel.setFont(font)
        self.mainLabel.setIndent(0)
        self.mainLabel.setObjectName("mainLabel")
        self.verticalLayout.addWidget(self.mainLabel)
        self.luaLabel = QtGui.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.luaLabel.setFont(font)
        self.luaLabel.setObjectName("luaLabel")
        self.verticalLayout.addWidget(self.luaLabel)
        self.memoryLabel = QtGui.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.memoryLabel.setFont(font)
        self.memoryLabel.setObjectName("memoryLabel")
        self.verticalLayout.addWidget(self.memoryLabel)
        self.actionLabel = QtGui.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.actionLabel.setFont(font)
        self.actionLabel.setObjectName("actionLabel")
        self.verticalLayout.addWidget(self.actionLabel)
        StatsDock.setWidget(self.dockWidgetContents)

        self.retranslateUi(StatsDock)
        QtCore.QMetaObject.connectSlotsByName(StatsDock)

    def retranslateUi(self, StatsDock):
        StatsDock.setWindowTitle(QtGui.QApplication.translate("StatsDock", "Stats", None, QtGui.QApplication.UnicodeUTF8))
        self.mainLabel.setText(QtGui.QApplication.translate("StatsDock", "MAIN", None, QtGui.QApplication.UnicodeUTF8))
        self.luaLabel.setText(QtGui.QApplication.translate("StatsDock", "LUA", None, QtGui.QApplication.UnicodeUTF8))
        self.memoryLabel.setText(QtGui.QApplication.translate("StatsDock", "MEMORY", None, QtGui.QApplication.UnicodeUTF8))
        self.actionLabel.setText(QtGui.QApplication.translate("StatsDock", "ACTION", None, QtGui.QApplication.UnicodeUTF8))

