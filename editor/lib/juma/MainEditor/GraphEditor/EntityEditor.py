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
class FrameworkEditorObjectMixin(object):
	def __init__(self):
		super(FrameworkEditorObjectMixin, self).__init__()

class EntityEditorObject(FrameworkEditorObjectMixin, CommonIntrospectorObject):
	def __init__(self):
		super(EntityEditorObject, self).__init__()

	def initWidget( self, container, objectContainer ):
		# self.header = EntityHeader( container )
		# self.property = PropertyEditor( self.header )
		self.property = PropertyEditor( container )
		# self.header.layout().addWidget( self.grid )
		self.property.setContext( 'main_editor' )		

		self.property.propertyChanged.connect( self.onPropertyChanged )		
		# self.header.buttonEdit   .clicked .connect ( self.onEditProto )
		# self.header.buttonGoto   .clicked .connect ( self.onGotoProto )
		# self.header.buttonUnlink .clicked .connect ( self.onUnlinkProto )
		
		# self.initFieldContextMenu( self.grid )
		# self.initFoldState()
		# self.initAnimatorButton()

		return self.property
		# return self.header

	def onPropertyChanged( self, obj, id, value ):
		# if _MOCK.markProtoInstanceOverrided( obj, id ):
		# 	self.grid.refershFieldState( id )
		if id == 'name':
			signals.emit( 'entity.renamed', obj, value )
		# elif id == 'layer':
		# 	signals.emit( 'entity.renamed', obj, value )
		# elif id == 'visible':
		# 	signals.emit( 'entity.visible_changed', obj )
		signals.emit( 'entity.modified', obj, 'introspector' )

##----------------------------------------------------------------##

registerFrameworkEditorBuilder( "Entity", EntityEditorObject )
