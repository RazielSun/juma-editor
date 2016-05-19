#!/usr/bin/env python

from PySide import QtGui, QtCore
from PySide.QtCore import Qt

from juma.core.ModelManager import *
from juma.moai.bridge import luaTypeToPyType

from PropertyEditor import FieldEditor, registerSimpleFieldEditorFactory
from juma.SearchView import requestArrayView

##----------------------------------------------------------------##
class ArrayFieldButton( QtGui.QToolButton ):
	def sizeHint( self ):
		return QtCore.QSize( 20, 20)

##----------------------------------------------------------------##
class ArrayFieldEditor( FieldEditor ):
	def setTarget( self, parent, field ):
		super( ArrayFieldEditor, self ).setTarget( parent, field )
		t = field.getType()
		self.targetType    = t.itemType
		self.targetContext = None  #TODO
		self.value = None

	def get( self ):
		#TODO
		pass
		
	def set( self, value ):
		self.value = value
		if value:
			txt = '[ contains {} element(s) ]'.format(len(value)) # '[...]'
			self.button.setText( txt )
		else:
			self.button.setText( '[]' )
		
	def setValue( self, value ):
		self.set( value )
		self.notifyChanged( value )

	def initEditor( self, container ):
		self.button = ArrayFieldButton( container )
		self.button.setSizePolicy(
			QtGui.QSizePolicy.Expanding,
			QtGui.QSizePolicy.Expanding
			)
		self.button.setText( '[]' )
		if self.getOption( 'readonly', False ):
			self.button.setEnabled( False )
		self.button.clicked.connect( self.openArrayView )
		return self.button

	def openArrayView( self ):
		requestArrayView(
			context      	= 'scene',
			type         	= self.targetType,
			on_save 		= self.onSave,
			initial      	= self.value,
			)

	def onSave( self, value ):
		formatted = []
		frm = luaTypeToPyType(self.targetType)
		for v in value:
			data = frm(v)
			formatted.append(data)
		self.setValue( formatted )
		self.setFocus()

	def setFocus( self ):
		self.button.setFocus()

##----------------------------------------------------------------##

registerSimpleFieldEditorFactory( ArrayType, ArrayFieldEditor )
