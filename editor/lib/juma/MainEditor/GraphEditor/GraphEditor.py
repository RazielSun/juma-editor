#!/usr/bin/env python

import os.path

from PySide             import QtCore, QtGui, QtOpenGL
from PySide.QtCore      import Qt
from PySide.QtGui     	import QFileDialog, QStyle, QBrush, QColor, QPen, QIcon, QPalette

from juma.core                			import signals, app
from juma.core.layout 					import _saveLayoutToFile
from juma.moai.MOAIRuntime 				import MOAILuaDelegate
from juma.qt.IconCache 					import getIcon
from juma.qt.controls.GenericTreeWidget import GenericTreeWidget, GenericTreeFilter
from juma.MainEditor.MainEditor       	import MainEditorModule

##----------------------------------------------------------------##
def getModulePath( path ):
	import os.path
	return os.path.dirname( __file__ ) + '/' + path

##----------------------------------------------------------------##
class GraphEditor( MainEditorModule ):
	_name = 'graph_editor'
	_dependency = [ 'qt', 'moai', 'main_editor' ]

	def __init__(self):
		super( GraphEditor, self ).__init__()
		self.delegate = None
		self.dirty = False
		self.previewing = False

	def onLoad( self ):
		self.windowTitle = 'Hierarchy'
		self.window = self.requestDockWindow( 'GraphEditor',
			title     = self.windowTitle,
			dock      = 'left',
			size      = (300,200),
			minSize   = (300,200),
			)
		self.treeFilter = self.window.addWidget(
				GenericTreeFilter(
					self.window
				),
				expanding = False
			)
		self.tree = self.window.addWidget( 
				GraphTreeWidget( 
					self.window,
					sorting  = True,
					editable = True,
					multiple_selection = True,
					drag_mode = 'internal'
				)
			)

		self.treeFilter.setTargetTree( self.tree )
		self.tree.module = self

		self.tool = self.addToolBar( 'hierarchy', self.window.addToolBar() )

		self.delegate = MOAILuaDelegate( self )
		self.delegate.load( getModulePath( 'GraphEditor.lua' ) )
		self.luaMgrId = 'graphEditor'

		self.findMenu( 'main/scene' ).addChild([
            dict( name = 'scene_open', label = 'Open Scene' ),
            dict( name = 'scene_save', label = 'Save Scene' ),
        ], self )

		self.addTool( 'hierarchy/scene_settings', label ='Scene Settings', icon = 'cog' )
		self.addTool( 'hierarchy/create_widget', label ='+ Entity', icon = 'plus_mint' )
		# self.addTool( 'hierarchy/destroy_item', label ='- Item', icon = 'minus' )

		self.contextMenu = self.addMenu( 'widget_context', dict( label = 'Widgets' ) )
		self.addMenuItem( 'widget_context/create_sprite', dict( label = 'Sprite' ) )
		self.addMenuItem( 'widget_context/create_label', dict( label = 'Label' ) )
		self.addMenuItem( 'widget_context/create_button', dict( label = 'Button' ) )
		self.addMenuItem( 'widget_context/create_group', dict( label = 'Group' ) )

		#SIGNALS
		signals.connect( 'moai.clean',        self.onMoaiClean        )

		signals.connect( 'selection.changed', self.onSelectionChanged )
		signals.connect( 'selection.hint',    self.onSelectionHint    )

		signals.connect( 'entity.added',      self.onEntityAdded      )
		signals.connect( 'entity.removed',    self.onEntityRemoved    )
		signals.connect( 'entity.renamed',    self.onEntityRenamed    )
		signals.connect( 'entity.modified',   self.onEntityModified    )
		signals.connect( 'entity.visible_changed',    self.onEntityVisibleChanged )
		signals.connect( 'entity.pickable_changed',   self.onEntityPickableChanged )

	def onStart(self): # FIXME
		self.tree.rebuild()

	def getActiveScene( self ):
		return self.delegate.safeCallMethod( self.luaMgrId, 'getScene' )

	def getActiveSceneRootGroup( self ):
		rootNode = self.delegate.safeCallMethod( self.luaMgrId, 'getSceneRootNode' )
		if rootNode:
			return rootNode
		return None

	def markDirty( self, dirty = True ):
		if not self.previewing:
			self.dirty = dirty

	def onSceneChange(self):
		self.tree.hide()
		self.tree.rebuild()
		# self.restoreWorkspaceState()
		self.tree.refreshAllContent()
		self.tree.verticalScrollBar().setValue( 0 )
		self.tree.show()

