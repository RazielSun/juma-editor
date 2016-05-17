

#!/usr/bin/env python
import sys
import PySide
import os

from time import strftime

from PySide import QtCore, QtGui
from PySide.QtCore 	import Qt
from PySide.QtGui 	import QDockWidget

from juma.core 					import app, signals
from juma.moai.MOAIRuntime		import MOAILuaDelegate
from juma.MainEditor.MainEditor import MainEditorModule
from juma.qt.helpers 			import QColorF, unpackQColor
from juma.qt.controls.PropertyEditor.ColorFieldEditor import ColorBlock

from ui.debug_draw_item_ui 		import Ui_DebugDrawItem as ItemUi

##----------------------------------------------------------------##
def _getModulePath( path ):
	import os.path
	return os.path.dirname( __file__ ) + '/' + path

##----------------------------------------------------------------##
MOAIDebugDrawStyles = [
    'partitionCells',
    'partitionPaddedCells',
    'propModelBounds',
    'propWorldBounds',
    'textBox',
    'textBoxBaselines',
    'textBoxLayout'
]

def upperFirstLetter(s):
	return s[0].upper() + s[1:]

##----------------------------------------------------------------##
class DebugDrawItem( QtGui.QWidget ):
	styleChanged = QtCore.Signal( str, bool, int, QtGui.QColor )

	def __init__(self, *args):
		super(DebugDrawItem, self).__init__( *args )
		self.ui = ui = ItemUi()
		ui.setupUi( self )

		self.name = 'DebugDrawItem'
		self.width = 1
		self.showed = False
		self.color = QColorF( 1,1,1 )

		intValidator = QtGui.QIntValidator()
		intValidator.setRange(0, 100)
		ui.edit.setValidator(intValidator)

		self.colorBlock = block = ColorBlock( self )
		self.colorBlock.setMaximumSize( 20, 20 )
		ui.horizontalLayout.addWidget( block )

		ui.name.stateChanged.connect( self.changeShow )
		ui.edit.textChanged.connect( self.changeWidth )
		self.colorBlock.colorChanged.connect( self.changeColor )

		self.updateParams()

	def setStyle( self, name ):
		self.name = name
		self.ui.name.setText( name )

	def changeShow( self, show ):
		self.showed = show == Qt.Checked
		self.styleChanged.emit( self.name, self.showed, self.width, self.color )

	def changeWidth( self, text ):
		self.width = int(text)
		self.styleChanged.emit( self.name, self.showed, self.width, self.color )

	def changeColor( self, color ):
		self.color = self.colorBlock.getColor()
		self.styleChanged.emit( self.name, self.showed, self.width, self.color )

	def setConfig( self, config ):
		self.showed = config.get("state", False)
		self.width = config.get("width", 1)
		color = config.get("color", (1,1,1))
		(r,g,b) = color
		self.color = QColorF( r,g,b )
		self.updateParams()

	def updateParams( self ):
		self.setCheck( self.showed )
		self.ui.edit.setText( str(self.width) )
		self.colorBlock.setColor( self.color )

	def uncheck( self ):
		self.setCheck( False )

	def setCheck( self, state ):
		self.ui.name.setCheckState( state and Qt.Checked or Qt.Unchecked )

##----------------------------------------------------------------##
class DebugDrawDock( MainEditorModule ):
	"""docstring for DebugDrawDock"""
	_name       = 'debug_draw_dock'
	_dependency = ['qt', 'moai', 'main_editor']

	def __init__(self):
		super(DebugDrawDock, self).__init__()
		self.delegate = MOAILuaDelegate( self, autoReload = False )
		self.scriptPath = None
		self.scriptEnv = None
		self.isReady = False
		self.projectLoaded = False
		
		self.config_name = "debug_draw_config"
		self.config = {}

		self.items = {}

	def onLoad( self ):
		self.window = window = self.requestDockWindow( 'DebugDrawDock',
			title     = 'DebugDraw',
			dock      = 'right',
			minSize   = ( 200, 200 ),
		)

		self.window.setStayOnTop( True )
		self.window.setObjectName( 'DebugDrawDock' )
		self.window.hide()

		self.loadScript( _getModulePath('DebugDrawDock.lua') )

		# SIGNALS
		signals.connect( 'project.load', 		self.onProjectLoad )
		signals.connect( 'moai.prepare_clean', 	self.onMoaiPrepareClean )
		signals.connect( 'moai.ready', 			self.onMoaiReady )

	def updateItems( self ):
		drawNames = self.delegate.safeCallMethod( 'debugDraw', 'getDrawNames' )
		for name in drawNames:
			item = self.items.get(name, None)

			if item is None:
				item = self.window.addWidget( DebugDrawItem() )
				item.setStyle( name )
				item.styleChanged.connect( self.changeStyle )
				self.items[name] = item

			if item:
				config = self.getConfigByName( name )
				item.setConfig( config )

	def loadScript( self, scriptPath, env = None, **kwargs ):
		self.scriptPath = scriptPath
		self.scriptEnv  = env
		self.setupEnv()

	def setupEnv(self):
		env = {}			
		if self.scriptEnv:
			env.update( self.scriptEnv )
		self.delegate.load( self.scriptPath, env )

	def changeStyle(self, name, state, width, color):
		if self.isReady:
			self.updateConfigs( name, state, width, color )
			self.delegate.safeCallMethod( 'debugDraw', 'setDrawFlag', name, state )
			if state:
				r, g, b, a = unpackQColor(color)
				self.delegate.safeCallMethod( 'debugDraw', 'setDrawStyle', name, width, r, g, b, a )

	##----------------------------------------------------------------##
	def saveConfig( self ):
		proj = self.getProject()
		if proj:
			proj.setConfig( self.config_name, self.config )
			proj.saveConfig()

	def updateConfigs( self, name, state, width, color ):
		config = self.getConfigByName( name )
		config['state'] = state
		config['width'] = width
		r, g, b, a = unpackQColor(color)
		config['color'] = (r,g,b)

	def getConfigByName( self, name ):
		config = self.config.get(name, None)
		if config is None:
			config = dict( state=False, width=1, color=(1,1,1) )
			self.config[name] = config
		return config

	##----------------------------------------------------------------##
	def onMoaiPrepareClean(self):
		self.isReady = False

		for item in self.items.values():
			item.uncheck()

	def onMoaiReady(self):
		self.setupEnv()

		self.isReady = True
		if self.projectLoaded:
			self.updateItems()

	def onProjectLoad( self, project ):
		self.config = project.getConfig( self.config_name, None )
		if self.config is None:
			self.config = {}
			self.saveConfig()

		self.projectLoaded = True
		if self.isReady:
			self.updateItems()

##----------------------------------------------------------------##

DebugDrawDock().register()
