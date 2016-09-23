#!/usr/bin/env python

import sys
import os

from PySide import QtCore, QtGui

from juma.core 			import app, signals
from juma.qt.IconCache 	import getIcon

##----------------------------------------------------------------##
class SizeComboBox( QtGui.QComboBox ):
	sizeChanged = QtCore.Signal( int, int )

	sizes = [
	dict( icon = 'macbook', name = 'Custom' ),
	dict( icon = 'macbook', width = 600, height = 400 ),
	dict( icon = 'macbook', width = 640, height = 480 ),
	dict( icon = 'iphone', width = 320, height = 480 ),
	dict( icon = 'iphone_h', width = 480, height = 320 ),
	dict( icon = 'iphone', width = 320, height = 568 ),
	dict( icon = 'iphone_h', width = 568, height = 320 ),
	dict( icon = 'iphone', width = 375, height = 667 ),
	dict( icon = 'iphone_h', width = 667, height = 375 ),
	dict( icon = 'iphone', width = 414, height = 736 ),
	dict( icon = 'iphone_h', width = 736, height = 414 ),
	dict( icon = 'ipad', width = 384, height = 512 ),
	dict( icon = 'ipad_h', width = 512, height = 384 ),
	dict( icon = 'ipad', width = 768, height = 1024 ),
	dict( icon = 'ipad_h', width = 1024, height = 768 ),
	]

	def __init__( self, parent ):
		super( SizeComboBox, self ).__init__( parent )

		self.setIconSize(QtCore.QSize(16,16))
		# self.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
		# self.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToMinimumContentsLengthWithIcon)

		self.createSizes()

		self.currentIndexChanged.connect(self.onSizeChanged)

	def createSizes(self):
		name = None
		for size in self.sizes:
			if 'name' in size:
				name = size['name']
			elif 'width' in size and 'height' in size:
				name = '{} x {}'.format(size['width'], size['height'])
			self.addItem(getIcon(size['icon']), name)

	def findSize(self, width, height):
		self.setCurrentIndex(0)
		for index, size in enumerate(self.sizes):
			if 'width' in size and 'height' in size:
				if size['width'] == width and size['height'] == height:
					self.setCurrentIndex(index)
					break

	def findSizeObj(self, obj):
		if obj and obj.width and obj.height:
			self.findSize( obj.width(), obj.height() )

	def onSizeChanged(self, index):
		size = self.sizes[index]
		if 'width' in size and 'height' in size:
			self.sizeChanged.emit( int(size['width']), int(size['height']) )

##----------------------------------------------------------------##
class ToolSizeWidget( QtGui.QWidget ):
	valuesChanged = QtCore.Signal( int, int )

	def __init__( self, parent ):
		super( ToolSizeWidget, self ).__init__( parent )
		self.setMaximumSize(80, 30)
		self.mainLayout = layout = QtGui.QHBoxLayout( self )
		layout.setSpacing(3)
		layout.setContentsMargins(0, 0, 0, 0)
		layout.addStretch()

		self.valueX = 320
		self.valueY = 480

		intValidator = QtGui.QIntValidator()
		# floatValidator.setRange(0.0, 100.0)
		
		self.xEdit = self.createEdit()
		self.yEdit = self.createEdit()

		self.xEdit.setValidator( intValidator )
		self.yEdit.setValidator( intValidator )

		self.xEdit.textChanged.connect( self.valueChangedX )
		self.yEdit.textChanged.connect( self.valueChangedY )

		self.setup()

	def createEdit( self ):
		edit = QtGui.QLineEdit( self )
		edit.setMaximumSize( 40, 20 )
		self.mainLayout.addWidget( edit )
		return edit

	def setup( self ):
		self.xEdit.setText( '{}'.format(self.valueX) )
		self.yEdit.setText( '{}'.format(self.valueY) )

	def setValues( self, x, y ):
		self.valueX = x
		self.valueY = y
		self.setup()

	def valueChangedX( self, text ):
		if text =='':
			text = '0'
		self.valueX = int(text)
		self.valuesChanged.emit( self.valueX, self.valueY )

	def valueChangedY( self, text ):
		if text =='':
			text = '0'
		self.valueY = int(text)
		self.valuesChanged.emit( self.valueX, self.valueY )

##----------------------------------------------------------------##
class ToolCoordWidget( ToolSizeWidget ):
	gotoSignal = QtCore.Signal( int, int )

	def __init__( self, parent ):
		super( ToolCoordWidget, self ).__init__( parent )
		self.setMaximumSize(100, 30)
		self.button = btn = QtGui.QToolButton( self )
		btn.setIcon( getIcon('gotopoint') )
		btn.setMaximumSize( 20, 20 )
		self.mainLayout.addWidget( btn )

		self.valueX = 0
		self.valueY = 0

		self.setup()

		btn.clicked.connect( self.btnClicked )

	def btnClicked( self ):
		self.gotoSignal.emit( self.valueX, self.valueY )

	