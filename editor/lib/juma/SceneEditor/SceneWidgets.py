#!/usr/bin/env python

import sys
import os

from PySide import QtCore, QtGui

class SceneSizeComboBox( QtGui.QComboBox ):
	def __init__( self, parent ):
		super( SceneSizeComboBox, self ).__init__( parent )