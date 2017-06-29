import BxData ,BxClient

_account = "boxalino_automated_tests"
_password = "boxalino_automated_tests"
_domain = ""
_languages = []
_languages.append('en')
_isDev = False
_isDelta = False
_logs = []
_print = True

bxData = BxData.BxData(BxClient.BxClient(_account, _password, _domain), _languages, _isDev,_isDelta)
try:
	_file = '../sample_data/products.csv'
	_itemIdColumn = 'id'
	_sourceKey = bxData.addMainCSVItemFile( _file, _itemIdColumn)
	if _isDelta==False:
		bxData.addSourceTitleField(_sourceKey, {"en":"name_en"})
		bxData.addSourceDescriptionField(_sourceKey, {"en":"description_en"})
		bxData.addSourceListPriceField(_sourceKey, "list_price")
		bxData.addSourceDiscountedPriceField(_sourceKey, "discounted_price")
		bxData.addSourceLocalizedTextField(_sourceKey, "short_description", {"en":"short_description_en"})
		bxData.addSourceStringField(_sourceKey, "sku", "sku")
		_logs.append("publish the data specifications")
		bxData.pushDataSpecifications()
		_logs.append("publish the api owner changes")
		bxData.publishChanges()
	_logs.append("push the data for data sync")
	bxData.pushData()
	if _print:
		print "<br/>".join(_logs)
except Exception as e:
	#raise e
	if _print :
		print e
	