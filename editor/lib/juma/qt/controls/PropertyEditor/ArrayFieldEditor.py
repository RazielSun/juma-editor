#!/usr/bin/env python

from PySide import QtGui, QtCore
from PySide.QtCore import Qt

from juma.core.ModelManager import *

from PropertyEditor import FieldEditor, registerSimpleFieldEditorFactory

from ui.array_view_container_ui			import Ui_ArrayViewContainer as ArrayViewContainer

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
			self.button.setText( '[...]' )
		else:
			self.button.setText( '[]' )
		
	def setValue( self, value ):
		self.set( value )
		self.notifyChanged( value )

	def initEditor( self, container ):
		self.button = CollectionFieldButton( container )
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
		pass

	# def openSearchView( self ):
	# 	print("openSearchView", self.targetType, self.value)
	# 	requestSearchView( 
	# 		context      = 'scene',
	# 		type         = self.targetType,
	# 		multiple_selection = True,
	# 		on_selection = self.onSearchSelection,
	# 		on_cancel    = self.onSearchCancel,
	# 		initial      = self.value
	# 		)

	# def onSearchSelection( self, value ):
	# 	self.setValue( value )
	# 	self.setFocus()

	# def onSearchCancel( self ):
	# 	self.setFocus()

	def setFocus( self ):
		self.button.setFocus()

##----------------------------------------------------------------##

registerSimpleFieldEditorFactory( ArrayType, ArrayFieldEditor )
