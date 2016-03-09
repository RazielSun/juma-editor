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
	_type = None

	def __init__(self, type):
		self._type = type

	def getType(self):
		return self._type