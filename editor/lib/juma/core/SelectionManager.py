#!/usr/bin/env python

import signals
import weakref

_SelectionManagerRegistry = {}

##----------------------------------------------------------------##
def getSelectionManager( key ):
	return _SelectionManagerRegistry.get( key, None )

##----------------------------------------------------------------##
class SelectionManager(object):	
	def __init__( self, key ):
		assert not _SelectionManagerRegistry.has_key( key ), 'duplicated Manager ' + key
		_SelectionManagerRegistry[ key ] = self
		self.currentSelection = []
		self.key = key

	def clearSelection(self):
		self.changeSelection([])

	def changeSelection( self, selection ):
		if selection: # tommo todo: use weakref to hold selection	
			if not isinstance(selection, list): selection = [ selection ]
		if selection is None:
			selection = []
			if not self.currentSelection: return
		self.currentSelection = selection
		signals.emitNow('selection.changed', selection, self.key )

	def addSelection( self, selection ):
		if not selection: return
		if not isinstance(selection, list): selection = [ selection ]
		currentSelection = self.currentSelection
		for e in selection: # avoid duplicated
			if e in currentSelection:
				currentSelection.remove( e )
		return self.changeSelection( currentSelection + selection )

	def removeSelection( self, selection ):
		if not selection: return
		if not isinstance(selection, list): selection = [ selection ]
		currentSelection = self.currentSelection
		for e in selection: # avoid duplicated
			if e in currentSelection:
				currentSelection.remove( e )
		return self.changeSelection( self.currentSelection )

	def toggleSelection( self, selection ): #if has exist selection, remove only; otherwise add
		if not selection: return
		if not isinstance(selection, list): selection = [ selection ]
		currentSelection = self.currentSelection
		hasPrevious = False
		for e in selection: # avoid duplicated
			if e in currentSelection:
				hasPrevious = True
				currentSelection.remove( e )
		if hasPrevious:
			return self.changeSelection( currentSelection )
		else:
			return self.changeSelection( currentSelection + selection )

	def getSelection(self):
		return self.currentSelection or []

	def getSingleSelection(self):
		return self.currentSelection and self.currentSelection[0] or None
