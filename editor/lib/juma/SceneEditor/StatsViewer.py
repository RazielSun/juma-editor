#!/usr/bin/env python
import sys
import PySide
import os

from time import strftime

from PySide import QtCore, QtGui
from PySide.QtGui import QDockWidget

from juma.core 				import app, signals
from juma.moai.MOAIRuntime	import MOAILuaDelegate
from SceneEditor  			import SceneEditorModule
from ui.statsdock_ui 		import Ui_statsdock as Ui

##----------------------------------------------------------------##
def _getModulePath( path ):
	import os.path
	return os.path.dirname( __file__ ) + '/' + path

##----------------------------------------------------------------##
class StatsViewer( SceneEditorModule ):
	"""docstring for StatsViewer"""
	_name       = 'stats_viewer'
	_dependency = ['qt', 'moai', 'scene_editor']

	def __init__(self):
		super(StatsViewer, self).__init__()
		self.runtime = None
		self.delegate = MOAILuaDelegate( self, autoReload = False )
		self.scriptPath = None
		self.scriptEnv = None
		self.ready = False

	def getRuntime(self):
		if self.runtime is None:
			self.runtime = self.affirmModule('moai')
		return self.runtime
	
	def onLoad( self ):
		self.window = self.requestDockWindow( 'StatsViewer',
			title     = 'Stats',
			dock      = 'right',
		)
		
		ui = Ui()
		self.ui =  ui
		self.ui.setupUi(self.window)

		self.window.setStayOnTop( True )
		self.window.setObjectName( 'StatsViewer' )
		self.window.hide()

		self.loadScript( _getModulePath('StatsViewer.lua') )

		signals.connect( 'moai.prepare_clean', self.onMoaiPrepareClean )
		signals.connect( 'moai.ready', self.onMoaiReady )

		self.timer = QtCore.QTimer( self.window )
		self.timer.timeout.connect( self.onUpdateStats )

	def onStop( self ):
		self.stopTimer()

	def loadScript( self, scriptPath, env = None, **kwargs ):
		self.scriptPath = scriptPath
		self.scriptEnv  = env
		self.setupEnv()

	def setupEnv(self):
		env = {}			
		if self.scriptEnv:
			env.update( self.scriptEnv )
		self.delegate.load( self.scriptPath, env )

	def startTimer(self):
		if self.ready: return
		self.delegate.safeCall( 'onStart' )
		self.ready = True
		self.timer.start(600)

	def stopTimer(self):
		if self.ready == False: return
		self.ready = False
		self.timer.stop()
		self.delegate.safeCall( 'onStop' )

	def onMoaiPrepareClean(self):
		self.stopTimer()

	def onMoaiReady(self):
		self.setupEnv()
		self.startTimer()

	def onUpdateStats(self):
		if self.ready:
			fps, drawcalls, luaCount, luaMem, textureMem, actionTree, nodeMgr, sim, render = self.delegate.safeCall( 'onStats' )
			self.ui.valueFps.setText(str(fps))
			self.ui.valueDrawCalls.setText(str(drawcalls))
			self.ui.valueLuaCount.setText( '{:,}'.format(int(luaCount)) )
			self.ui.valueLuaMemory.setText( '{:,}'.format(int(luaMem)) )
			self.ui.valeuTextureMemory.setText( '{:,}'.format(int(textureMem)) )
			self.ui.valueNodeMgr.setText(str(actionTree))
			self.ui.valueActionTree.setText(str(nodeMgr))
			self.ui.valueSim.setText(str(sim))
			self.ui.valueRender.setText(str(render))

##----------------------------------------------------------------##

StatsViewer().register()
