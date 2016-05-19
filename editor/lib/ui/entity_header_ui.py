# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'entity_header.ui'
#
# Created: Thu May 19 16:41:52 2016
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_EntityHeader(object):
    def setupUi(self, EntityHeader):
        EntityHeader.setObjectName("EntityHeader")
        EntityHeader.resize(387, 260)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(EntityHeader.sizePolicy().hasHeightForWidth())
        EntityHeader.setSizePolicy(sizePolicy)
        self.verticalLayout = QtGui.QVBoxLayout(EntityHeader)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.containerPrefab = QtGui.QWidget(EntityHeader)
        self.containerPrefab.setObjectName("containerPrefab")
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.containerPrefab)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setContentsMargins(5, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.labelPrefabPath = QtGui.QLabel(self.containerPrefab)
        self.labelPrefabPath.setMinimumSize(QtCore.QSize(100, 20))
        self.labelPrefabPath.setMaximumSize(QtCore.QSize(16777215, 20))
        self.labelPrefabPath.setObjectName("labelPrefabPath")
        self.horizontalLayout_2.addWidget(self.labelPrefabPath)
        self.buttonEdit = QtGui.QToolButton(self.containerPrefab)
        self.buttonEdit.setMinimumSize(QtCore.QSize(0, 20))
        self.buttonEdit.setMaximumSize(QtCore.QSize(16777215, 20))
        self.buttonEdit.setObjectName("buttonEdit")
        self.horizontalLayout_2.addWidget(self.buttonEdit)
        self.buttonGoto = QtGui.QToolButton(self.containerPrefab)
        self.buttonGoto.setMinimumSize(QtCore.QSize(0, 20))
        self.buttonGoto.setMaximumSize(QtCore.QSize(16777215, 20))
        self.buttonGoto.setObjectName("buttonGoto")
        self.horizontalLayout_2.addWidget(self.buttonGoto)
        self.buttonUnlink = QtGui.QToolButton(self.containerPrefab)
        self.buttonUnlink.setMinimumSize(QtCore.QSize(40, 20))
        self.buttonUnlink.setMaximumSize(QtCore.QSize(16777215, 20))
        self.buttonUnlink.setObjectName("buttonUnlink")
        self.horizontalLayout_2.addWidget(self.buttonUnlink)
        self.verticalLayout.addWidget(self.containerPrefab)

        self.retranslateUi(EntityHeader)
        QtCore.QMetaObject.connectSlotsByName(EntityHeader)

    def retranslateUi(self, EntityHeader):
        EntityHeader.setWindowTitle(QtGui.QApplication.translate("EntityHeader", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.labelPrefabPath.setText(QtGui.QApplication.translate("EntityHeader", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonEdit.setText(QtGui.QApplication.translate("EntityHeader", "edit", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonGoto.setText(QtGui.QApplication.translate("EntityHeader", "goto", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonUnlink.setText(QtGui.QApplication.translate("EntityHeader", "unlink", None, QtGui.QApplication.UnicodeUTF8))

