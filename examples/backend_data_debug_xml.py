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
	
	_sourceKey = bxData.addMainCSVItemFile(_file, _itemIdColumn)
	
	bxData.addSourceTitleField(_sourceKey, {"en":"name_en"})
	bxData.addSourceDescriptionField(_sourceKey, {"en":"description_en"})
	bxData.addSourceListPriceField(_sourceKey, "list_price")
	bxData.addSourceDiscountedPriceField(_sourceKey, "discounted_price")
	bxData.addSourceLocalizedTextField(_sourceKey, "short_description", {"en":"short_description_en"})
	bxData.addSourceStringField(_sourceKey, "sku", "sku")

	if _print:
		print cgi.escape(bxData.getXML()).encode('ascii', 'xmlcharrefreplace')
	

except Exception as e:
	#raise e
	if _print :
		print e
