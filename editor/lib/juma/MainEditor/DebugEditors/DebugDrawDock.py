

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

from ui.debugdock_ui 		import Ui_DebugDrawDock as Ui

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
class DebugDrawDock( MainEditorModule ):
	"""docstring for DebugDrawDock"""
	_name       = 'debug_draw_dock'
	_dependency = ['qt', 'moai', 'main_editor']

	def __init__(self):
		super(DebugDrawDock, self).__init__()
		self.runtime = None
		self.delegate = MOAILuaDelegate( self, autoReload = False )
		self.scriptPath = None
		self.scriptEnv = None
		self.ready = False

	def onLoad( self ):
		self.window = window = self.requestDockWindow( 'DebugDrawDock',
			title     = 'DebugDraw',
			dock      = 'right',
		)

		self.createSlots( window )
		
		self.ui = ui = Ui()
		self.ui.setupUi( self.window )

		self.window.setStayOnTop( True )
		self.window.setObjectName( 'DebugDrawDock' )
		self.window.hide()

		self.loadScript( _getModulePath('DebugDrawDock.lua') )

		floatValidator = PySide.QtGui.QDoubleValidator()
		floatValidator.setRange(0.0, 100.0)
		ui.partitionCellsWidth.setValidator(floatValidator)
		ui.partitionPaddedCellsWidth.setValidator(floatValidator)
		ui.propModelBoundsWidth.setValidator(floatValidator)
		ui.propWorldBoundsWidth.setValidator(floatValidator)
		ui.textBoxWidth.setValidator(floatValidator)
		ui.textBoxBaselinesWidth.setValidator(floatValidator)
		ui.textBoxLayoutWidth.setValidator(floatValidator)

		# SIGNALS
		signals.connect( 'moai.prepare_clean', self.onMoaiPrepareClean )
		signals.connect( 'moai.ready', self.onMoaiReady )

	def createSlots(self, window):
		for style in MOAIDebugDrawStyles:
			@QtCore.Slot(bool)
			def toggle(flag, style = style):
				self.toggleStyle(style, flag)

			@QtCore.Slot(str)
			def setWidth(width, style = style):
				self.setWidth(style, width)

			@QtCore.Slot()
			def pickColor(style = style):
				self.pickColor(style)

			setattr(window, 'toggle' + upperFirstLetter(style), toggle)
			setattr(window, 'setWidth' + upperFirstLetter(style), setWidth)
			setattr(window, 'pickColor' + upperFirstLetter(style), pickColor)

	def loadScript( self, scriptPath, env = None, **kwargs ):
		self.scriptPath = scriptPath
		self.scriptEnv  = env
		self.setupEnv()

	def setupEnv(self):
		env = {}			
		if self.scriptEnv:
			env.update( self.scriptEnv )
		self.delegate.load( self.scriptPath, env )

	def toggleStyle(self, styleName, flag):
		pass
		# self.updateDebugDrawValues(styleName)

	def setWidth(self, styleName, width):
		pass
		# self.updateDebugDrawValues(styleName)

	def pickColor(self, styleName):
		pass

	# SIGNALS
	def onMoaiPrepareClean(self):
		pass

	def onMoaiReady(self):
		self.setupEnv()

##----------------------------------------------------------------##

DebugDrawDock().register()