##----------------------------------------------------------------##
	def openScene(self):
		filePath, filt = QFileDialog.getOpenFileName(self.getMainWindow(), "Open Scene", self.getProject().path or "~", "Layout file (*.layout )")
		if filePath:
			sceneName = os.path.basename( filePath )
			signals.emitNow( 'scene.open', sceneName )
			node = self.delegate.safeCallMethod( self.luaMgrId, 'loadScene', filePath )
			self.onSceneChange()

	def saveScene(self):
		filePath, filt = QFileDialog.getSaveFileName(self.getMainWindow(), "Save Scene", self.getProject().path or "~", "Layout file (*.layout )")
		if filePath:
			data = self.delegate.safeCallMethod( self.luaMgrId, 'saveScene' )
			_saveLayoutToFile( filePath, data )
			sceneName = os.path.basename( filePath )
			signals.emitNow( 'scene.open', sceneName )

	def openSceneSettings(self):
		pass

	def createWidget(self, widget):
		node = self.delegate.safeCallMethod( self.luaMgrId, 'createWidget', widget )
		self.tree.addNode( node, expanded = False )

	def removeWidget(self, item):
		node = item.node
		if node:
			if self.tree.removeNode( node ):
				self.delegate.safeCallMethod( self.luaMgrId, 'removeWidget', node )

	##----------------------------------------------------------------##
	def openContextMenu( self ):
		if self.contextMenu:
			self.contextMenu.popUp()

	##----------------------------------------------------------------##
	def onMenu( self, tool ):
		name = tool.name
		if name == 'scene_open':
			self.openScene()

		elif name == 'scene_save':
			self.saveScene()

		elif name == 'create_sprite':
			self.createWidget( 'Sprite' )

		elif name == 'create_label':
			self.createWidget( 'Label' )

		elif name == 'create_button':
			self.createWidget( 'Button' )

		elif name == 'create_group':
			self.createWidget( 'Group' )

	def onTool( self, tool ):
		name = tool.name
		if name == 'scene_settings':
			self.openSceneSettings()

		elif name == 'create_widget':
			self.openContextMenu()

		elif name == 'destroy_item':
			self.destroyItem()

	def onMoaiClean( self ):
		self.tree.clear()

	def onSelectionChanged( self, selection, key ):
		if key != 'scene': return
		# if self.tree.syncSelection:
		# 	self.tree.blockSignals( True )
		# 	self.tree.selectNode( None )
		# 	for e in selection:
		# 		self.tree.selectNode( e, add = True)
		# 	self.tree.blockSignals( False )

	def onSelectionHint( self, selection ):
		pass
		# if selection._entity:
		# 	self.changeSelection( selection._entity )			
		# else:
		# 	self.changeSelection( selection )

	##----------------------------------------------------------------##
	def onEntityAdded( self, entity, context = None ):
		if context == 'new':
			self.setFocus()
			pnode = entity.parent
			if pnode:
				self.tree.setNodeExpanded( pnode, True )
			self.tree.setFocus()
			# self.tree.editNode( entity )
			# self.tree.selectNode( entity )
		signals.emit( 'scene.update' )
		self.markDirty()

	def onEntityRemoved( self, entity ):
		signals.emit( 'scene.update' )
		self.markDirty()

	def onEntityRenamed( self, entity, newname ):
		self.tree.refreshNodeContent( entity )
		self.markDirty()

	def onEntityModified( self, entity, context = None ):
		self.markDirty()

	def onEntityVisibleChanged( self, entity ):
		self.tree.refreshNodeContent( entity )

	def onEntityPickableChanged( self, entity ):
		self.tree.refreshNodeContent( entity )

##----------------------------------------------------------------##

GraphEditor().register()

##----------------------------------------------------------------##
class GraphTreeItemDelegate(QtGui.QStyledItemDelegate):
	_textBrush      = QBrush( QColor( '#dd5200' ) )
	_textPen        = QPen( QColor( '#dddddd' ) )
	_textPenGroup   = QPen( QColor( '#ada993' ) )
	_backgroundBrushHovered  = QBrush( QColor( '#454768' ) )
	_backgroundBrushSelected = QBrush( QColor( '#515c84' ) )
	
	def paint(self, painter, option, index):
		painter.save()
		index0 = index.sibling( index.row(), 0 )
		utype = index0.data( Qt.UserRole )

		# # set background color
		if option.state & QStyle.State_Selected:
			painter.setPen  ( Qt.NoPen )
			painter.setBrush( GraphTreeItemDelegate._backgroundBrushSelected )
			painter.drawRect(option.rect)
		elif option.state & QStyle.State_MouseOver:
			painter.setPen  ( Qt.NoPen )
			painter.setBrush( GraphTreeItemDelegate._backgroundBrushHovered )
			painter.drawRect(option.rect)

		rect = option.rect
		icon = QIcon( index.data( Qt.DecorationRole) )
		rect.adjust( 5, 0, 0, 0 )
		if icon and not icon.isNull():
			icon.paint( painter, rect, Qt.AlignLeft )
			rect.adjust( 22, 0, 0, 0 )
		text = index.data(Qt.DisplayRole)
		if utype == 1: #GROUP
			painter.setPen( GraphTreeItemDelegate._textPenGroup )
		else:
			painter.setPen( GraphTreeItemDelegate._textPen )
		painter.drawText( rect, Qt.AlignLeft | Qt.AlignVCenter, text )
		painter.restore()

class ReadonlyGraphTreeItemDelegate( GraphTreeItemDelegate ):
	def createEditor( *args ):
		return None

