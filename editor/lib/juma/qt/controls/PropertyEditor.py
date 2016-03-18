from PySide import QtGui, QtCore
from PySide.QtCore import Qt

from juma.core.ModelManager import *



##----------------------------------------------------------------##
class PropertyEditor( QtGui.QFrame ):
	def __init__( self, parent ):	
		super( PropertyEditor, self ).__init__( parent )
		self.setObjectName( 'PropertyEditor' )
		layout = QtGui.QFormLayout()
		self.setLayout( layout )
		self.layout = layout
		self.layout.setHorizontalSpacing( 4 )
		self.layout.setVerticalSpacing( 1 )
		self.layout.setContentsMargins(4,4,4,4)
		self.layout.setLabelAlignment( Qt.AlignLeft )
		self.layout.setFieldGrowthPolicy( QtGui.QFormLayout.ExpandingFieldsGrow )
		self.setSizePolicy( QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding )

		self.editors    = {}
		self.target     = None
		self.refreshing = False
		self.context    = None
		self.model      = False
		self.readonly   = False
		self.clear()

	# def addFieldEditor( self, field ):
	# 	label = field.label
	# 	editor  =  buildFieldEditor( self, field )
	# 	labelWidget  = editor.initLabel( label, self )
	# 	editorWidget = editor.initEditor( self )
	# 	editorWidget.setObjectName( 'FieldEditor' )
	# 	labelWidget.setObjectName( 'FieldLabel' )
	# 	if labelWidget in (None, False):
	# 		self.layout.addRow ( editorWidget )
	# 	else:
	# 		self.layout.addRow ( labelWidget, editorWidget )
	# 	self.editors[ field ] = editor
	# 	return editor

	def addLabelField( self, label, container ):
		labelWidget = QtGui.QLabel( container )
		labelWidget.setText( "Name: {}".format(label) )
		labelWidget.setMinimumSize( 50, 16 )
		labelWidget.setSizePolicy(
			QtGui.QSizePolicy.Expanding,
			QtGui.QSizePolicy.Expanding
			)
		self.layout.addRow ( labelWidget )
		return labelWidget

	def getTarget( self ):
		return self.target
		
	def setTarget( self, target, **kwargs ):
		model = kwargs.get( 'model', None )
		if not model:
			model = ModelManager.get().getModel( target )
		if not model:
			self.model = None
			self.clear()
			return

		rebuildFields = model != self.model
		assert(model)
		if rebuildFields:
			self.clear()
			self.refreshing = True
			# currentId = None
			# for field in model.fieldList:
			# 	lastId = currentId
			# 	currentId = field.id
			# 	if field.getOption('no_edit'):
			# 		if field.id == '----' and lastId != '----':
			# 			self.addSeparator()
			# 		continue
			# 	self.addFieldEditor( field )			
			# assert self.refreshing
			self.addLabelField( model.name, self )
			self.refreshing = False
			
		self.model  = model
		self.target = target
		self.refreshAll()
		self.show()

	def refreshAll( self ):
		target = self.target
		if not target: return
	# 	for field in self.model.fieldList: #todo: just use propMap to iter?
	# 		self._refreshField( field )

	# def refreshField( self, fieldId ):
	# 	for field in self.model.fieldList: #todo: just use propMap to iter?
	# 		if field.id == fieldId:
	# 			self._refreshField( field )
	# 			return True
	# 	return False

	# def _refreshField( self, field ):
	# 	target = self.target
	# 	if not target: return
	# 	editor = self.editors.get( field, None )
	# 	if editor:			
	# 		v = self.model.getFieldValue( target, field.id )
	# 		self.refreshing = True #avoid duplicated update
	# 		editor.refreshing = True
	# 		editor.refreshState()
	# 		editor.set( v )
	# 		editor.refreshing = False
	# 		self.refreshing = False
	# 		editor.setOverrided( self.model.isFieldOverrided( target, field.id ) )

	# def refershFieldState( self, fieldId ):
	# 	target = self.target
	# 	if not target: return
	# 	for field in self.model.fieldList: #todo: just use propMap to iter?
	# 		if field.id == fieldId:
	# 			editor = self.editors.get( field, None )
	# 			if not editor: return
	# 			editor.setOverrided( self.model.isFieldOverrided( target, field.id ) )

	def clear( self ):
		for editor in self.editors.values():
			editor.clear()
			
		layout = self.layout
		while layout.count() > 0:
			child = layout.takeAt( 0 )
			if child :
				w = child.widget()
				if w:
					w.setParent( None )
			else:
				break
		self.editors.clear()
		self.target  = None