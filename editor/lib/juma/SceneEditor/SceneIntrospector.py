import os.path

from PySide  import QtCore, QtGui, QtOpenGL
from PySide.QtCore import Qt, QSize

from juma.core 							import *
from juma.qt.controls.PropertyEditor 	import PropertyEditor
from SceneEditor             			import SceneEditorModule
from juma.qt.IconCache         			import getIcon

from ui.object_container_ui 			import Ui_ObjectContainer


##----------------------------------------------------------------##
def _getModulePath( path ):
	return os.path.dirname( __file__ ) + '/' + path

class ObjectContainer( QtGui.QWidget ):
	def __init__( self, *args ):
		super( ObjectContainer, self ).__init__( *args )
		self.ui = Ui_ObjectContainer()
		self.ui.setupUi( self )
		self.setSizePolicy( QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed )
		self.setAttribute( Qt.WA_NoSystemBackground, True )
		self.contextObject = None

		self.ui.nameBtn.setToolButtonStyle( Qt.ToolButtonTextBesideIcon )
		
		self.ui.nameBtn.setIcon( getIcon( 'grid' ) )
		self.ui.menuBtn.setIcon( getIcon( 'list' ) )
		self.ui.foldBtn.setIcon( getIcon( 'arrow_down' ) )

		self.ui.nameBtn.setIconSize( QSize( 16, 16 ) )
		self.ui.menuBtn.setIconSize( QSize( 16, 16 ) )
		self.ui.foldBtn.setIconSize( QSize( 16, 16 ) )

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

##----------------------------------------------------------------##
class IntrospectorObject( object ):
	def __init__(self):
		self.target = None

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
		self.header.setStyleSheet('font-size:13px')
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

		self.updateTimer = self.container.startTimer( 10, self.onUpdateTimer )
		self.updatePending = False

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

	def addObjectEditor( self, target, **option ):
		self.scroll.hide()
		typeId = ModelManager.get().getTypeId( target )
		if not typeId:
			self.scroll.show()
			return

		defaultEditorClass = option.get("editor_class", None)
		parent = app.getModule('introspector')
		editorBuilder = parent.getEditorBuilderByTypeId( typeId, defaultEditorClass )
		editor = editorBuilder()
		editor.targetTypeId = typeId
		self.editors.append( editor )
		container = ObjectContainer( self.body )
		
		editor.container = container
		widget = editor.initWidget( container.getBody(), container )
		container.setContextObject( target )

		if widget:
			container.addWidget( widget )

			model = ModelManager.get().getModel( target ) # FIXME
			# model = ModelManager.get().getModelFromTypeId( typeId )
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
			# cached = False
			# if editor.needCache():
			# 	cached = pushObjectEditorToCache( editor.targetTypeId, editor )
			# if not cached:
			# 	editor.unload()
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

	def onUpdateTimer(self):
		pass

##----------------------------------------------------------------##
def registerEditorBuilder( typeId, editorBuilder ):
	app.getModule('introspector').registerEditorBuilder( typeId, editorBuilder )

##----------------------------------------------------------------##
class SceneIntrospector( SceneEditorModule ):
	_name       = 'introspector'
	_dependency = [ 'qt', 'scene_editor' ]

	def __init__(self):
		super( SceneIntrospector, self ).__init__()
		self.instances      = []
		# self.instanceCache  = []
		self.activeInstance = None
		self.editorBuilderRegistry = {}

	def onLoad( self ):
		self.container = self.requestDockWindow('SceneIntrospector',
				title   = 'Introspector',
				dock    = 'left',
				minSize = (300,200)
		)
		self.requestInstance()
		# SIGNALS
		signals.connect( 'selection.changed', self.onSelectionChanged )

	def requestInstance(self):
		instance = IntrospectorInstance()
		instance.createWidget( self.container )
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

##----------------------------------------------------------------##

SceneIntrospector().register()