##----------------------------------------------------------------##
class GraphTreeWidget( GenericTreeWidget ):
	def __init__( self, *args, **kwargs ):
		super( GraphTreeWidget, self ).__init__( *args, **kwargs )
		self.syncSelection = True
		# self.adjustingRange = False
		# self.verticalScrollBar().rangeChanged.connect( self.onScrollRangeChanged )
		self.setIndentation( 13 )

	def getHeaderInfo( self ):
		return [('Name',160), ('V',32 ), ('L',32 ), ( 'Layer', 50 ), ('', -1) ]

	def getReadonlyItemDelegate( self ):
		return ReadonlyGraphTreeItemDelegate( self )

	def getDefaultItemDelegate( self ):
		return GraphTreeItemDelegate( self )

	def getRootNode( self ):
		return self.module.getActiveSceneRootGroup()

	def getNodeParent( self, node ):
		p = node.getParent( node )
		if p:
			return p
		return None

	def getNodeChildren( self, node ):
		className = node.className(node)
		output = []
		if className == 'EntityGroup': # GROUP
			children = node.children
			for index in children:
				output.append( children[index] )
		else: # ENTITY
			pass
		return output

	def updateItemContent( self, item, node, **option ):
		name = None
		item.setData( 0, Qt.UserRole, 0 )

		item.setText( 0, node.name or '<unnamed>' )
		item.setIcon( 0, getIcon('dot') )

		# if isMockInstance( node, 'EntityGroup' ):
		# 	item.setText( 0, node.name or '<unnamed>' )
		# 	item.setIcon( 0, getIcon('entity_group') )
		# 	if node.isLocalVisible( node ):
		# 		item.setIcon( 1, getIcon( 'entity_vis' ) )
		# 	else:
		# 		item.setIcon( 1, getIcon( 'entity_invis' ) )

		# 	if node.isLocalEditLocked( node ):
		# 		item.setIcon( 2, getIcon( 'entity_lock' ) )
		# 	else:
		# 		item.setIcon( 2, getIcon( 'entity_nolock' ) )
		# 	item.setData( 0, Qt.UserRole, 1 )

		# elif isMockInstance( node, 'Entity' ):
		# 	if node['FLAG_PROTO_SOURCE']:
		# 		item.setIcon( 0, getIcon('proto') )
		# 	elif node['PROTO_INSTANCE_STATE']:
		# 		item.setIcon( 0, getIcon('instance') )
		# 	elif node['__proto_history']:
		# 		item.setIcon( 0, getIcon('instance-sub') )
		# 	elif isMockInstance( node, 'ProtoContainer' ):
		# 		item.setIcon( 0, getIcon('instance-container') )
		# 	else:
		# 		item.setIcon( 0, getIcon('obj') )
		# 	item.setText( 0, node.name or '<unnamed>' )
	
		# 	layerName = node.getLayer( node )
		# 	if isinstance( layerName, tuple ):
		# 		item.setText( 3, '????' )
		# 	else:
		# 		item.setText( 3, layerName )
		# 	# item.setText( 2, node.getClassName( node ) )
		# 	# item.setFont( 0, _fontAnimatable )
		# 	if node.isLocalVisible( node ):
		# 		item.setIcon( 1, getIcon( 'entity_vis' ) )
		# 	else:
		# 		item.setIcon( 1, getIcon( 'entity_invis' ) )

		# 	if node.isLocalEditLocked( node ):
		# 		item.setIcon( 2, getIcon( 'entity_lock' ) )
		# 	else:
		# 		item.setIcon( 2, getIcon( 'entity_nolock' ) )

	##----------------------------------------------------------------##
	# Event Callback
	##----------------------------------------------------------------##
	def onClicked(self, item, col):
		print("onClicked", item, col)

	def onDClicked(self, item, col):
		print("onDClicked", item, col)
		
	def onItemSelectionChanged(self):
		if not self.syncSelection: return
		items = self.selectedItems()
		if items:
			selections=[item.node for item in items]
			self.module.changeSelection(selections)
		else:
			self.module.changeSelection(None)

	def onItemActivated(self, item, col):
		print("onItemActivated", item, col)

	def onItemExpanded( self, item ):
		print("onItemExpanded", item)

	def onItemCollapsed( self, item ):
		print("onItemCollapsed", item)

	def onClipboardCopy( self ):
		print("onClipboardCopy")

	def onClipboardCut( self ):
		print("onClipboardCut")

	def onClipboardPaste( self ):
		print("onClipboardPaste")

	def onItemChanged( self, item, col ):
		print("onItemChanged", item, col)

	def onDeletePressed( self ):
		self.syncSelection = False
		item0 = self.currentItem()
		item1 = self.itemBelow( item0 )
		self.module.removeWidget( item0 ) # FIXME
		# self.module.doCommand( 'scene_editor/remove_entity' )
		if item1:
			self.setFocusedItem( item1 )
		self.syncSelection = True
		self.onItemSelectionChanged()