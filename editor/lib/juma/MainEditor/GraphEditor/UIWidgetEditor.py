#!/usr/bin/env python

import os.path

from PySide import QtGui, QtCore
from PySide.QtCore import Qt

from juma.core import  *
from juma.MainEditor.Introspector 		import IntrospectorObject, CommonIntrospectorObject, registerEditorBuilder
from juma.qt.controls.PropertyEditor 	import PropertyEditor
from juma.qt.helpers 					import addWidgetWithLayout, repolishWidget
from juma.qt.IconCache               	import getIcon

##----------------------------------------------------------------##
def getModulePath( path ):
	return os.path.dirname( __file__ ) + '/' + path

##----------------------------------------------------------------##
_frameworkInited = False
_frameworkEditorBuilders = {}

def registerFrameworkEditorBuilder( className, editorClass ):
	_frameworkEditorBuilders[ className ] = editorClass
	if _frameworkInited:
		# mockClass = _MOCK[ mockClassName ]
		registerEditorBuilder( className, editorClass )

def onFrameworkInited():
	global _frameworkInited
	_frameworkInited = True
	for className, editorClass in  _frameworkEditorBuilders.items():
		# mockClass = _MOCK[ mockClassName ]
		registerEditorBuilder( className, editorClass )

signals.connect( 'framework.init', onFrameworkInited )

##----------------------------------------------------------------##
## Framework Custom Inspector Builder
##----------------------------------------------------------------##
class FrameworkObjectMixin(object):
	def __init__(self):
		super(FrameworkEditorObjectMixin, self).__init__()

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

	def onPropertyChanged( self, obj, id, value ):
		if id == 'name':
			signals.emit( 'entity.renamed', obj, value )
		elif id == 'sprite':
			self.grid.refershFieldState( 'size' )
		elif id == 'loc':
			self.grid.refershFieldState( 'pos' )
		# elif id == 'layer':
		# 	signals.emit( 'entity.renamed', obj, value )
		# elif id == 'visible':
		# 	signals.emit( 'entity.visible_changed', obj )
		signals.emit( 'entity.modified', obj, 'introspector' )

##----------------------------------------------------------------##

registerFrameworkEditorBuilder( "UISprite", UIWidgetEditorObject )
registerFrameworkEditorBuilder( "UILabel", UIWidgetEditorObject )
registerFrameworkEditorBuilder( "UIButtonColor", UIWidgetEditorObject )
registerFrameworkEditorBuilder( "UIButton", UIWidgetEditorObject )
registerFrameworkEditorBuilder( "UIWidget", UIWidgetEditorObject )
