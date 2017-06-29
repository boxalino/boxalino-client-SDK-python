import BxClient, BxData

_account = "csharp_unittest"
_password = "csharp_unittest"
_domain = ""
_languages = ['en']
_isDev = False
_isDelta = False
_logs = []
_print = True

bxData = BxData.BxData(BxClient.BxClient(_account, _password, _domain), _languages, _isDev, _isDelta)

try :
	
	_productFile = '../sample_data/products.csv'  # //a csv file with header row
	_itemIdColumn = 'id' # //the column header row name of the csv with the unique id of each item
	
	_customerFile = '../sample_data/customers.csv' # //a csv file with header row
	_customerIdColumn = 'customer_id' # //the column header row name of the csv with the unique id of each item
	
	_transactionFile = '../sample_data/transactions.csv' # //a csv file with header row, this file should contain one entry per product and per transaction (so the same transaction should appear several time if it contains more than 1 product
	_orderIdColumn = 'order_id' # //the column header row name of the csv with the order (or transaction) id
	_transactionProductIdColumn = 'product_id' # //the column header row name of the csv with the product id
	_transactionCustomerIdColumn = 'customer_id' # //the column header row name of the csv with the customer id
	_orderDateIdColumn = 'order_date' # //the column header row name of the csv with the order date
	_totalOrderValueColumn = 'total_order_value' # //the column header row name of the csv with the total order value
	_productListPriceColumn = 'price' # //the column header row name of the csv with the product list price
	_productDiscountedPriceColumn = 'discounted_price' # //the column header row name of the csv with the product price after discounts (real price paid)
	
	#//optional fields, provided here with default values (so, no effect if not provided), matches the field to connect to the transaction product id and customer id columns (if the ids are not the same as the itemIdColumn of your products and customers files, then you can define another field)
	_transactionProductIdField = 'bx_item_id' # //default value (can be left null) to define a specific field to map with the product id column
	_transactionCustomerIdField = 'bx_customer_id' # //default value (can be left null) to define a specific field to map with the product id column
	
	#//add a csv file as main product file
	bxData.addMainCSVItemFile(_productFile, _itemIdColumn) 
	
	#//add a csv file as main customer file
	bxData.addMainCSVCustomerFile(_customerFile, _customerIdColumn) 
	
	#//add a csv file as main customer file
	bxData.setCSVTransactionFile(_transactionFile, _orderIdColumn, _transactionProductIdColumn, _transactionCustomerIdColumn, _orderDateIdColumn, _totalOrderValueColumn, _productListPriceColumn, _productDiscountedPriceColumn, _transactionProductIdField, _transactionCustomerIdField) 
	
	#//this part is only necessary to do when you push your data in full, as no specifications changes should not be published without a full data sync following next
	#//even when you publish your data in full, you don't need to repush your data specifications if you know they didn't change, however, it is totally fine (and suggested) to push them everytime if you are not sure if something changed or not
	if _isDelta==False:

		_logs.append("publish the data specifications") 
		bxData.pushDataSpecifications() 

		_logs.append("publish the api owner changes") # //if the specifications have changed since the last time they were pushed
		bxData.publishChanges() 
	

	_logs.append("push the data for data sync") 
	bxData.pushData() 
	
	if _print:
		print "<br/>".join(_logs)
	
except Exception as e:
	 #raise e
	if _print :
		print e
	
