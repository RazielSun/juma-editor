import os.path
import logging

from juma.core import app

def run( stop_other_instance, name ):
	import juma.SceneEditor
	
	options = {}
	options[ 'stop_other_instance' ] = stop_other_instance

	print 'starting IDE...'
	app.run( **options )		

def main( argv ):
	return run( argv[1:], 'juma ide' )