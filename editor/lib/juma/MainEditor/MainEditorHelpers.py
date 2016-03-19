#!/usr/bin/env python

import sys
import os

from PySide import QtCore, QtGui

from juma.core 			import app, signals
from juma.qt.IconCache 	import getIcon

class SizeComboBox( QtGui.QComboBox ):
	sizes = [
	dict( icon = 'macbook', name = 'Custom' ),
	dict( icon = 'iphone', width = 320, height = 480 ),
	dict( icon = 'iphone', width = 320, height = 568 ),
	dict( icon = 'iphone', width = 375, height = 667 ),
	dict( icon = 'iphone', width = 414, height = 736 ),
	dict( icon = 'ipad', width = 384, height = 512 ),
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
			signals.emitNow( 'scene.change_size', size )