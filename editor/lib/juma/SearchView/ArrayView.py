##----------------------------------------------------------------##
class ArrayFieldView( QtGui.QWidget ):
	def __init__(self, *args ):
		super( ArrayFieldView, self ).__init__( *args )
		# self.searchState = None

		self.setWindowFlags( Qt.Popup )
		self.ui = ui = ArrayViewContainer()
		ui.setupUi( self )
		
		# self.installEventFilter( WindowAutoHideEventFilter( self ) )
		# self.editor = None
		# self.treeResult = addWidgetWithLayout( 
		# 		SearchViewTree(
		# 			self.ui.containerResultTree,
		# 			multiple_selection = False,
		# 			editable = False,
		# 			sorting  = False
		# 		) 
		# 	)
		# self.treeResult.hideColumn( 0 )
		# self.textTerms = addWidgetWithLayout (
		# 	SearchViewTextTerm(self.ui.containerTextTerm )
		# 	)
		# self.textTerms.browser = self
		# self.textTerms.textEdited.connect( self.onTermsChanged )
		# self.textTerms.returnPressed.connect( self.onTermsReturn )

		# self.treeResult.browser = self
		# self.entries = None
		self.setMinimumSize( 400, 300  )
		# self.multipleSelection = False