#!/usr/bin/env python
import logging
import sys
import imp
import os
import os.path
import re
import shutil
import hashlib
import time

import signals
import jsonHelper

##----------------------------------------------------------------##
class Project(object):
	_type = 'moai'
	_header = None

	def __init__(self):
		pass

	def getType(self):
		return self._type

	# Header
	def setHeader( self, header ):
		if header:
			self._header = header

	def head(self):
		return self._header