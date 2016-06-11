# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'object_container.ui'
#
# Created: Sat Jun 11 12:39:53 2016
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_ObjectContainer(object):
    def setupUi(self, ObjectContainer):
        ObjectContainer.setObjectName("ObjectContainer")
        ObjectContainer.resize(249, 133)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ObjectContainer.sizePolicy().hasHeightForWidth())
        ObjectContainer.setSizePolicy(sizePolicy)
        self.mainLayout = QtGui.QVBoxLayout(ObjectContainer)
        self.mainLayout.setSpacing(0)
        self.mainLayout.setContentsMargins(5, 5, 5, 0)
        self.mainLayout.setObjectName("mainLayout")
        self.header = QtGui.QWidget(ObjectContainer)
        self.header.setObjectName("header")
        self.headerLayout = QtGui.QHBoxLayout(self.header)
        self.headerLayout.setSpacing(0)
        self.headerLayout.setContentsMargins(0, 0, 0, 0)
        self.headerLayout.setContentsMargins(0, 0, 0, 0)
        self.headerLayout.setObjectName("headerLayout")
        self.foldBtn = QtGui.QToolButton(self.header)
        self.foldBtn.setMaximumSize(QtCore.QSize(20, 20))
        self.foldBtn.setObjectName("foldBtn")
        self.headerLayout.addWidget(self.foldBtn)
        self.nameBtn = QtGui.QToolButton(self.header)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.nameBtn.sizePolicy().hasHeightForWidth())
        self.nameBtn.setSizePolicy(sizePolicy)
        self.nameBtn.setMaximumSize(QtCore.QSize(99999, 20))
        self.nameBtn.setObjectName("nameBtn")
        self.headerLayout.addWidget(self.nameBtn)
        self.menuBtn = QtGui.QToolButton(self.header)
        self.menuBtn.setMaximumSize(QtCore.QSize(20, 20))
        self.menuBtn.setObjectName("menuBtn")
        self.headerLayout.addWidget(self.menuBtn)
        self.mainLayout.addWidget(self.header)
        self.body = QtGui.QWidget(ObjectContainer)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.body.sizePolicy().hasHeightForWidth())
        self.body.setSizePolicy(sizePolicy)
        self.body.setObjectName("body")
        self.bodyLayout = QtGui.QVBoxLayout(self.body)
        self.bodyLayout.setSpacing(0)
        self.bodyLayout.setContentsMargins(0, 0, 0, 0)
        self.bodyLayout.setContentsMargins(0, 0, 0, 0)
        self.bodyLayout.setObjectName("bodyLayout")
        self.mainLayout.addWidget(self.body)

        self.retranslateUi(ObjectContainer)
        QtCore.QMetaObject.connectSlotsByName(ObjectContainer)

    def retranslateUi(self, ObjectContainer):
        ObjectContainer.setWindowTitle(QtGui.QApplication.translate("ObjectContainer", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.foldBtn.setText(QtGui.QApplication.translate("ObjectContainer", "+", None, QtGui.QApplication.UnicodeUTF8))
        self.nameBtn.setText(QtGui.QApplication.translate("ObjectContainer", "+", None, QtGui.QApplication.UnicodeUTF8))
        self.menuBtn.setText(QtGui.QApplication.translate("ObjectContainer", "+", None, QtGui.QApplication.UnicodeUTF8))

