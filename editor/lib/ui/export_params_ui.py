# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'export_params.ui'
#
# Created: Fri Jun 17 13:29:29 2016
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
        self.exportParamsLayout = QtGui.QFormLayout(ExportParams)
        self.exportParamsLayout.setFieldGrowthPolicy(QtGui.QFormLayout.ExpandingFieldsGrow)
        self.exportParamsLayout.setRowWrapPolicy(QtGui.QFormLayout.DontWrapRows)
        self.exportParamsLayout.setContentsMargins(5, 5, 5, 5)
        self.exportParamsLayout.setObjectName("exportParamsLayout")
        self.perPixelLabel = QtGui.QLabel(ExportParams)
        self.perPixelLabel.setObjectName("perPixelLabel")
        self.exportParamsLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.perPixelLabel)
        self.perPixelEdit = QtGui.QLineEdit(ExportParams)
        self.perPixelEdit.setObjectName("perPixelEdit")
        self.exportParamsLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.perPixelEdit)
        self.textureLabel = QtGui.QLabel(ExportParams)
        self.textureLabel.setObjectName("textureLabel")
        self.exportParamsLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.textureLabel)
        self.textureEdit = QtGui.QLineEdit(ExportParams)
        self.textureEdit.setObjectName("textureEdit")
        self.exportParamsLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.textureEdit)
        self.exportNameEdit = QtGui.QLineEdit(ExportParams)
        self.exportNameEdit.setObjectName("exportNameEdit")
        self.exportParamsLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.exportNameEdit)
        self.exportAnimEdit = QtGui.QLineEdit(ExportParams)
        self.exportAnimEdit.setObjectName("exportAnimEdit")
        self.exportParamsLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.exportAnimEdit)
        self.exportNameLabel = QtGui.QLabel(ExportParams)
        self.exportNameLabel.setObjectName("exportNameLabel")
        self.exportParamsLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.exportNameLabel)
        self.exportAnimLabel = QtGui.QLabel(ExportParams)
        self.exportAnimLabel.setObjectName("exportAnimLabel")
        self.exportParamsLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.exportAnimLabel)

        self.retranslateUi(ExportParams)
        QtCore.QMetaObject.connectSlotsByName(ExportParams)

    def retranslateUi(self, ExportParams):
        ExportParams.setWindowTitle(QtGui.QApplication.translate("ExportParams", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.perPixelLabel.setText(QtGui.QApplication.translate("ExportParams", "Pixels", None, QtGui.QApplication.UnicodeUTF8))
        self.perPixelEdit.setText(QtGui.QApplication.translate("ExportParams", "256", None, QtGui.QApplication.UnicodeUTF8))
        self.textureLabel.setText(QtGui.QApplication.translate("ExportParams", "Texture", None, QtGui.QApplication.UnicodeUTF8))
        self.exportNameLabel.setText(QtGui.QApplication.translate("ExportParams", "Export Name", None, QtGui.QApplication.UnicodeUTF8))
        self.exportAnimLabel.setText(QtGui.QApplication.translate("ExportParams", "Export Anim", None, QtGui.QApplication.UnicodeUTF8))

