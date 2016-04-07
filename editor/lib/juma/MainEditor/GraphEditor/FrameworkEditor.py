#!/usr/bin/env python

import os.path

from juma.core import  *
from juma.MainEditor.Introspector 		import registerEditorBuilder

##----------------------------------------------------------------##
_frameworkInited = False
_frameworkEditorBuilders = {}

def registerFrameworkEditorBuilder( className, editorClass ):
	_frameworkEditorBuilders[ className ] = editorClass
	if _frameworkInited:
		# mockClass = _MOCK[ mockClassName ]
		registerEditorBuilder( className, editorClass )

def onFrameworkInited():
	global _frameworkInited
	_frameworkInited = True
	for className, editorClass in  _frameworkEditorBuilders.items():
		# mockClass = _MOCK[ mockClassName ]
		registerEditorBuilder( className, editorClass )

signals.connect( 'framework.init', onFrameworkInited )