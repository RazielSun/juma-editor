#!/usr/bin/env python

import os.path

from PySide  import QtCore, QtGui, QtOpenGL
from PySide.QtCore import Qt, QSize

from juma.core 							import *
from juma.qt.controls.PropertyEditor 	import PropertyEditor
from MainEditor             			import MainEditorModule
from juma.qt.IconCache         			import getIcon

from ui.object_container_ui 			import Ui_ObjectContainer

##----------------------------------------------------------------##
def _getModulePath( path ):
	return os.path.dirname( __file__ ) + '/' + path

##----------------------------------------------------------------##
_OBJECT_EDITOR_CACHE = {} 

def pushObjectEditorToCache( typeId, editor ):
	pool = _OBJECT_EDITOR_CACHE.get( typeId, None )
	if not pool:
		pool = []
		_OBJECT_EDITOR_CACHE[ typeId ] = pool
	editor.container.setUpdatesEnabled( False )
	pool.append( editor )
	return True

def popObjectEditorFromCache( typeId ):
	pool = _OBJECT_EDITOR_CACHE.get( typeId, None )
	if pool:
		editor = pool.pop()
		if editor:
			editor.container.setUpdatesEnabled( True )
		return editor

def clearObjectEditorCache( typeId ):
	if _OBJECT_EDITOR_CACHE.has_key( typeId ):
		del _OBJECT_EDITOR_CACHE[ typeId ]

##----------------------------------------------------------------##
class ObjectContainer( QtGui.QWidget ):
	foldChanged  = QtCore.Signal( bool )

	def __init__( self, *args ):
		super( ObjectContainer, self ).__init__( *args )
		self.ui = ui = Ui_ObjectContainer()
		ui.setupUi( self )
		self.setSizePolicy( QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed )
		self.setAttribute( Qt.WA_NoSystemBackground, True )
		self.contextObject = None
		self.folded = False
		self.toggleFold( False, True )

		ui.nameBtn.setToolButtonStyle( Qt.ToolButtonTextBesideIcon )
		ui.menuBtn.setVisible( False )
		
		# ui.nameBtn.setIcon( getIcon( 'grid' ) )
		ui.menuBtn.setIcon( getIcon( 'list' ) )
		ui.foldBtn.setIcon( getIcon( 'arrow_down' ) )

		ui.nameBtn.setIconSize( QSize( 16, 16 ) )
		ui.menuBtn.setIconSize( QSize( 16, 16 ) )
		ui.foldBtn.setIconSize( QSize( 16, 16 ) )

		ui.foldBtn.clicked.connect( lambda: self.toggleFold( None ) )
		ui.menuBtn.clicked.connect( lambda: self.openContextMenu() )
		ui.nameBtn.clicked.connect( lambda: self.toggleFold( None ) )

	def setContextObject( self, context ):
		self.contextObject = context

	def getBody( self ):
		return self.ui.body

	def getBodyLayout( self ):
		return self.ui.bodyLayout

	def addWidget(self, widget, **layoutOption):
		if isinstance( widget, list):
			for w in widget:
				self.addWidget( w, **layoutOption )
			return

		if layoutOption.get('fixed', False):
			widget.setSizePolicy(
				QtGui.QSizePolicy.Fixed,
				QtGui.QSizePolicy.Fixed
				)
		elif layoutOption.get('expanding', True):
			widget.setSizePolicy(
				QtGui.QSizePolicy.Expanding,
				QtGui.QSizePolicy.Expanding
				)		
		self.getBodyLayout().addWidget(widget)
		return widget

	def setTitle( self, title ):
		self.ui.nameBtn.setText( title )

	def toggleFold( self, folded = None, notify = True ):
		if folded == None:
			folded = not self.folded
		self.folded = folded
		if folded:
			self.ui.foldBtn.setIcon( getIcon( 'arrow_right' ) )
			self.ui.body.hide()
		else:
			self.ui.foldBtn.setIcon( getIcon( 'arrow_down' ) )
			self.ui.body.show()
		if notify:
			self.foldChanged.emit( self.folded )

	def openContextMenu( self ):
		if self.contextMenu:
			self.contextMenu.popUp( context = self.contextObject )

