#!/usr/bin/env python

import os.path

from PySide import QtGui, QtCore
from PySide.QtCore import Qt

from juma.core import  *
from juma.MainEditor.Introspector 		import IntrospectorObject, CommonIntrospectorObject
from FrameworkEditor					import registerFrameworkEditorBuilder
from juma.qt.controls.PropertyEditor 	import PropertyEditor
from juma.qt.helpers 					import addWidgetWithLayout, repolishWidget
from juma.qt.IconCache               	import getIcon

##----------------------------------------------------------------##
def getModulePath( path ):
	return os.path.dirname( __file__ ) + '/' + path

##----------------------------------------------------------------##
## Framework Custom Inspector Builder
##----------------------------------------------------------------##
class FrameworkObjectMixin(object):
	def __init__(self):
		super(FrameworkObjectMixin, self).__init__()

	def initFoldState( self ):
		self.getContainer().foldChanged.connect( self.onFoldChanged )

	def onFoldChanged( self, folded ):
		self.getTarget()['__foldState'] = folded

class UIWidgetEditorObject(FrameworkObjectMixin, CommonIntrospectorObject):
	def __init__(self):
		super(UIWidgetEditorObject, self).__init__()

	def initWidget(self, container, objectContainer):
		self.property = PropertyEditor( container )
		self.property.setContext( 'main_editor' )		
		self.property.propertyChanged.connect( self.onPropertyChanged )		
		self.initFoldState()
		return self.property

	def needRefreshForContext(self, context = None):
		if context == "translation":
			self.property.refreshField( 'loc' )
			self.property.refreshField( 'rot' )
			self.property.refreshField( 'scl' )
			self.property.calculateField( 'anchorPos' )
			self.property.refreshField( 'anchorPos' )
			return True
		return False

	def onPropertyChanged( self, obj, id, value ):
		if id == 'name':
			signals.emit( 'entity.renamed', obj, value )
		elif id == 'sprite':
			self.property.refreshFieldState( 'size' )
		signals.emit( 'entity.modified', obj, 'introspector' )

##----------------------------------------------------------------##

registerFrameworkEditorBuilder( "UISprite", UIWidgetEditorObject )
registerFrameworkEditorBuilder( "UILabel", UIWidgetEditorObject )
registerFrameworkEditorBuilder( "UILabelSDF", UIWidgetEditorObject )
registerFrameworkEditorBuilder( "UIButtonColor", UIWidgetEditorObject )
registerFrameworkEditorBuilder( "UIButton", UIWidgetEditorObject )
registerFrameworkEditorBuilder( "UIWidget", UIWidgetEditorObject )
