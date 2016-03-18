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