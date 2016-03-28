from juma.core.signals import register 

register( 'scene.start' )
register( 'scene.pause' )
register( 'scene.stop' )
register( 'scene.pre_open_source' )
register( 'scene.open_source' )

register( 'scene.pre_open' )
register( 'scene.open' )
register( 'scene.update' )
register( 'scene.change' )

# register( 'scene.clear' )
# register( 'scene.save' )
# register( 'scene.saved' )

register( 'entity.added' )
register( 'entity.removed' )
register( 'entity.modified' )
register( 'entity.renamed' )
register( 'entity.visible_changed' )
register( 'entity.pickable_changed' )

register( 'scene_tool.change' )