##----------------------------------------------------------------##
class IntrospectorObject( object ):
	def __init__(self):
		self.target = None
		self.parentIntrospector = None

	def getContainer( self ):
		return self.container

	def getInnerContainer( self ):
		return self.container.getBody()

	def getIntrospector( self ):
		return self.parentIntrospector

	def setTarget(self, target):
		self.target = target

	def getTarget(self):
		return self.target

	def initWidget( self, container, objectContainer ):
		pass

	def unload( self ):
		pass

	def needCache( self ):
		return True

	def setFocus( self ):
		pass

##----------------------------------------------------------------##
class CommonIntrospectorObject( IntrospectorObject ):
	def __init__(self):
		super(CommonIntrospectorObject, self).__init__()

	def initWidget(self, container, objectContainer):
		self.property = PropertyEditor( container )
		self.property.propertyChanged.connect( self.onPropertyChanged )
		return self.property

	def setTarget(self, target):
		self.target = target
		self.property.setTarget( target )

	def refresh( self ):
		self.property.refreshAll()

	def unload( self ):
		self.property.clear()
		self.target = None

	def onPropertyChanged( self, obj, id, value ):
		pass

##----------------------------------------------------------------##
class IntrospectorInstance(object):
	def __init__(self):
		self.target    = None
		self.container = None
		self.body      = None
		self.editors   = []

	def createWidget(self, container):
		self.container = container
		self.header = container.addWidget( QtGui.QLabel("QLabel Header Scene Introspector"), expanding=False )
		self.header.setStyleSheet('font-size:15px;padding: 5px; color:#eda900;')
		self.header.hide()
		self.scroll = scroll = container.addWidget( QtGui.QScrollArea( container ) )
		scroll.verticalScrollBar().setStyleSheet('width:4px;')
		scroll.setWidgetResizable( True )
		self.body = body = QtGui.QWidget( container )
		body.mainLayout = layout = QtGui.QVBoxLayout( body )
		scroll.setWidget( body )
		layout.setSpacing(0)
		layout.setContentsMargins(0, 0, 0, 0)
		layout.addStretch()

		self.updateTimer = self.container.startTimer( 0.1, self.onUpdateTimer )
		self.updatePending = False

	def addWidget( self, widget, **option ):
		self.scroll.hide()
		widget.setParent( self.body )
		count = self.body.mainLayout.count()
		self.body.mainLayout.insertWidget( count - 1, widget )
		self.scroll.show()

	def getTarget(self):
		return self.target

	def setTarget(self, t, forceRefresh = False ):
		if self.target == t and not forceRefresh: return

		if self.target:
			self.clear()
		
		if not t: 
			self.target=None
			return

		if len(t)>1:
			self.header.setText('Multiple object selected...')
			self.header.show()
			self.target = t[0] #TODO: use a multiple selection proxy as target
		else:
			self.target = t[0]

		self.addObjectEditor( self.target )

	def hasTarget( self, target ):
		if self.getObjectEditor( target ): return True
		return False

	def getObjectEditor( self, targetObject ):
		for editor in self.editors:
			if editor.getTarget() == targetObject: return editor
		return None

	def addObjectEditor( self, target, **option ):
		self.scroll.hide()
		typeId = ModelManager.get().getTypeId( target )
		if not typeId:
			self.scroll.show()
			return

		cachedEditor = popObjectEditorFromCache( typeId )
		if cachedEditor:
			editor = cachedEditor
			self.editors.append( editor )
			container = editor.container
			count = self.body.mainLayout.count()
			assert count>0
			self.body.mainLayout.insertWidget( count - 1, container )
			container.setContextObject( target )
			container.show()
		else:
			defaultEditorClass = option.get("editor_class", None)
			parent = app.getModule('introspector')
			editorBuilder = parent.getEditorBuilderByTypeId( typeId, defaultEditorClass )
			editor = editorBuilder()
			self.editors.append( editor )
			editor.targetTypeId = typeId
			container = ObjectContainer( self.body )
			editor.container = container
			container.setContextObject( target )
			widget = editor.initWidget( container.getBody(), container )
			if widget:
				container.addWidget( widget )
				model = ModelManager.get().getModelFromTypeId( typeId )
				if model:
					container.setTitle( model.name )
				count = self.body.mainLayout.count()
				assert count > 0
				self.body.mainLayout.insertWidget( count - 1, container )
			else:
				container.hide()

		editor.parentIntrospector = self
		editor.setTarget( target )
		size = self.body.sizeHint()
		size.setWidth( self.scroll.width() )
		self.body.resize( size )
		self.scroll.show()
		return editor

	def clear(self):
		for editor in self.editors:
			editor.container.setContextObject( None )
			cached = False
			if editor.needCache():
				cached = pushObjectEditorToCache( editor.targetTypeId, editor )
			if not cached:
				editor.unload()
			editor.target = None

		layout = self.body.mainLayout
		for count in reversed( range(layout.count()) ):
			child = layout.takeAt( count )
			w = child.widget()
			if w:
				w.setParent( None )
		layout.addStretch()
		
		self.target = None
		self.header.hide()
		self.editors = []

	def refresh(self, target = None):
		for editor in self.editors:
			if not target or editor.getTarget() == target:
				editor.refresh()

	def onUpdateTimer(self):
		if self.updatePending == True:
			self.updatePending = False
			self.refresh()

	def scheduleUpdate( self ):
		self.updatePending = True

