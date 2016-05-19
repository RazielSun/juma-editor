# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'array_view_container.ui'
#
# Created: Thu May 19 15:06:53 2016
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_ArrayViewContainer(object):
    def setupUi(self, ArrayViewContainer):
        ArrayViewContainer.setObjectName("ArrayViewContainer")
        ArrayViewContainer.resize(400, 300)
        self.verticalLayout_2 = QtGui.QVBoxLayout(ArrayViewContainer)
        self.verticalLayout_2.setContentsMargins(5, 5, 5, 5)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.header = QtGui.QWidget(ArrayViewContainer)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.header.sizePolicy().hasHeightForWidth())
        self.header.setSizePolicy(sizePolicy)
        self.header.setMinimumSize(QtCore.QSize(200, 30))
        self.header.setObjectName("header")
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.header)
        self.horizontalLayout_2.setContentsMargins(5, 5, 5, 5)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.totalLabel = QtGui.QLabel(self.header)
        self.totalLabel.setMinimumSize(QtCore.QSize(50, 0))
        self.totalLabel.setObjectName("totalLabel")
        self.horizontalLayout_2.addWidget(self.totalLabel)
        self.totalEdit = QtGui.QLineEdit(self.header)
        self.totalEdit.setObjectName("totalEdit")
        self.horizontalLayout_2.addWidget(self.totalEdit)
        self.totalBtn = QtGui.QToolButton(self.header)
        self.totalBtn.setObjectName("totalBtn")
        self.horizontalLayout_2.addWidget(self.totalBtn)
        self.verticalLayout_2.addWidget(self.header)
        self.body = QtGui.QWidget(ArrayViewContainer)
        self.body.setObjectName("body")
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.body)
        self.verticalLayout_3.setContentsMargins(5, 5, 5, 5)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_2.addWidget(self.body)

        self.retranslateUi(ArrayViewContainer)
        QtCore.QMetaObject.connectSlotsByName(ArrayViewContainer)

    def retranslateUi(self, ArrayViewContainer):
        ArrayViewContainer.setWindowTitle(QtGui.QApplication.translate("ArrayViewContainer", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.totalLabel.setText(QtGui.QApplication.translate("ArrayViewContainer", "Total:", None, QtGui.QApplication.UnicodeUTF8))
        self.totalBtn.setText(QtGui.QApplication.translate("ArrayViewContainer", "+", None, QtGui.QApplication.UnicodeUTF8))

