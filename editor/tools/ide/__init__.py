import os.path
import logging
# import click

from juma.core import app

# @click.command( help = 'start gii IDE' )

def run( stop_other_instance, name ):
	app.openEditor()

	import juma.qt.QtSupport
	# import gii.SceneEditor
	# import gii.AssetEditor
	# import gii.DeviceManager
	# import gii.DebugView

	# import gii.ScriptView
	
	options = {}
	options[ 'stop_other_instance' ] = stop_other_instance

	print 'starting gii IDE...'
	app.run( **options )		

def main( argv ):
	return run( argv[1:], 'juma ide' )