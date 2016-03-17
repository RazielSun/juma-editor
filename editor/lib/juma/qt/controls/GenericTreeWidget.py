
from PySide                 import QtCore, QtGui, QtOpenGL
from PySide.QtCore 			import Qt



##----------------------------------------------------------------##
class ReadonlyItemDelegate( QtGui.QStyledItemDelegate ):
	def createEditor( *args ):
		return None

##----------------------------------------------------------------##
class GenericTreeWidget( QtGui.QTreeWidget ):
	def __init__( self, *args, **option ):
		super(GenericTreeWidget, self).__init__(*args)

		self.setUniformRowHeights( True )
		self.setHorizontalScrollMode( QtGui.QAbstractItemView.ScrollPerPixel )
		self.setVerticalScrollMode( QtGui.QAbstractItemView.ScrollPerItem )

		self.readonlyItemDelegate = self.getReadonlyItemDelegate()
		self.defaultItemDelegate  = self.getDefaultItemDelegate()

		self.option = option
		headerInfo = self.getHeaderInfo()
		headerItem = QtGui.QTreeWidgetItem()
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
		self.itemChanged          .connect( self.onItemChanged )
		self.setIndentation( 12 )

		self.initRootItem()

		self.counts = 0

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

	def newItem( self ):
		item  = QtGui.QTreeWidgetItem()
		return item

	def createEntity( self ):
		self.counts += 1
		root = self.rootItem
		item = QtGui.QTreeWidgetItem( root, ["Entity {}".format(self.counts), "default"])

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

	def onItemChanged( self, item, col ):
		pass

	def onDeletePressed( self ):
		pass

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
