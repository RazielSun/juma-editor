#!/usr/bin/env python
import sys
import PySide
import os

from time import strftime

from PySide import QtCore, QtGui
from PySide.QtGui import QDockWidget

from colorama import Fore, Back, Style

from juma.core import app, signals
from SceneEditor  import SceneEditorModule
from ui.statsdock_ui import Ui_statsdock as Ui

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
		super(GamePreview, self).__init__()
		self.statsFunc = None
		self.startFunc = None
		self.stopFunc = None

	def getRuntime(self):
		return self.affirmModule('moai')
	
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

		self.timer = self.window.addTimer( self.onUpdateStats )

		# signals.connect( 'scene.start', self.onSceneStarted )
		# signals.connect( 'scene.stop', self.onSceneStoped )
		# signals.connect( 'scene.pause', self.onScenePaused )
		# signals.connect( 'scene.open_source', self.onSceneSourceOpened )
		# signals.connect( 'scene.pre_open_source', self.onSceneSourcePreOpened )

	def onStop( self ):
		self.stopTimer()

	def startTimer(self):
		self.timer.start(600)
		if self.statsFunc:
			self.statsFunc()
		if self.startFunc:
			self.startFunc()

	def stopTimer(self):
		self.timer.stop()
		if self.stopFunc:
			self.stopFunc()
		self.statsFunc = None
		self.startFunc = None
		self.stopFunc = None
		self._setuped = False

	def setLuaState( self, lua ):
		self.statsFunc = lua.eval("""function()
			local fps = MOAISim.getPerformance()
			local drawcalls = MOAIGfxDevice.getFrameBuffer():getPerformanceDrawCount()
			local luaCount = MOAISim.getLuaObjectCount()
			local mem = MOAISim.getMemoryUsage()
			local lua, texture = mem.lua, mem.texture
			local node = STATS and STATS.nodeMgr or 0
			local action = STATS and STATS.actionTree or 0
			local sim = STATS and STATS.simTime or 0
			local render = STATS and STATS.renderTime or 0
			return math.round(fps, 0.1), drawcalls, luaCount, lua, texture, 
				math.round(node, 0.01), math.round(action, 0.01), math.round(sim, 0.01), math.round(render, 0.01)
		end""")

		self.startFunc = lua.eval("""function()
            STATS = {}
            STATS.thread = MOAICoroutine.new()

            local nIdx = 0
            local node = {0}
            local action = {0}
            local sim = {0}
            local render = {0}
            local buffer = 10
            STATS.thread:run(function()
                while true do
                    local _, a, n, s, r = MOAISim.getPerformance()
                    nIdx = (nIdx + 1) % buffer
                    action[nIdx + 1] = a
                    node[nIdx + 1] = n
                    sim[nIdx + 1] = s
                    render[nIdx + 1] = r
                    
                    local nodeMgrTime = 0
                    local actionTreeTime = 0
                    local simTime = 0
                    local renderTime = 0
                    for i = 1, #action do
                        nodeMgrTime = nodeMgrTime + node[i]
                        actionTreeTime = actionTreeTime + action[i]
                        simTime = simTime + sim[i]
                        renderTime = renderTime + render[i]
                    end
                    STATS.nodeMgr = 1000 * nodeMgrTime / buffer
                    STATS.actionTree = 1000 * actionTreeTime / buffer
                    STATS.simTime = 1000 * simTime / buffer
                    STATS.renderTime = 1000 * renderTime / buffer
                    coroutine.yield()
                end
            end)
		end""")

		self.stopFunc = lua.eval("""function()
            if STATS and STATS.thread then
                STATS.thread:stop()
                STATS.thread = nil
            end
		end""")

		self._setuped = True

	def onUpdateStats(self):
		if self.statsFunc and self._setuped:
			fps, drawcalls, luaCount, luaMem, textureMem, actionTree, nodeMgr, sim, render = self.statsFunc()
			self.ui.valueFps.setText(str(fps))
			self.ui.valueDrawCalls.setText(str(drawcalls))
			self.ui.valueLuaCount.setText( '{:,}'.format(int(luaCount)) )
			self.ui.valueLuaMemory.setText( '{:,}'.format(int(luaMem)) )
			self.ui.valeuTextureMemory.setText( '{:,}'.format(int(textureMem)) )
			self.ui.valueNodeMgr.setText(str(actionTree))
			self.ui.valueActionTree.setText(str(nodeMgr))
			self.ui.valueSim.setText(str(sim))
			self.ui.valueRender.setText(str(render))

	def onSceneStarted( self, sceneId ):
		# print("Scene Started: {}   current: {}".format(sceneId, self._sceneId))
		if self._sceneId == -1 and sceneId != -1:
			self._sceneId = sceneId
			moai = self.getSceneEditor().getScene().moai()
			if moai.initReady:
				self.setLuaState( moai.lua )
			self.startTimer()

	def onSceneStoped( self, sceneId ):
		# print("Scene Stoped: {}   current: {}".format(sceneId, self._sceneId))
		if self._sceneId == sceneId and sceneId != -1:
			self.stopTimer()
			self._sceneId = -1

	def onScenePaused( self, sceneId ):
		# print("Scene Paused: {}   current: {}".format(sceneId, self._sceneId))
		if self._sceneId == sceneId and sceneId != -1:
			self.stopTimer()
			self._sceneId = -1

	def onSceneSourcePreOpened( self, sceneId ):
		# print("Scene Pre Opened: {}   current: {}".format(sceneId, self._sceneId))
		if self._sceneId == sceneId and sceneId != -1:
			self.stopTimer()

	def onSceneSourceOpened( self, sceneId ):
		# print("Scene Opened: {}   current: {}".format(sceneId, self._sceneId))
		if self._sceneId == sceneId and sceneId != -1:
			self._sceneId = -1
			self.onSceneStarted( sceneId )

##----------------------------------------------------------------##

# StatsViewer().register()