##----------------------------------------------------------------##
def registerEditorBuilder( typeId, editorBuilder ):
	app.getModule('introspector').registerEditorBuilder( typeId, editorBuilder )

##----------------------------------------------------------------##
class Introspector( MainEditorModule ):
	_name       = 'introspector'
	_dependency = [ 'qt', 'main_editor' ]

	def __init__(self):
		super( Introspector, self ).__init__()
		self.instances      = []
		# self.instanceCache  = []
		self.activeInstance = None
		self.editorBuilderRegistry = {}

	def onLoad( self ):
		self.window = self.requestDockWindow('Introspector',
				title   = 'Inspector',
				dock    = 'left',
				minSize = (300,200)
		)
		self.requestInstance()
		# SIGNALS
		signals.connect( 'selection.changed', self.onSelectionChanged )
		signals.connect( 'entity.modified',   self.onEntityModified )

	def requestInstance(self):
		instance = IntrospectorInstance()
		instance.createWidget( self.window )
		self.instances.append( instance )
		if not self.activeInstance:
			self.activeInstance = instance
		return instance

	def getInstances(self):
		return self.instances

	# REGISTER CUSTOME EDITORS #
	def registerEditorBuilder( self, typeId, editorBuilder ):
		assert typeId, 'null typeid'
		self.editorBuilderRegistry[ typeId ] = editorBuilder

	def getEditorBuilderByTypeId( self, typeId, defaultClass = None ):
		while True:
			editorBuilder = self.editorBuilderRegistry.get( typeId, None )
			if editorBuilder: 
				return editorBuilder
			typeId = getSuperType( typeId )
			if not typeId:
				break

		if defaultClass:
			return defaultClass

		return CommonIntrospectorObject

	# CALLBACKS #
	def onSelectionChanged( self, selection, key ):
		if key != 'scene': return
		if not self.activeInstance: return
		target = None
		if isinstance( selection, list ):
			target = selection
		elif isinstance( selection, tuple ):
			(target) = selection
		else:
			target=selection
		self.activeInstance.setTarget(target) #first selection only?

	def onEntityModified( self, entity, context=None ):
		if context != 'introspector' :
			self.refresh( entity, context )

	def refresh( self, target = None, context = None ):
		for ins in self.instances:
			if not target or ins.hasTarget( target ):
				ins.scheduleUpdate()

##----------------------------------------------------------------##

Introspector().register()