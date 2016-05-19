# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'debug_draw_item.ui'
#
# Created: Thu May 19 15:06:53 2016
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_DebugDrawItem(object):
    def setupUi(self, DebugDrawItem):
        DebugDrawItem.setObjectName("DebugDrawItem")
        DebugDrawItem.resize(200, 30)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(DebugDrawItem.sizePolicy().hasHeightForWidth())
        DebugDrawItem.setSizePolicy(sizePolicy)
        DebugDrawItem.setMaximumSize(QtCore.QSize(16777215, 30))
        DebugDrawItem.setWindowTitle("")
        self.horizontalLayout = QtGui.QHBoxLayout(DebugDrawItem)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setContentsMargins(5, 5, 5, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.name = QtGui.QCheckBox(DebugDrawItem)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.name.sizePolicy().hasHeightForWidth())
        self.name.setSizePolicy(sizePolicy)
        self.name.setObjectName("name")
        self.horizontalLayout.addWidget(self.name)
        self.edit = QtGui.QLineEdit(DebugDrawItem)
        self.edit.setMaximumSize(QtCore.QSize(40, 20))
        self.edit.setObjectName("edit")
        self.horizontalLayout.addWidget(self.edit)

        self.retranslateUi(DebugDrawItem)
        QtCore.QMetaObject.connectSlotsByName(DebugDrawItem)

    def retranslateUi(self, DebugDrawItem):
        self.name.setText(QtGui.QApplication.translate("DebugDrawItem", "CheckBox", None, QtGui.QApplication.UnicodeUTF8))

