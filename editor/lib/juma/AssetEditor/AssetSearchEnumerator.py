
from juma.core import *
from juma.SearchView  import requestSearchView, registerSearchEnumerator

##----------------------------------------------------------------##
def assetSearchEnumerator( typeId, context, option ):
	if not context in [ 'all', 'asset' ] : return
	result = []
	lib = AssetLibrary.get()
	for node in AssetLibrary.get().enumerateAsset( typeId ):
		assetType = node.getType()
		iconName = lib.getAssetIcon( assetType ) or 'normal'
		entry = ( node, node.getNodePath(), node.getType(), iconName )
		result.append( entry )
	return result

registerSearchEnumerator( assetSearchEnumerator  )
