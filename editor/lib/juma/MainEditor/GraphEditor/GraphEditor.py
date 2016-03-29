#!/usr/bin/env python

import os.path

from PySide             import QtCore, QtGui, QtOpenGL
from PySide.QtCore      import Qt
from PySide.QtGui     	import QFileDialog, QStyle, QBrush, QColor, QPen, QIcon, QPalette

from juma.core                			import signals, app, AssetRefType
from juma.moai.MOAIRuntime 				import MOAILuaDelegate
from juma.qt.IconCache 					import getIcon
from juma.qt.controls.GenericTreeWidget import GenericTreeWidget, GenericTreeFilter
from juma.MainEditor.MainEditor       	import MainEditorModule
from juma.SearchView 					import requestSearchView

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

		self.findMenu( 'main/scene' ).addChild([
			dict( name = 'scene_open', label = 'Open Scene', shortcut = 'ctrl+O' ),
            dict( name = 'scene_open_as', label = 'Open Scene As...' ),
            dict( name = 'scene_save_as', label = 'Save Scene As...' ),
        ], self )

		self.addTool( 'hierarchy/scene_settings', label ='Scene Settings', icon = 'cog' )
		self.addTool( 'hierarchy/create_widget', label ='Create widget', icon = 'plus_mint' )

		self.contextMenu = self.addMenu( 'ui_context', dict( label = 'UI' ) )
		self.addMenuItem( 'ui_context/create_entity', dict( label = 'Entity' ) )
		self.addMenuItem( 'ui_context/create_button_color', dict( label = 'ButtonColor' ) )
		self.addMenuItem( 'ui_context/create_button', dict( label = 'Button' ) )
		self.addMenuItem( 'ui_context/create_label', dict( label = 'Label' ) )
		self.addMenuItem( 'ui_context/create_sprite', dict( label = 'Sprite' ) )
		

		#SIGNALS
		signals.connect( 'moai.clean',        self.onMoaiClean        )

		signals.connect( 'selection.changed', self.onSelectionChanged )
		signals.connect( 'selection.hint',    self.onSelectionHint    )

		signals.connect( 'scene.change',    self.onSceneChange		  )

		signals.connect( 'entity.added',      self.onEntityAdded      )
		signals.connect( 'entity.removed',    self.onEntityRemoved    )
		signals.connect( 'entity.renamed',    self.onEntityRenamed    )
		signals.connect( 'entity.modified',   self.onEntityModified   )
		signals.connect( 'entity.visible_changed',    self.onEntityVisibleChanged )
		signals.connect( 'entity.pickable_changed',   self.onEntityPickableChanged )

	def getActiveScene( self ):
		return self.delegate.safeCallMethod( 'editor', 'getScene' )

	def getActiveSceneRootGroup( self ):
		rootNode = self.delegate.safeCallMethod( 'editor', 'getSceneRootNode' )
		if rootNode:
			return rootNode
		return None

	def markDirty( self, dirty = True ):
		if not self.previewing:
			self.dirty = dirty

	def onSceneChange(self, scene):
		self.tree.hide()

		self.delegate.safeCallMethod( 'editor', 'changeScene', scene )

		self.tree.rebuild()
		# self.restoreWorkspaceState()
		self.tree.refreshAllContent()
		self.tree.verticalScrollBar().setValue( 0 )
		self.tree.show()

		signals.emitNow( 'scene.open', scene )

