import BxData ,BxClient

_account = "csharp_unittest"
_password = "csharp_unittest"
_domain = ""
_languages = ['en']
_isDev = False
_isDelta = False
_logs = []
_print = True

bxData = BxData.BxData(BxClient.BxClient(_account, _password, _domain), _languages, _isDev,_isDelta)
try:
	_mainProductFile = '../sample_data/products.csv' #//a csv file with header row
	_itemIdColumn = 'id' # //the column header row name of the csv with the unique id of each item
	
	_colorFile = '../sample_data/color.csv' # //a csv file with header row
	_colorIdColumn = 'color_id' # //column header row name of the csv with the unique category id
	_colorLabelColumns = {'en':'value_en'} # //column header row names of the csv with the category label in each language
	
	_productToColorsFile = '../sample_data/product_color.csv' # //a csv file with header row
	
	#//add a csv file as main product file
	_mainSourceKey = bxData.addMainCSVItemFile(_mainProductFile, _itemIdColumn)
	
	#//add a csv file with products ids to Colors ids
	_productToColorsSourceKey = bxData.addCSVItemFile(_productToColorsFile, _itemIdColumn)
	
	#//add a csv file with Colors
	_colorSourceKey = bxData.addResourceFile(_colorFile, _colorIdColumn, _colorLabelColumns)
	
	#//this part is only necessary to do when you push your data in full, as no specifications changes should not be published without a full data sync following next
	#//even when you publish your data in full, you don't need to repush your data specifications if you know they didn't change, however, it is totally fine (and suggested) to push them everytime if you are not sure if something changed or not
	if _isDelta:
		
		#//declare the color field as a localized textual field with a resource source key
		bxData.addSourceLocalizedTextField(_productToColorsSourceKey, "color", _colorIdColumn, _colorSourceKey)
		
		_logs.append("publish the data specifications")
		bxData.pushDataSpecifications()
		
		_logs.append("publish the api owner changes") #//if the specifications have changed since the last time they were pushed
		bxData.publishChanges()
	
	
	_logs.append("push the data for data sync")
	bxData.pushData()
	if _print:
		print "<br/>".join(_logs)
except Exception as e:
	#raise e
	if _print :
		print e
	