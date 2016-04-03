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

from ui.runstring_dock_ui 		import Ui_RunStringDock as Ui

##----------------------------------------------------------------##
def _getModulePath( path ):
	import os.path
	return os.path.dirname( __file__ ) + '/' + path

##----------------------------------------------------------------##
class RunStringDock( MainEditorModule ):
	"""docstring for RunStringDock"""
	_name       = 'run_string_dock'
	_dependency = ['qt', 'moai', 'main_editor']

	def __init__(self):
		super(RunStringDock, self).__init__()
		self.runtime = None

	def getRuntime(self):
		if self.runtime is None:
			self.runtime = self.affirmModule('moai')
		return self.runtime
	
	def onLoad( self ):
		self.window = self.requestDockWindow( 'RunStringDock',
			title     = 'Run String',
			dock      = 'right',
		)
		
		ui = Ui()
		self.ui =  ui
		self.ui.setupUi(self.window)

		ui.btnlocal.clicked.connect( self.onLocal )
		ui.btnremote.clicked.connect( self.onRemote )

		self.window.setStayOnTop( True )
		self.window.hide()

	def getString( self ): 
		return self.ui.textEdit.document().toPlainText()

	def onLocal( self ):
		runtime = self.getRuntime()
		if runtime:
			runtime.runString( self.getString() )

	def onRemote( self ):
		pass

##----------------------------------------------------------------##

RunStringDock().register()
