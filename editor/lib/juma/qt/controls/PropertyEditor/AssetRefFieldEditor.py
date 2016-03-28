
import json
import os.path

from PySide import QtGui, QtCore
from PySide.QtCore import Qt

from juma.core import *
from juma.core.ModelManager import *
from PropertyEditor import FieldEditor, registerSimpleFieldEditorFactory
from juma.qt.IconCache import getIcon
from juma.qt.helpers import repolishWidget

from SearchFieldEditor import SearchFieldEditorBase

##----------------------------------------------------------------##
class AssetRefFieldEditor( SearchFieldEditorBase ):	
	def getValueRepr( self, value ):
		lib = AssetLibrary.get()
		if value:
			node = lib.getAssetNode( value )
			if node:
				icon = lib.getAssetIcon( node.getType() )
				return ( value, icon )
		return value #str

	def getSearchType( self ):
		t = self.field.getType()
		print("{} {} {}".format(t, self.getTarget(), t.getAssetType( self.getTarget() )))
		return t.getAssetType( self.getTarget() )

	def getSearchContext( self ):
		return "asset"

	def getSearchInitial( self ):
		return self.target and AssetLibrary.get().getAssetNode( self.target ) or None

	def setValue( self, node ):
		if node:
			value = node.getNodePath()
		else:
			value = None
		super( AssetRefFieldEditor, self ).setValue( value )

	def gotoObject( self ):
		assetBrowser = app.getModule( 'asset_browser' )
		if assetBrowser:
			assetBrowser.locateAsset( self.target )
	
	def formatRefName( self, name )	:
		if isinstance( name, ( str, unicode ) ):
			baseName, ext = os.path.splitext( os.path.basename( name ) )
			return baseName
		else:
			return name

	def findMatchedAssetFromMime( self, mime ):
		if not mime.hasFormat( GII_MIME_ASSET_LIST ): return None
		assetList = json.loads( str(mime.data( GII_MIME_ASSET_LIST )), 'utf-8' )
		matched = False
		assetLib = AssetLibrary.get()

		assets = []
		for path in assetList:			
			asset = assetLib.getAssetNode( path )
			if asset:
				assets.append( asset )

		result = assetLib.enumerateAsset( self.getSearchType(), subset = assets )
		if result:
			return result[0]
		else:
			return None

	def dragEnterEvent( self, ev ):
		mime = ev.mimeData()
		asset = self.findMatchedAssetFromMime( mime )
		button = self.getRefButton()
		if asset:
			button.setProperty( 'dragover', 'ok' )
		else:			
			button.setProperty( 'dragover', 'bad' )
		repolishWidget( button )
		ev.acceptProposedAction()

	def dropEvent( self, ev ):
		button = self.getRefButton()
		button.setProperty( 'dragover', False )
		repolishWidget( button )
		mime = ev.mimeData()
		asset = self.findMatchedAssetFromMime( mime )		
		if not asset: return False
		self.setValue( asset )
		ev.acceptProposedAction()

	def dragLeaveEvent( self, ev ):
		button = self.getRefButton()
		button.setProperty( 'dragover', False )
		repolishWidget( button )

	def isDropAllowed( self ):
		return True

##----------------------------------------------------------------##

registerSimpleFieldEditorFactory( AssetRefType, AssetRefFieldEditor )

