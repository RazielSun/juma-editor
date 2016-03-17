import os.path

from PySide                   import QtCore, QtGui, QtOpenGL
from PySide.QtCore            import Qt

from juma.core                	import signals, app
from juma.moai.MOAIRuntime import MOAILuaDelegate
from juma.qt.controls.GenericTreeWidget import GenericTreeWidget
from SceneEditor             	import SceneEditorModule



##----------------------------------------------------------------##
def getModulePath( path ):
	import os.path
	return os.path.dirname( __file__ ) + '/' + path

##----------------------------------------------------------------##
class SceneGraphEditor( SceneEditorModule ):
	_name = 'scenegraph_editor'
	_dependency = [ 'qt', 'moai', 'scene_editor' ]

	def __init__(self):
		super( SceneGraphEditor, self ).__init__()
		self.delegate = None

	def onLoad( self ):
		self.windowTitle = 'Scenegraph'
		self.window = self.requestDockWindow( 'SceneGraphEditor',
			title     = self.windowTitle,
			dock      = 'left',
			size      = (200,200),
			minSize   = (200,200),
			)

		self.tree = self.window.addWidget( 
				SceneGraphTreeWidget( 
					self.window,
					sorting  = True,
					editable = True,
					multiple_selection = True,
					drag_mode = 'internal'
				)
			)

		self.tree.module = self

		self.tool = self.addToolBar( 'scene_graph', self.window.addToolBar() )

		self.delegate = MOAILuaDelegate( self )
		self.delegate.load( getModulePath( 'SceneGraphEditor.lua' ) )

		self.addTool( 'scene_graph/create_group', label ='+ Group', icon = 'folder_plus' )
		self.addTool( 'scene_graph/create_entity', label ='+ Entity', icon = 'plus_mint' )
		self.addTool( 'scene_graph/destroy_item', label ='- Item', icon = 'minus' )

	def createGroup(self):
		pass

	def createEntity(self):
		pass

	def destroyItem(self):
		pass

	def onTool( self, tool ):
		name = tool.name
		if name == 'create_group':
			self.createGroup()

		elif name == 'create_entity':
			self.createEntity()

		elif name == 'destroy_item':
			self.destroyItem()

##----------------------------------------------------------------##

SceneGraphEditor().register()

##----------------------------------------------------------------##
class SceneGraphTreeWidget( GenericTreeWidget ):
	def __init__( self, *args, **kwargs ):
		super( SceneGraphTreeWidget, self ).__init__( *args, **kwargs )