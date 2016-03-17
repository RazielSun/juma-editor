
from PySide                   import QtCore, QtGui, QtOpenGL



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
		# self.defaultItemDelegate  = self.getDefaultItemDelegate()

		self.option = option
		headerInfo = self.getHeaderInfo()
		headerItem = QtGui.QTreeWidgetItem()
		self.setHeaderItem(headerItem)
		# self.setItemDelegate( self.defaultItemDelegate )
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
		# self.sortByColumn( 0, 0 )

		# self.itemDoubleClicked    .connect( self.onDClicked )
		# self.itemClicked          .connect( self.onClicked )
		# self.itemExpanded         .connect( self.onItemExpanded )
		# self.itemCollapsed        .connect( self.onItemCollapsed )
		# self.itemSelectionChanged .connect( self.onItemSelectionChanged )
		# self.itemActivated        .connect( self.onItemActivated )
		# self.itemChanged          .connect( self._onItemChanged )
		self.setIndentation( 12 )

		self.initRootItem()

	def getReadonlyItemDelegate( self ):
		return ReadonlyItemDelegate( self )

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
		return [('Name',100), ('State',30)]

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
			self.rootItem = self.createItem( None )
			self.invisibleRootItem().addChild( self.rootItem )
		else:
			self.rootItem = self.invisibleRootItem()