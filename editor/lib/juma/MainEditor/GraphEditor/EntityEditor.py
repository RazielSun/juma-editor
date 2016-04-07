#!/usr/bin/env python

import os.path

from PySide import QtGui, QtCore
from PySide.QtCore import Qt

from juma.core import  *
from juma.MainEditor.Introspector 		import IntrospectorObject, CommonIntrospectorObject
from FrameworkEditor					import registerFrameworkEditorBuilder
from juma.qt.controls.PropertyEditor 	import PropertyEditor
from juma.qt.helpers 					import addWidgetWithLayout, repolishWidget
from juma.SearchView 					import requestSearchView, registerSearchEnumerator
from juma.qt.IconCache               	import getIcon

from ui.entity_header_ui				import Ui_EntityHeader

##----------------------------------------------------------------##
def getModulePath( path ):
	return os.path.dirname( __file__ ) + '/' + path

##----------------------------------------------------------------##
## Framework Custom Inspector Builder
##----------------------------------------------------------------##
class FrameworkEditorObjectMixin(object):
	def __init__(self):
		super(FrameworkEditorObjectMixin, self).__init__()

	#foldstate
	def initFoldState( self ):
		self.getContainer().foldChanged.connect( self.onFoldChanged )
	
	def restoreFoldState( self ):
		folded = self.getTarget()['__foldState'] or False
		self.getContainer().toggleFold( folded, False )

	def onFoldChanged( self, folded ):
		self.getTarget()['__foldState'] = folded

##----------------------------------------------------------------##
class EntityHeader( QtGui.QWidget ):
	def __init__(self, *args ):
		super(EntityHeader, self).__init__( *args )
		self.layout = layout = QtGui.QVBoxLayout( self )
		layout.setSpacing(0)
		layout.setContentsMargins(0, 0, 0, 0)
		layout.addStretch()
		# self.ui = ui = Ui_EntityHeader()
		# ui.setupUi( self )

	def uilayout( self ):
		return self.layout #self.ui.verticalLayout

class EntityEditorObject(FrameworkEditorObjectMixin, CommonIntrospectorObject):
	def __init__(self):
		super(EntityEditorObject, self).__init__()

	def initWidget(self, container, objectContainer):
		self.header = EntityHeader( container )
		self.property = PropertyEditor( self.header )
		self.header.uilayout().addWidget( self.property )
		self.property.setContext( 'main_editor' )

		self.property.propertyChanged.connect( self.onPropertyChanged )		
		# self.header.buttonEdit   .clicked .connect ( self.onEditProto )
		# self.header.buttonGoto   .clicked .connect ( self.onGotoProto )
		# self.header.buttonUnlink .clicked .connect ( self.onUnlinkProto )
		
		# self.initFieldContextMenu( self.property )
		self.initFoldState()
		# self.initAnimatorButton()

		return self.header

	def setTarget( self, target ):
		if not target.components: return
		introspector = self.getIntrospector()
		self.target = target
		self.property.setTarget( target )
		targetName = target.className(target)
		if targetName == 'Entity':
			self.buttonAddComponent = buttonAddComponent = QtGui.QToolButton()
			buttonAddComponent.setObjectName( 'ButtonIntrospectorAddComponent' )
			buttonAddComponent.setText( 'Add Component ...' )
			buttonAddComponent.setSizePolicy( QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed )
			buttonAddComponent.clicked.connect( self.onButtonAddComponent )
			introspector.addWidget( self.buttonAddComponent )
		self.restoreFoldState()

	def onButtonAddComponent( self ):
		requestSearchView( 
				info    = 'select component type to create',
				context = 'component_creation',
				# on_selection = lambda obj: 
					# app.doCommand( 'scene_editor/create_component', name = obj )
				)

	def onPropertyChanged( self, obj, id, value ):
		# if _MOCK.markProtoInstanceOverrided( obj, id ):
		# 	self.property.refershFieldState( id )
		if id == 'name':
			signals.emit( 'entity.renamed', obj, value )
		elif id == 'sprite':
			self.property.refershFieldState( 'size' )
		elif id == 'loc':
			self.property.refershFieldState( 'pos' )
		# elif id == 'layer':
		# 	signals.emit( 'entity.renamed', obj, value )
		# elif id == 'visible':
		# 	signals.emit( 'entity.visible_changed', obj )
		signals.emit( 'entity.modified', obj, 'introspector' )

##----------------------------------------------------------------##

registerFrameworkEditorBuilder( "Entity", EntityEditorObject )
