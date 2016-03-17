import os.path

from PySide             import QtCore, QtGui, QtOpenGL
from PySide.QtCore      import Qt
from PySide.QtGui     	import QApplication, QStyle, QBrush, QColor, QPen, QIcon, QPalette

from juma.core                	import signals, app
from juma.moai.MOAIRuntime import MOAILuaDelegate
from juma.qt.controls.GenericTreeWidget import GenericTreeWidget, GenericTreeFilter
from SceneEditor             	import SceneEditorModule



##----------------------------------------------------------------##
def getModulePath( path ):
	import os.path
	return os.path.dirname( __file__ ) + '/' + path

##----------------------------------------------------------------##
class SceneGraphEditor( SceneEditorModule ):
	_name = 'scenegraph_editor'
	_dependency = [ 'qt', 'moai', 'scene_editor' ]

	def __init__(self):
		super( SceneGraphEditor, self ).__init__()
		self.delegate = None

	def onLoad( self ):
		self.windowTitle = 'Scenegraph'
		self.window = self.requestDockWindow( 'SceneGraphEditor',
			title     = self.windowTitle,
			dock      = 'left',
			size      = (200,200),
			minSize   = (200,200),
			)
		self.treeFilter = self.window.addWidget(
				GenericTreeFilter(
					self.window
				),
				expanding = False
			)
		self.tree = self.window.addWidget( 
				SceneGraphTreeWidget( 
					self.window,
					sorting  = True,
					editable = True,
					multiple_selection = True,
					drag_mode = 'internal'
				)
			)

		self.treeFilter.setTargetTree( self.tree )
		self.tree.module = self

		self.tool = self.addToolBar( 'scene_graph', self.window.addToolBar() )

		self.delegate = MOAILuaDelegate( self )
		self.delegate.load( getModulePath( 'SceneGraphEditor.lua' ) )

		self.addTool( 'scene_graph/create_group', label ='+ Group', icon = 'folder_plus' )
		self.addTool( 'scene_graph/create_entity', label ='+ Entity', icon = 'plus_mint' )
		self.addTool( 'scene_graph/destroy_item', label ='- Item', icon = 'minus' )

	def createGroup(self):
		pass

	def createEntity(self):
		self.tree.createEntity()

	def destroyItem(self):
		pass

	def onTool( self, tool ):
		name = tool.name
		if name == 'create_group':
			self.createGroup()

		elif name == 'create_entity':
			self.createEntity()

		elif name == 'destroy_item':
			self.destroyItem()

##----------------------------------------------------------------##

SceneGraphEditor().register()

##----------------------------------------------------------------##
class SceneGraphTreeItemDelegate(QtGui.QStyledItemDelegate):
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
			painter.setBrush( SceneGraphTreeItemDelegate._backgroundBrushSelected )
			painter.drawRect(option.rect)
		elif option.state & QStyle.State_MouseOver:
			painter.setPen  ( Qt.NoPen )
			painter.setBrush( SceneGraphTreeItemDelegate._backgroundBrushHovered )
			painter.drawRect(option.rect)

		rect = option.rect
		icon = QIcon( index.data( Qt.DecorationRole) )
		rect.adjust( 5, 0, 0, 0 )
		if icon and not icon.isNull():
			icon.paint( painter, rect, Qt.AlignLeft )
			rect.adjust( 22, 0, 0, 0 )
		text = index.data(Qt.DisplayRole)
		if utype == 1: #GROUP
			painter.setPen( SceneGraphTreeItemDelegate._textPenGroup )
		else:
			painter.setPen( SceneGraphTreeItemDelegate._textPen )
		painter.drawText( rect, Qt.AlignLeft | Qt.AlignVCenter, text )
		painter.restore()

class ReadonlySceneGraphTreeItemDelegate( SceneGraphTreeItemDelegate ):
	def createEditor( *args ):
		return None

##----------------------------------------------------------------##
class SceneGraphTreeWidget( GenericTreeWidget ):
	def __init__( self, *args, **kwargs ):
		super( SceneGraphTreeWidget, self ).__init__( *args, **kwargs )
		# self.syncSelection = True
		# self.adjustingRange = False
		# self.verticalScrollBar().rangeChanged.connect( self.onScrollRangeChanged )
		self.setIndentation( 13 )

	def getHeaderInfo( self ):
		return [('Name',240), ('V',27 ), ('L',27 ), ( 'Layer', 50 ), ('', -1) ]

	def getReadonlyItemDelegate( self ):
		return ReadonlySceneGraphTreeItemDelegate( self )

	def getDefaultItemDelegate( self ):
		return SceneGraphTreeItemDelegate( self )

	def getRootNode( self ):
		return self.module.getActiveSceneRootGroup()

	##----------------------------------------------------------------##
	# Event Callback
	##----------------------------------------------------------------##
	def onClicked(self, item, col):
		print("onClicked", item, col)

	def onDClicked(self, item, col):
		print("onDClicked", item, col)
		
	def onItemSelectionChanged(self):
		print("onItemSelectionChanged")

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
		print("onDeletePressed")