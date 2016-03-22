import re, fnmatch

from PySide                 import QtCore, QtGui, QtOpenGL
from PySide.QtCore 			import Qt
from PySide.QtGui 			import QApplication

from juma.qt.helpers 		import repolishWidget


##----------------------------------------------------------------##
class ReadonlyItemDelegate( QtGui.QStyledItemDelegate ):
	def createEditor( *args ):
		return None

##----------------------------------------------------------------##
class GenericTreeWidgetItem( QtGui.QTreeWidgetItem ):
	def __eq__(self, other):
		return str(self) == str(other)

	def __ne__(self, other):
		return str(self) != str(other)

##----------------------------------------------------------------##
class GenericTreeWidget( QtGui.QTreeWidget ):
	def __init__( self, *args, **option ):
		super(GenericTreeWidget, self).__init__(*args)

		self.setUniformRowHeights( True )
		self.setHorizontalScrollMode( QtGui.QAbstractItemView.ScrollPerPixel )
		self.setVerticalScrollMode( QtGui.QAbstractItemView.ScrollPerItem )
		self.nodeDict = {}

		self.readonlyItemDelegate = self.getReadonlyItemDelegate()
		self.defaultItemDelegate  = self.getDefaultItemDelegate()

		self.refreshing = False
		self.rebuilding = False
		self.firstSetup = True

		self.option = option
		headerInfo = self.getHeaderInfo()
		headerItem = GenericTreeWidgetItem()
		self.setHeaderItem(headerItem)
		self.setItemDelegate( self.defaultItemDelegate )
		self.resetHeader()
	
		self.setSortingEnabled( self.getOption('sorting', True) )
	
		if self.getOption( 'multiple_selection', False ):
			self.setSelectionMode( QtGui.QAbstractItemView.ExtendedSelection )
		else:
			self.setSelectionMode( QtGui.QAbstractItemView.SingleSelection )

		dragMode = self.getOption( 'drag_mode', None )
		if dragMode == 'all':
			self.setDragDropMode( QtGui.QAbstractItemView.DragDrop )
		elif dragMode == 'drag':
			self.setDragDropMode( QtGui.QAbstractItemView.DragOnly )
		elif dragMode == 'drop':
			self.setDragDropMode( QtGui.QAbstractItemView.DropOnly )
		elif dragMode == 'internal' or dragMode == True:
			self.setDragDropMode( QtGui.QAbstractItemView.InternalMove )
			
		self.setAlternatingRowColors( self.getOption('alternating_color', False) )
		self.setExpandsOnDoubleClick( False )
		self.sortByColumn( 0, Qt.AscendingOrder )

		self.itemDoubleClicked    .connect( self.onDClicked )
		self.itemClicked          .connect( self.onClicked )
		self.itemExpanded         .connect( self.onItemExpanded )
		self.itemCollapsed        .connect( self.onItemCollapsed )
		self.itemSelectionChanged .connect( self.onItemSelectionChanged )
		self.itemActivated        .connect( self.onItemActivated )
		self.itemChanged          .connect( self._onItemChanged )
		self.setIndentation( 12 )

		self.initRootItem()

	def getReadonlyItemDelegate( self ):
		return ReadonlyItemDelegate( self )

	def getDefaultItemDelegate( self ):
		return QtGui.QStyledItemDelegate( self )

	def getOption( self, k, v ):
		defOption = self.getDefaultOptions()
		option    = self.option
		if defOption:
			defValue = defOption.get( k, v )
		else:
			defValue = v
		return option.get( k, defValue )

	def getDefaultOptions( self ):
		return None

	def getHeaderInfo( self ):
		return [('Name',150), ('State',50)]

	def updateHeaderItem( self, item, col, info ):
		pass

	def clear( self ):
		self.setUpdatesEnabled( False )
		for item in self.nodeDict.values():
			item.node = None
		self.nodeDict = {}
		super( GenericTreeWidget, self ).clear()
		self.initRootItem()
		self.rootItem.node = None
		self.setUpdatesEnabled( True )

	def rebuild( self, **option ):
		self.rebuilding = True
		self.hide()
		self.setUpdatesEnabled( False )
		self.clear()
		rootNode = self.getRootNode()
		if rootNode:
			self.addNode( rootNode )
			self.loadTreeStates()
		self.setUpdatesEnabled( True )
		self.show()
		self.rebuilding = False
		if self.firstSetup: # workaround: avoid unexpected column resizing
			self.resetHeader()
			self.firstSetup = False

	def resetHeader( self ):
		headerInfo = self.getHeaderInfo()
		headerItem = self.headerItem()
		for i in range( 0, len(headerInfo) ):			
			if i > 0:
				self.setItemDelegateForColumn( i, self.readonlyItemDelegate )			
			info =  headerInfo[i]
			title = info[ 0 ]
			width = info[ 1 ]
			headerItem.setText ( i, title )
			if width > 0:
				self.setColumnWidth ( i, width )
			self.updateHeaderItem( headerItem, i, info )

	def initRootItem( self ):
		if self.getOption( 'show_root', False ):
			self.rootItem = self.newItem()
			self.invisibleRootItem().addChild( self.rootItem )
		else:
			self.rootItem = self.invisibleRootItem()

	def createItem( self ):
		item  = GenericTreeWidgetItem()
		return item

	def getItemByNode(self, node):
		return self.nodeDict.get( node, None )

	def addNode( self, node, addChildren = True, **option ):
		assert not node is None, 'attempt to insert null node '
		item = self.nodeDict.get( node, None )
		if item:
			return item

		pnode = self.getNodeParent( node )
		assert pnode != node, 'parent is item itself'

		if not pnode :
			item = self.rootItem
			item.node = node
		else:
			pitem = self.getItemByNode( pnode )
			if not pitem:
				pitem = self.rootItem
				pitem.node = pnode
				self.nodeDict[ pnode ] = pitem
			item = self.createItem()
			item.node = node
			pitem.addChild( item )

		self.nodeDict[ node ] = item

		item.setExpanded( self.getOption( 'expanded', True ) )

		self.updateItem( node )
		if addChildren:
			children = self.getNodeChildren( node )
			if children:
				for child in children:
					self.addNode( child, True, **option )

		return item

	def getNodeParent( self, node ):
		return None
		
	def refreshAllContent( self ):
		for node in self.nodeDict.keys():
			self.refreshNodeContent( node )

	def refreshNodeContent( self, node, **option ):
		prevRefreshing = self.refreshing
		self.refreshing = True
		item = self.getItemByNode( node )
		if item:
			self.updateItemContent( item, node, **option )
			if option.get('updateChildren', False):
				children = self.getNodeChildren( node )
				if children:
					for child in children:
						self.refreshNodeContent( child , **option )
		self.refreshing = prevRefreshing

	def updateItemContent( self, item, node, **option ):
		pass

	def updateItem(self, node, **option ):
		return self._updateItem( node, None, **option )

	def getNodeChildren( self, node ):
		return []

	##----------------------------------------------------------------##
	def _updateItem(self, node, updateLog=None, **option):
		item = self.getItemByNode(node)
		if not item:
			return False
		if not updateLog: # for avoiding duplicated updates
			updateLog={}
		if updateLog.has_key(node):
			return False
		updateLog[node]=True

		self.refreshing = True
		self.updateItemContent( item, node, **option )
		# flags = self._calcItemFlags( node )
		# item.setFlags( flags )
		self.refreshing = False

		if option.get('updateChildren',False):
			children = self.getNodeChildren( node )
			if children:
				for child in children:
					self._updateItem(child, updateLog, **option)

		return True

	def selectNode( self, node, **kw ):
		pass
		# if not kw.get( 'add', False ):
		# 		self.selectionModel().clearSelection()
		# if not node: return
		# if isinstance( node, (tuple, list) ):
		# 	for n in node:
		# 		item = self.getItemByNode( n )
		# 		if item:
		# 			item.setSelected( True )
		# 	if kw.get('goto',True) : 
		# 		first = len( node ) > 0 and node[0]
		# 		if first:
		# 			self.gotoNode( first )
		# else:
		# 	item = self.getItemByNode( node )
		# 	if item:
		# 		item.setSelected( True )
		# 		if kw.get('goto',True) : 
		# 			self.gotoNode( node )

	##----------------------------------------------------------------##
	def _removeItem( self, item ):
		for child in item.takeChildren():
			self._removeItem( child )
		node = item.node
		item.node = None
		del self.nodeDict[ node ]
		( item.parent() or self.rootItem ).removeChild( item )
		return True

	def removeNode(self, node):		
		item = self.getItemByNode( node )
		if item and item != self.rootItem:
			self._removeItem( item )
			return True
		return False

	##----------------------------------------------------------------##
	def loadTreeStates( self ):
		pass

	##----------------------------------------------------------------##
	# Event Callback
	##----------------------------------------------------------------##
	def onClicked(self, item, col):
		pass

	def onDClicked(self, item, col):
		pass
		
	def onItemSelectionChanged(self):
		pass

	def onItemActivated(self, item, col):
		pass

	def onItemExpanded( self, item ):
		pass

	def onItemCollapsed( self, item ):
		pass

	def onClipboardCopy( self ):
		pass

	def onClipboardCut( self ):
		pass

	def onClipboardPaste( self ):
		pass

	def _onItemChanged( self, item, col ):
		if self.refreshing: return
		return self.onItemChanged( item, col )

	def onItemChanged( self, item, col ):
		pass

	def onDeletePressed( self ):
		pass

	##----------------------------------------------------------------##
	#custom control
	def keyPressEvent( self, ev ):
		modifiers = QApplication.keyboardModifiers()
		key = ev.key()
		if key in ( Qt.Key_Delete, Qt.Key_Backspace ):			
			self.onDeletePressed()
		elif key == Qt.Key_Escape: 
			self.selectNode( [] ) # deselect all

