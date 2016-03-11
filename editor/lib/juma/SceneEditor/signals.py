from juma.core.signals import register 

register( 'scene.start' )
register( 'scene.pause' )
register( 'scene.stop' )
register( 'scene.pre_open_source' )
register( 'scene.open_source' )
register( 'scene.change_size' )

# register( 'scene.pre_open' )
# register( 'scene.update' )
# register( 'scene.clear' )
# register( 'scene.save' )
# register( 'scene.saved' )
# register( 'scene.open' )