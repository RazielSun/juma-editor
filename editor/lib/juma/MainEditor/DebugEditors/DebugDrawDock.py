

#!/usr/bin/env python
import sys
import PySide
import os

from time import strftime

from PySide import QtCore, QtGui
from PySide.QtGui import QDockWidget

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
	showChanged = QtCore.Signal( str, bool )
	styleChanged = QtCore.Signal( str, int, QtGui.QColor )

	def __init__(self, *args):
		super(DebugDrawItem, self).__init__( *args )
		self.ui = ui = ItemUi()
		ui.setupUi( self )

		self.name = 'DebugDrawItem'
		self.width = 1
		self.showed = False

		intValidator = QtGui.QIntValidator()
		intValidator.setRange(0, 100)
		ui.edit.setValidator(intValidator)
		ui.edit.setText( str(self.width) )

		self.colorBlock = block = ColorBlock( self )
		self.colorBlock.setMaximumSize( 30, 20 )
		ui.horizontalLayout.addWidget( block )

		ui.name.stateChanged.connect( self.changeShow )
		ui.edit.textChanged.connect( self.changeWidth )
		self.colorBlock.colorChanged.connect( self.changeColor )

	def setStyle( self, name ):
		self.name = name
		self.ui.name.setText( name )

	def changeShow( self, show ):
		self.showed = show == 2
		self.showChanged.emit( self.name, self.showed )

	def changeWidth( self, text ):
		self.width = int(text)
		self.styleChanged.emit( self.name, self.width, self.colorBlock.getColor() )

	def changeColor( self, color ):
		self.styleChanged.emit( self.name, self.width, self.colorBlock.getColor() )

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
		signals.connect( 'moai.prepare_clean', self.onMoaiPrepareClean )
		signals.connect( 'moai.ready', self.onMoaiReady )

	def createItems( self ):
		drawNames = self.delegate.safeCallMethod( 'debugDraw', 'getDrawNames' )
		for name in drawNames:
			item = self.items.get(name, None)
			if item is None:
				item = self.window.addWidget( DebugDrawItem() )
				item.setStyle( name )
				item.showChanged.connect( self.toggleStyle )
				item.styleChanged.connect( self.changeStyle )
				self.items[name] = item

	def loadScript( self, scriptPath, env = None, **kwargs ):
		self.scriptPath = scriptPath
		self.scriptEnv  = env
		self.setupEnv()

	def setupEnv(self):
		env = {}			
		if self.scriptEnv:
			env.update( self.scriptEnv )
		self.delegate.load( self.scriptPath, env )

		self.createItems()

	def toggleStyle(self, name, flag):
		self.delegate.safeCallMethod( 'debugDraw', 'setDrawFlag', name, flag )

	def changeStyle(self, name, width, color ):
		r, g, b, a = unpackQColor(color)
		self.delegate.safeCallMethod( 'debugDraw', 'setDrawStyle', name, width, r, g, b, a )

	# SIGNALS
	def onMoaiPrepareClean(self):
		pass

	def onMoaiReady(self):
		self.setupEnv()

##----------------------------------------------------------------##

DebugDrawDock().register()
