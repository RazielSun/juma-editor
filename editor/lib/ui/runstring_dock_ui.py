# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'runstring_dock.ui'
#
# Created: Thu Apr  7 15:14:46 2016
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_RunStringDock(object):
    def setupUi(self, RunStringDock):
        RunStringDock.setObjectName("RunStringDock")
        RunStringDock.resize(375, 285)
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.textEdit = QtGui.QTextEdit(self.dockWidgetContents)
        self.textEdit.setObjectName("textEdit")
        self.verticalLayout_2.addWidget(self.textEdit)
        self.horizontalWidget = QtGui.QWidget(self.dockWidgetContents)
        self.horizontalWidget.setMinimumSize(QtCore.QSize(30, 30))
        self.horizontalWidget.setObjectName("horizontalWidget")
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtGui.QLabel(self.horizontalWidget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.btnlocal = QtGui.QPushButton(self.horizontalWidget)
        self.btnlocal.setObjectName("btnlocal")
        self.horizontalLayout.addWidget(self.btnlocal)
        self.btnremote = QtGui.QPushButton(self.horizontalWidget)
        self.btnremote.setObjectName("btnremote")
        self.horizontalLayout.addWidget(self.btnremote)
        self.verticalLayout_2.addWidget(self.horizontalWidget)
        RunStringDock.setWidget(self.dockWidgetContents)

        self.retranslateUi(RunStringDock)
        QtCore.QMetaObject.connectSlotsByName(RunStringDock)

    def retranslateUi(self, RunStringDock):
        RunStringDock.setWindowTitle(QtGui.QApplication.translate("RunStringDock", "Run String", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("RunStringDock", "Run String:", None, QtGui.QApplication.UnicodeUTF8))
        self.btnlocal.setText(QtGui.QApplication.translate("RunStringDock", "Local", None, QtGui.QApplication.UnicodeUTF8))
        self.btnremote.setText(QtGui.QApplication.translate("RunStringDock", "Remote", None, QtGui.QApplication.UnicodeUTF8))

