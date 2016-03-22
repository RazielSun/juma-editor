
from PySide import QtGui, QtCore
from PySide.QtCore import Qt
from PySide.QtCore import QEventLoop, QEvent, QObject

from PropertyEditor import FieldEditor,registerSimpleFieldEditorFactory

from juma.qt.dialogs import requestColorDialog

##----------------------------------------------------------------##
class DialogAutoAcceptEventFilter(QObject):
	def eventFilter(self, obj, event):
		e = event.type()
		if e == QEvent.WindowDeactivate:
			obj.accept()
		return QObject.eventFilter( self, obj, event )

##----------------------------------------------------------------##

def unpackQColor( c ):
	return ( c.redF(), c.greenF(), c.blueF(), c.alphaF() )

def QColorF( r, g, b, a =1 ):
	return QtGui.QColor( r*255, g*255, b*255, a*255)

class ColorBlock( QtGui.QToolButton ):
	colorChanged = QtCore.Signal( QtGui.QColor )

	def __init__(self, parent, color = None, **option ):
		super(ColorBlock, self).__init__( parent )
		self.setColor( color or QtGui.QColor( 1,1,1,1 ) )
		self.clicked.connect( self.onClicked )
		self.setSizePolicy(
			QtGui.QSizePolicy.Expanding,
			QtGui.QSizePolicy.Fixed
			)

		self.title = option.get( 'title', 'Color' )
		self.pen = QtGui.QPen()
		self.brush = QtGui.QBrush()
		self.brush.setStyle( Qt.SolidPattern )
		
	def sizeHint( self ):
		return QtCore.QSize( 60, 20 )

	def getColor( self ):
		return self.color

	def setColor( self, color ):
		self.color = color
		self.colorChanged.emit( self.color )
		self.update()

	def paintEvent( self, event ):
		painter = QtGui.QPainter()
		painter.begin( self )
		painter.setRenderHint( QtGui.QPainter.Antialiasing )
		pen   = self.pen
		brush = self.brush
		painter.setPen( pen )
		painter.setBrush( brush )
		margin = 1
		x = margin
		y = margin
		w = self.width() - margin * 2
		h = self.height() - margin * 2
		#border
		c = QtGui.QColor( self.color )
		c.setAlpha( 255 )
		painter.setBrush( c )
		painter.setPen( QtGui.QPen( QColorF( .5,.5,.5 ) ) )
		painter.drawRect( x,y,w,h )
		#alpha
		alphaH = 4
		p2 = QtGui.QPen()
		p2.setStyle( Qt.NoPen )
		painter.setPen( p2 )
		painter.setBrush( QtGui.QBrush( QColorF( 0,0,0 ) ) )
		painter.drawRect( x + 1, y + h - alphaH ,w - 2, alphaH )
		
		painter.setBrush( QtGui.QBrush( QColorF( 1,1,1 ) ) )
		painter.drawRect( x + 1, y + h - alphaH ,( w -2 ) * self.color.alphaF(), alphaH  )


	def onClicked( self ):
		self.prevColor = self.color
		requestColorDialog(
			None,
			on_cancel = self.onCancel,
			on_change = self.onChange,
			on_changed = self.onChanged,
			original_color  = self.color
		)

	def onCancel( self ):
		self.setColor( self.prevColor )
		self.setFocus()

	def onChange( self, color ):
		self.setColor( color )

	def onChanged( self, color ):
		self.setColor( color )
		self.setFocus()


##----------------------------------------------------------------##
class ColorFieldEditor( FieldEditor ):
	def get( self ):
		return unpackQColor( self.colorBlock.getColor() )

	def set( self, value ):
		self.colorBlock.setColor( QColorF( *value ) )


	def onColorChanged( self, state ):
		return self.notifyChanged( self.get() )

	def initEditor( self, container ):
		self.colorBlock = ColorBlock( container )
		self.colorBlock.colorChanged.connect( self.onColorChanged )
		if self.getOption( 'readonly', False ):
			self.colorBlock.setEnabled( False )
		return self.colorBlock

##----------------------------------------------------------------##

registerSimpleFieldEditorFactory( 'color',    ColorFieldEditor )
