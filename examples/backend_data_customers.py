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

	_productFile = '../sample_data/products.csv'
	_itemIdColumn = 'id'
	_customerFile = '../sample_data/customers.csv'
	_customerIdColumn = 'customer_id'
	bxData.addMainCSVItemFile(_productFile, _itemIdColumn)
	_customerSourceKey = bxData.addMainCSVCustomerFile(_customerFile, _customerIdColumn)
	if _isDelta==False:

		bxData.addSourceStringField(_customerSourceKey, "country", "country")
		bxData.addSourceStringField(_customerSourceKey, "zip", "zip")
		_logs.append("publish the data specifications")
		bxData.pushDataSpecifications()
		_logs.append("publish the api owner changes")
		bxData.publishChanges()
	

	_logs.append("push the data for data sync")
	if _print:
		print "<br>".join(_logs)
	
	bxData.pushData()

except Exception as e:
	#raise e
	if _print :
		print e