##----------------------------------------------------------------##
class GenericTreeFilter( QtGui.QWidget ):
	def __init__(self, *args ):
		super(GenericTreeFilter, self).__init__( *args )
		self.setObjectName( 'ItemFilter' )
		self.setSizePolicy( QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed )
		self.setMinimumSize( 100, 20 )
		layout = QtGui.QHBoxLayout( self )
		layout.setContentsMargins( 0, 0, 0, 0 )
		layout.setSpacing( 0 )
		self.buttonClear = QtGui.QToolButton( self )
		self.buttonClear.setText( 'X' )
		self.buttonClear.setObjectName( 'ClearButton' )
		# self.buttonClear.setIconSize( QtCore.QSize( 12, 12 ) )
		# self.buttonClear.setIcon( getIcon('remove') )
		self.buttonClear.clicked.connect( self.clearFilter )
		self.lineEdit = QtGui.QLineEdit( self )
		self.lineEdit.textChanged.connect( self.onTextChanged )
		self.lineEdit.setPlaceholderText( 'Filters' )
		self.targetTree = None

		layout.addWidget( self.buttonClear )
		layout.addWidget( self.lineEdit )
		self.lineEdit.setMinimumSize( 100, 20 )
		self.lineEdit.setSizePolicy( QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed )

		self.lineEdit.installEventFilter( self )
		self.buttonClear.hide()

	def eventFilter( self, object, event ):
		e=event.type()
		if e == QtCore.QEvent.KeyPress:
			key = event.key()
			if key == Qt.Key_Escape:
				self.clearFilter()
				return True
			elif key in [ Qt.Key_Down, Qt.Key_PageDown, Qt.Key_PageUp ]:
				self.targetTree.setFocus()
				return True
		return False

	def setTargetTree( self, tree ):
		self.targetTree = tree

	def onTextChanged( self, text ):
		self.applyFilter( text )

	def applyFilter( self, pattern ):
		if not self.targetTree: return
		pattern = pattern.strip()
		if pattern:
			regex = '.*?'.join( map(re.escape, pattern.upper()) )
			ro = re.compile( regex )
		else:
			ro = None
		if ro:
			self.targetTree.setProperty( 'filtered', True )
			self.buttonClear.show()
		else:
			self.targetTree.setProperty( 'filtered', False )
			self.buttonClear.hide()
		self.targetTree.hide()
		self.applyFilterToItem( self.targetTree.invisibleRootItem(), ro )
		repolishWidget( self.targetTree )
		self.targetTree.show()

	def applyFilterToItem( self, item, ro ):
		count = item.childCount()
		childVisible = False
		for idx in range( count ):
			childItem = item.child( idx )
			if self.applyFilterToItem( childItem, ro ):
				childVisible = True
		value = item.text( 0 ).upper()
		if ro:
			selfVisible = ro.search( value ) and True or False
		else:
			selfVisible = True

		if selfVisible:
			item.setHidden( False )
			return True
		elif childVisible:
			item.setHidden( False )
			return True
		else:
			item.setHidden( True )
			return False

	def setFilter( self, text ):
		self.lineEdit.setText( text )

	def clearFilter( self ):
		self.lineEdit.setText( '' )
