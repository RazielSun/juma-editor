#!/usr/bin/env python

from PySide import QtGui, QtCore

def restrainWidgetToScreen( widget ):
	screenRect = QtGui.QApplication.desktop().availableGeometry(widget.mapToGlobal( QPoint(0,0) ));
	widgetRect = widget.frameGeometry()
	pos = widget.pos()
	
	if widgetRect.left() < screenRect.left() :
		pos.setX( pos.x() + screenRect.left() - widgetRect.left() )
	elif widgetRect.right() > screenRect.right():
		pos.setX( pos.x() + screenRect.right() - widgetRect.right() )

	if widgetRect.top() < screenRect.top():
		pos.setY( pos.y() + screenRect.top() - widgetRect.top() )			
	elif widgetRect.bottom() > screenRect.bottom():
		pos.setY( pos.y() + screenRect.bottom() - widgetRect.bottom() )

	widget.move( pos )

def repolishWidget( widget ):
	style = widget.style()
	style.unpolish( widget )
	style.polish( widget )

def addWidgetWithLayout( child, parent = None, **option ):
	direction = option.get('direction', 'vertical')
	layout    = None
	if   direction == 'vertical':
		layout = QtGui.QVBoxLayout()
	elif direction == 'horizontoal':
		layout = QtGui.QHBoxLayout()
	if not parent:
		parent = child.parent()
	parent.setLayout( layout )
	layout.addWidget( child )
	layout.setSpacing(0)
	layout.setContentsMargins(0,0,0,0)
	return child