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
	def __init__(self):
		pass