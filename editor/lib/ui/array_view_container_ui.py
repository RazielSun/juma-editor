# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'array_view_container.ui'
#
# Created: Sat Jun 11 12:39:54 2016
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_ArrayViewContainer(object):
    def setupUi(self, ArrayViewContainer):
        ArrayViewContainer.setObjectName("ArrayViewContainer")
        ArrayViewContainer.resize(400, 300)
        self.mainLayout = QtGui.QVBoxLayout(ArrayViewContainer)
        self.mainLayout.setContentsMargins(5, 5, 5, 5)
        self.mainLayout.setObjectName("mainLayout")
        self.header = QtGui.QWidget(ArrayViewContainer)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.header.sizePolicy().hasHeightForWidth())
        self.header.setSizePolicy(sizePolicy)
        self.header.setMinimumSize(QtCore.QSize(200, 30))
        self.header.setObjectName("header")
        self.headerLayout = QtGui.QHBoxLayout(self.header)
        self.headerLayout.setContentsMargins(5, 5, 5, 5)
        self.headerLayout.setContentsMargins(0, 0, 0, 0)
        self.headerLayout.setObjectName("headerLayout")
        self.totalLabel = QtGui.QLabel(self.header)
        self.totalLabel.setMinimumSize(QtCore.QSize(50, 0))
        self.totalLabel.setObjectName("totalLabel")
        self.headerLayout.addWidget(self.totalLabel)
        self.totalEdit = QtGui.QLineEdit(self.header)
        self.totalEdit.setObjectName("totalEdit")
        self.headerLayout.addWidget(self.totalEdit)
        self.totalBtn = QtGui.QToolButton(self.header)
        self.totalBtn.setObjectName("totalBtn")
        self.headerLayout.addWidget(self.totalBtn)
        self.mainLayout.addWidget(self.header)
        self.body = QtGui.QWidget(ArrayViewContainer)
        self.body.setObjectName("body")
        self.bodyLayout = QtGui.QVBoxLayout(self.body)
        self.bodyLayout.setContentsMargins(5, 5, 5, 5)
        self.bodyLayout.setContentsMargins(0, 0, 0, 0)
        self.bodyLayout.setObjectName("bodyLayout")
        self.mainLayout.addWidget(self.body)

        self.retranslateUi(ArrayViewContainer)
        QtCore.QMetaObject.connectSlotsByName(ArrayViewContainer)

    def retranslateUi(self, ArrayViewContainer):
        ArrayViewContainer.setWindowTitle(QtGui.QApplication.translate("ArrayViewContainer", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.totalLabel.setText(QtGui.QApplication.translate("ArrayViewContainer", "Total:", None, QtGui.QApplication.UnicodeUTF8))
        self.totalBtn.setText(QtGui.QApplication.translate("ArrayViewContainer", "+", None, QtGui.QApplication.UnicodeUTF8))