##----------------------------------------------------------------##
	def openScene(self):
		requestSearchView( 
			context      = 'asset',
			type         = 'layout',
			multiple_selection = False,
			on_selection = self.onSceneSearchSelection,
			on_cancel    = self.onSceneSearchCancel,
			# on_search    = self.onSceneSearch,
			)

	def openSceneAs(self):
		filePath, filt = QFileDialog.getOpenFileName(self.getMainWindow(), "Open Scene As", self.getProject().path or "~", "Layout file (*.layout )")
		if filePath:
			scene = self.delegate.safeCallMethod( 'editor', 'openSceneAs', filePath )
			signals.emitNow( 'scene.change', scene )

	def saveSceneAs(self):
		filePath, filt = QFileDialog.getSaveFileName(self.getMainWindow(), "Save Scene As", self.getProject().path or "~", "Layout file (*.layout )")
		if filePath:
			data = self.delegate.safeCallMethod( 'editor', 'saveSceneAs', filePath )

	def openSceneSettings(self):
		pass

	def createNodeUI(self, widget):
		# self.doCommand( 'main_editor/create_entity', name = widget )
		self.delegate.safeCallMethod( 'editor', 'addEntityByName', widget )

	def removeEntity(self, item):
		node = item.node
		if node:
			if self.tree.removeNode( node ):
				self.delegate.safeCallMethod( 'editor', 'removeEntity', node )

	def addEntityNode( self, entity ):
		self.tree.addNode( entity, expanded = False )
		self.tree.setNodeExpanded( entity, False )

	##----------------------------------------------------------------##
	def openContextMenu( self ):
		if self.contextMenu:
			self.contextMenu.popUp()

	##----------------------------------------------------------------##
	def onMenu( self, tool ):
		name = tool.name
		if name == 'scene_open':
			self.openScene()
		elif name == 'scene_open_as':
			self.openSceneAs()
		elif name == 'scene_save_as':
			self.saveSceneAs()

		elif name == 'create_sprite':
			self.createNodeUI( 'Sprite' )
		elif name == 'create_label':
			self.createNodeUI( 'Label' )
		elif name == 'create_button_color':
			self.createNodeUI( 'ButtonColor' )
		elif name == 'create_button':
			self.createNodeUI( 'Button' )
		elif name == 'create_entity':
			self.createNodeUI( 'Entity' )

	def onTool( self, tool ):
		name = tool.name
		if name == 'scene_settings':
			self.openSceneSettings()

		elif name == 'create_widget':
			self.openContextMenu()

	def onMoaiClean( self ):
		self.tree.clear()

	def onSelectionChanged( self, selection, key ):
		if key != 'scene': return
		if self.tree.syncSelection:
			self.tree.blockSignals( True )
			self.tree.selectNode( None )
			for e in selection:
				self.tree.selectNode( e, add = True)
			self.tree.blockSignals( False )

	def onSelectionHint( self, selection ):
		pass
		# if selection._entity:
		# 	self.changeSelection( selection._entity )			
		# else:
		# 	self.changeSelection( selection )

	def onSceneSearchSelection( self, target ):
		scene = self.delegate.safeCallMethod( 'editor', 'openScene', target.getNodePath() )
		signals.emitNow( 'scene.change', scene )

	def onSceneSearchCancel( self ):
		pass

	def onSceneSearch( self, typeId, context, option ):
		pass

	##----------------------------------------------------------------##
	def onEntityAdded( self, entity, context = None ):
		if context == 'new':
			self.setFocus()
			pnode = entity.parent
			if pnode:
				self.tree.setNodeExpanded( pnode, True )
			self.tree.setFocus()
			# self.tree.editNode( entity )
			self.tree.selectNode( entity )
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
		return [('Name',160), ('V',32 ), ('L',32 ), ('I',32 ), ('', -1) ] #( 'Layer', 50 ), ('', -1) ]

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
		output = []
		children = node.children
		for index in children:
			output.append( children[index] )
		return output

	def reparentNode( self, node, pitem, **option ):
		mode = option.get("mode", None)

		if node and pitem:
			pnode = None
			if pitem == 'root':
				pnode = self.getRootNode()
			else:
				if mode:
					pnode = pitem.node.parent # subling above below
				else:
					pnode = pitem.node
			if pnode:
				node.detach( node )
				if mode:
					itemMode = None
					item = self.getItemByNode(node)
					indexPaste = 0
					if mode == "above":
						itemMode = self.itemAbove(item)
						indexPaste = 1
					elif mode == "below":
						itemMode = self.itemBelow(item)
						indexPaste = -1
					nodeMode = itemMode.node
					nodeIndex = pnode.getChildIndex( pnode, nodeMode )
					pnode.addChild( pnode, node, nodeIndex + indexPaste )
				else:
					pnode.addChild( pnode, node )
				return True			
		return False

	def updateItemContent( self, item, node, **option ):
		name = None
		item.setData( 0, Qt.UserRole, 0 )

		if node and (node is not None):
			item.setText( 0, node.name or '<widget>' )
			item.setIcon( 0, getIcon('dot') )				

	def getItemFlags( self, node ):
		flagNames = {}
		return flagNames

	##----------------------------------------------------------------##
	def dropEvent( self, event ):		
		p = self.dropIndicatorPosition()
		pos = False
		if p == QtGui.QAbstractItemView.OnItem: # reparent
			pos = 'on'
		elif p == QtGui.QAbstractItemView.AboveItem:
			pos = 'above'
		elif p == QtGui.QAbstractItemView.BelowItem:
			pos = 'below'
		else:
			pos = 'viewport'

		target = self.itemAt( event.pos() )
		items = self.module.getSelection()
		
		ok = False
		for item in items:
			print("dropEvent pos: {} ::{} {} node:: ".format(pos, item, target))
			if pos == 'on':
				ok = self.reparentNode( item, target )
			# 	ok = self.module.doCommand( 'scene_editor/reparent_entity', target = target.node )
			elif pos == 'viewport':
				ok = self.reparentNode( item, 'root' )
			# 	ok = self.module.doCommand( 'scene_editor/reparent_entity', target = 'root' )
			elif pos == 'above' or pos == 'below':
				ok = self.reparentNode( item, target, mode = pos )
			# 	ok = self.module.doCommand( 'scene_editor/reparent_entity', target = target.node, mode = 'sibling' )

		if ok:
			super( GenericTreeWidget, self ).dropEvent( event )
		else:
			event.setDropAction( Qt.IgnoreAction )

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
		self.module.removeEntity( item0 ) # FIXME
		# self.module.doCommand( 'scene_editor/remove_entity' )
		if item1:
			self.setFocusedItem( item1 )
		self.syncSelection = True
		self.onItemSelectionChanged()