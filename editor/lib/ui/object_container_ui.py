# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'object_container.ui'
#
# Created: Fri Mar 18 16:21:34 2016
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_ObjectContainer(object):
    def setupUi(self, ObjectContainer):
        ObjectContainer.setObjectName("ObjectContainer")
        ObjectContainer.resize(357, 184)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ObjectContainer.sizePolicy().hasHeightForWidth())
        ObjectContainer.setSizePolicy(sizePolicy)
        self.verticalLayout_2 = QtGui.QVBoxLayout(ObjectContainer)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.header = QtGui.QWidget(ObjectContainer)
        self.header.setObjectName("header")
        self.horizontalLayout = QtGui.QHBoxLayout(self.header)
        self.horizontalLayout.setSpacing(1)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton = QtGui.QPushButton(self.header)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.verticalLayout_2.addWidget(self.header)
        self.body = QtGui.QWidget(ObjectContainer)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.body.sizePolicy().hasHeightForWidth())
        self.body.setSizePolicy(sizePolicy)
        self.body.setObjectName("body")
        self.verticalLayout = QtGui.QVBoxLayout(self.body)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_2.addWidget(self.body)

        self.retranslateUi(ObjectContainer)
        QtCore.QMetaObject.connectSlotsByName(ObjectContainer)

    def retranslateUi(self, ObjectContainer):
        ObjectContainer.setWindowTitle(QtGui.QApplication.translate("ObjectContainer", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("ObjectContainer", "Push", None, QtGui.QApplication.UnicodeUTF8))

