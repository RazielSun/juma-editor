import os.path

from PySide  import QtCore, QtGui, QtOpenGL

from juma.core 					import signals, app
from SceneEditor             	import SceneEditorModule



##----------------------------------------------------------------##
def _getModulePath( path ):
	return os.path.dirname( __file__ ) + '/' + path

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
		self.scroll = scroll = container.addWidget( QtGui.QScrollArea( container ) )
		self.body   = body   = QtGui.QWidget( container )
		self.header.setStyleSheet('font-size:13px')
		self.header.hide()
		self.scroll.verticalScrollBar().setStyleSheet('width:4px')
		scroll.setWidgetResizable( True )
		body.mainLayout = layout = QtGui.QVBoxLayout( body )
		layout.setSpacing(0)
		layout.setContentsMargins(0, 0, 0, 0)
		layout.addStretch()
		scroll.setWidget( body )

		self.updateTimer = self.container.startTimer( 10, self.onUpdateTimer )
		self.updatePending = False

	def onUpdateTimer(self):
		pass

##----------------------------------------------------------------##
class SceneIntrospector( SceneEditorModule ):
	_name       = 'introspector'
	_dependency = [ 'qt', 'scene_editor' ]

	def __init__(self):
		super( SceneIntrospector, self ).__init__()
		self.instances      = []
		# self.instanceCache  = []
		self.activeInstance = None
		self.objectEditorRegistry = {}

	def onLoad( self ):
		self.container = self.requestDockWindow('SceneIntrospector',
				title   = 'Introspector',
				dock    = 'left',
				minSize = (200,200)
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

	def onSelectionChanged( self, selection, key ):
		if key != 'scene': return
		# if not self.activeInstance: return
		# target = None
		# if isinstance( selection, list ):
		# 	target = selection
		# elif isinstance( selection, tuple ):
		# 	(target) = selection
		# else:
		# 	target=selection
		# self.activeInstance.setTarget(target) #first selection only?

##----------------------------------------------------------------##

SceneIntrospector().register()