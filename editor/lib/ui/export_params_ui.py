# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'export_params.ui'
#
# Created: Sat Jun 11 12:39:54 2016
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_ExportParams(object):
    def setupUi(self, ExportParams):
        ExportParams.setObjectName("ExportParams")
        ExportParams.resize(300, 200)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ExportParams.sizePolicy().hasHeightForWidth())
        ExportParams.setSizePolicy(sizePolicy)
        ExportParams.setMinimumSize(QtCore.QSize(300, 200))
        self.formLayout = QtGui.QFormLayout(ExportParams)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.ExpandingFieldsGrow)
        self.formLayout.setRowWrapPolicy(QtGui.QFormLayout.DontWrapRows)
        self.formLayout.setContentsMargins(5, 5, 5, 5)
        self.formLayout.setObjectName("formLayout")
        self.perPixelLabel = QtGui.QLabel(ExportParams)
        self.perPixelLabel.setObjectName("perPixelLabel")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.perPixelLabel)
        self.perPixelEdit = QtGui.QLineEdit(ExportParams)
        self.perPixelEdit.setObjectName("perPixelEdit")
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.perPixelEdit)
        self.textureLabel = QtGui.QLabel(ExportParams)
        self.textureLabel.setObjectName("textureLabel")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.textureLabel)
        self.textureEdit = QtGui.QLineEdit(ExportParams)
        self.textureEdit.setObjectName("textureEdit")
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.textureEdit)

        self.retranslateUi(ExportParams)
        QtCore.QMetaObject.connectSlotsByName(ExportParams)

    def retranslateUi(self, ExportParams):
        ExportParams.setWindowTitle(QtGui.QApplication.translate("ExportParams", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.perPixelLabel.setText(QtGui.QApplication.translate("ExportParams", "Pixels", None, QtGui.QApplication.UnicodeUTF8))
        self.perPixelEdit.setText(QtGui.QApplication.translate("ExportParams", "256", None, QtGui.QApplication.UnicodeUTF8))
        self.textureLabel.setText(QtGui.QApplication.translate("ExportParams", "Texture", None, QtGui.QApplication.UnicodeUTF8))

