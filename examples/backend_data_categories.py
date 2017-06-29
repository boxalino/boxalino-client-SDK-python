import BxClient, BxData

_account = "boxalino_automated_tests"
_password = "boxalino_automated_tests"
_domain = ""
_languages = ['en']
_isDev = False
_isDelta = False
_logs = []
_print = True

bxData = BxData.BxData(BxClient.BxClient(_account, _password, _domain), _languages, _isDev, _isDelta)

try:

	_mainProductFile = '../sample_data/products.csv'
	_itemIdColumn = 'id'

	_categoryFile = '../sample_data/categories.csv'
	_categoryIdColumn = 'category_id'
	_parentCategoryIdColumn = 'parent_id'
	_categoryLabelColumns = {'en':'value_en'}
	_productToCategoriesFile = '../sample_data/product_categories.csv'

	_mainSourceKey = bxData.addMainCSVItemFile(_mainProductFile, _itemIdColumn)

	_productToCategoriesSourceKey = bxData.addCSVItemFile(_productToCategoriesFile, _itemIdColumn)

	bxData.addCategoryFile(_categoryFile, _categoryIdColumn, _parentCategoryIdColumn, _categoryLabelColumns)
	if _isDelta==False:

		bxData.setCategoryField(_productToCategoriesSourceKey, _categoryIdColumn)

		_logs.append("publish the data specifications")
		bxData.pushDataSpecifications(False)

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
	