from PySide import QtGui, QtCore
from PySide.QtCore import Qt

from juma.core.ModelManager import *
from FieldEditorControls import *

##----------------------------------------------------------------##
		
_FieldEditorFactories = []

##----------------------------------------------------------------##
class FieldEditorFactory():
	def getPriority( self ):
		return 0

	def build( self, parentEditor, field, context = None ):
		return None

##----------------------------------------------------------------##
class SimpleFieldEditorFactory( FieldEditorFactory ):
	def __init__( self, typeId, createClass, priority = -1 ):
		self.targetTypeId = typeId
		self.create = createClass
		self.priority = priority

	def getPriority( self ):
		return self.priority

	def createEditor( self, parentEditor, field ):
		return self.create( parentEditor, field )

	def build( self, parentEditor, field, context = None ):
		dataType  = field._type
		if field.getOption( 'objtype', None) == 'ref' :
			dataType    = ReferenceType
		while True:
			if dataType == self.targetTypeId:
				return self.createEditor( parentEditor, field )
			dataType = getSuperType( dataType )
			if not dataType: return None

##----------------------------------------------------------------##
def registerFieldEditorFactory( factory ):
	assert isinstance( factory, FieldEditorFactory )
	p = factory.getPriority()
	for i, fe in enumerate( _FieldEditorFactories ):
		if p >= fe.getPriority():
			_FieldEditorFactories.insert( i, factory )
			return
	_FieldEditorFactories.append( factory )

def registerSimpleFieldEditorFactory( dataType, clas, priority = -1 ):
	factory = SimpleFieldEditorFactory( dataType, clas, priority )
	registerFieldEditorFactory( factory )

##----------------------------------------------------------------##
def buildFieldEditor( parentEditor, field ):
	for factory in _FieldEditorFactories:
		editor = factory.build( parentEditor, field )
		if editor:
			return editor
	return None

##----------------------------------------------------------------##
class PropertyEditor( QtGui.QFrame ):
	propertyChanged = QtCore.Signal( object, str, object )
	objectChanged   = QtCore.Signal( object )
	contextMenuRequested = QtCore.Signal( object, str )

	def __init__( self, parent ):	
		super( PropertyEditor, self ).__init__( parent )
		self.setObjectName( 'PropertyEditor' )
		layout = QtGui.QFormLayout()
		self.setLayout( layout )
		self.layout = layout
		self.layout.setHorizontalSpacing( 5 )
		self.layout.setVerticalSpacing( 5 )
		self.layout.setContentsMargins(4,4,4,4)
		self.layout.setLabelAlignment( Qt.AlignLeft )
		self.layout.setFieldGrowthPolicy( QtGui.QFormLayout.ExpandingFieldsGrow )
		self.setSizePolicy( QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding )

		self.editors    = {}
		self.target     = None
		self.refreshing = False
		self.context    = None
		self.model      = False
		self.fieldMap 	= {}
		self.readonly   = False
		self.clear()

	def addFieldEditor( self, field ):
		label = field.label
		editor  =  buildFieldEditor( self, field )
		labelWidget  = editor.initLabel( label, self )
		editorWidget = editor.initEditor( self )
		editorWidget.setObjectName( 'FieldEditor' )
		labelWidget.setObjectName( 'FieldLabel' )
		if labelWidget in (None, False):
			self.layout.addRow ( editorWidget )
		else:
			self.layout.addRow ( labelWidget, editorWidget )
		self.editors[ field ] = editor
		return editor

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
			self.fieldMap.clear()
			self.refreshing = True
			currentId = None
			for field in model.fieldList:
				lastId = currentId
				currentId = field.id
				self.fieldMap[currentId] = field
				if field.getOption('no_edit'):
					continue
				self.addFieldEditor( field )			
			assert self.refreshing
			self.refreshing = False

		self.model  = model
		self.target = target
		self.refreshAll()
		self.show()

	def setContext( self, context ):
		self.context = context

	def refreshAll( self ):
		target = self.target
		if not target: return
		for field in self.model.fieldList:
			self._refreshField( field )

	def refreshField( self, fieldId ):
		field = self.fieldMap.get(fieldId, None)
		if field is None:
			return False
		self._refreshField( field )

	def _refreshField( self, field ):
		target = self.target
		if not target:
			return
		editor = self.editors.get( field, None )

		if editor:
			v = self.model.getFieldValue( target, field.id )
			self.refreshing = True # avoid duplicated update
			editor.refreshing = True
			editor.refreshState()
			editor.set( v )
			editor.refreshing = False
			self.refreshing = False
			editor.setOverrided( self.model.isFieldOverrided( target, field.id ) )

	def refreshFieldState( self, fieldId ):
		target = self.target
		if not target: return
		field = self.fieldMap.get(fieldId, None)
		if field != None:
			editor = self.editors.get( field, None )
			if not editor: return
			editor.setOverrided( self.model.isFieldOverrided( target, field.id ) )

	def calculateField( self, fieldId ):
		target = self.target
		if not target: return
		field = self.fieldMap.get(fieldId, None)
		if field != None:
			self.model.calculateField( target, field.id )

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

	def setReadonly( self, readonly = True ):
		self.readonly = readonly
		self.refreshAll()

	def isReadonly( self ):
		return self.readonly

	# CALLBACKS #
	def onPropertyChanged( self, field, value ):
		if self.refreshing : return
		self.model.setFieldValue( self.target, field.id, value )
		self.propertyChanged.emit( self.target, field.id, value )
		self.objectChanged.emit( self.target )

	def onMoaiClean( self ):
		self.clear()
		self.model = False

##----------------------------------------------------------------##
class FieldEditor( object ):
	def __init__( self, parent, field, fieldType = None ):
		self.setTarget( parent, field )
		self.fieldType = fieldType or field._type
		self.overrided = False

	def setTarget( self, parent, field ):
		self.field   = field
		self.parent  = parent

	def getTarget( self ):
		return self.parent.getTarget()

	def getFieldType( self ):
		return self.fieldType

	def getContext( self ):
		return self.parent.context

	def getOption( self, key, v = None ):
		return self.field.option.get( key, v )

	def notifyChanged( self, value ):
		return self.parent.onPropertyChanged( self.field, value )

	def notifyContextMenuRequested( self ):
		return self.parent.onContextMenuRequested( self.field )

	def notifyObjectChanged( self ):
		return self.parent.onObjectChanged()
		
	def get( self ):
		pass

	def set( self, value ):
		pass

	def setReadonly( self, readonly = True ):
		pass

	def setOverrided( self, overrided = True ):
		if overrided == self.overrided: return
		self.overrided = overrided
		self.labelWidget.setProperty( 'overrided', overrided )
		repolishWidget( self.labelWidget )

	def setRecording( self, recording = True ):
		self.labelWidget.setProperty( 'recording', recording )
		repolishWidget( self.labelWidget )

	def initLabel( self, label, container ):
		self.labelWidget = FieldEditorLabel( container )
		self.labelWidget.setEditor( self )
		self.labelWidget.setText( label )
		return self.labelWidget

	def initEditor( self, container ):
		return QtGui.QWidget( container )

	def refreshState( self ):
		readonly = self.getOption( 'readonly', False ) or self.parent.isReadonly()
		self.setReadonly( readonly )
		
	def clear( self ):
		pass
