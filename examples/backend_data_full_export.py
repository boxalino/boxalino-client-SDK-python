import BxClient, BxData
import cgi
_account = "boxalino_automated_tests"
_password = "boxalino_automated_tests"
_domain = ""
_languages = ['en']
_isDev = False
_isDelta = False
_logs = []
_print = True

bxData = BxData.BxData(BxClient.BxClient(_account, _password, _domain), _languages, _isDev, _isDelta)

try :

	_file = '../sample_data/products.csv'
	_itemIdColumn = 'id'
	_colorFile = '../sample_data/color.csv'
	_colorIdColumn = 'color_id'
	_colorLabelColumns = {'en':'value_en'}
	_productToColorsFile = '../sample_data/product_color.csv'

	_sourceKey = bxData.addMainCSVItemFile(_file, _itemIdColumn)
	bxData.addSourceStringField(_sourceKey, "related_product_ids", "related_product_ids")
	bxData.addFieldParameter(_sourceKey, "related_product_ids", "splitValues", ",")

	bxData.addSourceTitleField(_sourceKey, {"en":"name_en"})
	bxData.addSourceDescriptionField(_sourceKey, {"en":"description_en"})
	bxData.addSourceListPriceField(_sourceKey, "list_price")
	bxData.addSourceDiscountedPriceField(_sourceKey, "discounted_price")
	bxData.addSourceLocalizedTextField(_sourceKey, "short_description", {"en":"short_description_en"})
	bxData.addSourceStringField(_sourceKey, "sku", "sku")

	_productToColorsSourceKey = bxData.addCSVItemFile(_productToColorsFile, _itemIdColumn)

	_colorSourceKey = bxData.addResourceFile(_colorFile, _colorIdColumn, _colorLabelColumns)
	bxData.addSourceLocalizedTextField(_productToColorsSourceKey, "color", _colorIdColumn, _colorSourceKey)

	_categoryFile = '../sample_data/categories.csv'
	_categoryIdColumn = 'category_id'
	_parentCategoryIdColumn = 'parent_id'
	_categoryLabelColumns = {'en':'value_en'}
	_productToCategoriesFile = '../sample_data/product_categories.csv'

	_productToCategoriesSourceKey = bxData.addCSVItemFile(_productToCategoriesFile, _itemIdColumn)

	bxData.addCategoryFile(_categoryFile, _categoryIdColumn, _parentCategoryIdColumn, _categoryLabelColumns)
	bxData.setCategoryField(_productToCategoriesSourceKey, _categoryIdColumn)

	_customerFile = '../sample_data/customers.csv'
	_customerIdColumn = 'customer_id'
	_customerSourceKey = bxData.addMainCSVCustomerFile(_customerFile,_customerIdColumn)
	bxData.addSourceStringField(_customerSourceKey, "country", "country")
	bxData.addSourceStringField(_customerSourceKey, "zip", "zip")

	_transactionFile = '../sample_data/transactions.csv'
	_orderIdColumn = 'order_id'
	_transactionProductIdColumn = 'product_id' #the column header row name of the csv with the product id
	_transactionCustomerIdColumn = 'customer_id' #the column header row name of the csv with the customer id
	_orderDateIdColumn = 'order_date' #the column header row name of the csv with the order date
	_totalOrderValueColumn = 'total_order_value' #the column header row name of the csv with the total order value
	_productListPriceColumn = 'price' #the column header row name of the csv with the product list price
	_productDiscountedPriceColumn = 'discounted_price' #the column header row name of the csv with the product price after discounts (real price paid)

	#optional fields, provided here with default values (so, no effect if not provided), matches the field to connect to the transaction product id and customer id columns (if the ids are not the same as the itemIdColumn of your products and customers files, then you can define another field)
	_transactionProductIdField = 'bx_item_id' #default value (can be left null) to define a specific field to map with the product id column
	_transactionCustomerIdField = 'bx_customer_id' #default value (can be left null) to define a specific field to map with the product id column

	#add a csv file as main customer file
	bxData.setCSVTransactionFile(_transactionFile, _orderIdColumn, _transactionProductIdColumn, _transactionCustomerIdColumn, _orderDateIdColumn, _totalOrderValueColumn, _productListPriceColumn, _productDiscountedPriceColumn, _transactionProductIdField,_transactionCustomerIdField)

	#//prepare autocomplete index
	bxData.prepareCorpusIndex()
	fields = ["products_color"]
	bxData.prepareAutocompleteIndex(_fields)

	_logs.append("publish the data specifications")
	bxData.pushDataSpecifications()

	_logs.append("publish the api owner changes") # //if the specifications have changed since the last time they were pushed
	bxData.publishChanges()

	_logs.append("push the data for data sync")
	bxData.pushData()
	if _print:
		print "<br>".join(_logs)

	

except Exception as e:
	#raise e
	if _print :
		print e
