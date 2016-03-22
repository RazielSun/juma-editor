
from PySide import QtGui, QtCore
from PySide.QtCore import Qt

from PropertyEditor import FieldEditor, registerSimpleFieldEditorFactory
from FieldEditorControls import *
from juma.qt.IconCache import getIcon
from juma.core.ModelManager import AssetRefType

##----------------------------------------------------------------##
class BasicAssetRefEditorWidget( QtGui.QWidget ):
	def __init__( self, parent ):
		super(BasicAssetRefEditorWidget, self).__init__( parent )
		self.layout = layout = QtGui.QHBoxLayout( self )
		layout.setSpacing(0)
		layout.setContentsMargins(0,0,0,0)

		self.line = FieldEditorLineEdit( self )
		self.line.setMinimumSize( 50, 16 )
		self.line.setSizePolicy( QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding )
		layout.addWidget( self.line )

		self.btn = QtGui.QToolButton( self )
		self.btn.setMaximumSize( 20, 20 )
		self.btn.setIcon( getIcon("tick_mint") )
		layout.addWidget( self.btn )

##----------------------------------------------------------------##
class BasicAssetRefFieldEditor( FieldEditor ):
	def get( self ):
		return self.assetEdit.line.text()

	def set( self, value ):
		self.assetEdit.line.setText( value or '' )

	def initEditor( self, container ):
		self.assetEdit = BasicAssetRefEditorWidget( container )
		self.assetEdit.btn.clicked.connect( self.doAction )
		return self.assetEdit

	def setReadonly( self, readonly ):
		self.assetEdit.line.setReadOnly( readonly )

	def doAction( self ):
		self.notifyChanged( self.get() )

##----------------------------------------------------------------##

registerSimpleFieldEditorFactory( AssetRefType, BasicAssetRefFieldEditor )
