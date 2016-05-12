#!/usr/bin/env python

import os
import os.path
import platform
import sys

##----------------------------------------------------------------##
def isPythonFrozen():
	return hasattr( sys, "frozen" )

def getMainModulePath():
	if isPythonFrozen():
		p = os.path.dirname(unicode(sys.executable, sys.getfilesystemencoding( )))
		if platform.system() == u'Darwin':
			return os.path.realpath( p + '/../../../..' )
		elif platform.system() == u'Windows':
			return p
		else:
			return p
	if __name__ == 'main':
		mainfile = os.path.realpath( __file__ )
		return os.path.dirname( mainfile )
	else:
		import __main__
		if hasattr( __main__, "__gii_path__" ):
			return __main__.__gii_path__
		else:
			mainfile = os.path.realpath( __main__.__file__ )
			return os.path.dirname( mainfile )

##----------------------------------------------------------------##

jumapath = getMainModulePath() + '/editor/lib'
thirdPartyPathBase = getMainModulePath() + '/editor/lib/3rdparty'
thirdPartyPathCommon = thirdPartyPathBase + '/common'
if platform.system() == u'Darwin':
	thirdPartyPathNative = thirdPartyPathBase + '/osx'
else:
	thirdPartyPathNative = thirdPartyPathBase + '/windows'

sys.path.insert( 0, jumapath )
sys.path.insert( 2, thirdPartyPathNative )
sys.path.insert( 1, thirdPartyPathCommon )

##----------------------------------------------------------------##

import juma

def main():
    juma.startup()

if __name__ == '__main__':
    main()