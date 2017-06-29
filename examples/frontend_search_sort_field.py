import BxClient
import BxSearchRequest

_account = "csharp_unittest"
_password = "csharp_unittest"
_domain = ""
_logs = []
_print = True

#Create the Boxalino Client SDK instance
#N.B.: you should not create several instances of BxClient on the same page, make sure to save it in a static variable and to re-use it.
bxClient = BxClient.BxClient(_account, _password, _domain)

try :
	_language = "en" # // a valid language code (e.g.: "en", "fr", "de", "it", ...)
	_queryText = "women" # // a search query to be completed
	_hitCount = 10 # //a maximum number of search result to return in one page
	_sortField = "title" # //sort the search results by this field - IMPORTANT: you need to put "products_" as a prefix to your field name except for standard fields: "title", "body", "discountedPrice", "standardPrice"
	_sortDesc = True # //sort in an ascending / descending way

	#//create search request
	bxRequest = BxSearchRequest.BxSearchRequest(_language, _queryText, _hitCount)

	#//add a sort field in the provided direction
	bxRequest.addSortField(_sortField, _sortDesc)

	#//set the fields to be returned for each item in the response
	bxRequest.setReturnFields([sortField])

	#//add the request
	bxClient.addRequest(bxRequest)

	#//make the query to Boxalino server and get back the response for all requests
	bxResponse = bxClient.getResponse()

	#//loop on the search response hit ids and print them
	for _id , _fieldValueMap in bxResponse.getHitFieldValues([_sortField]):
		_product = "<h3>"+_id+"</h3>"
		for _fieldName , _fieldValues in _fieldValueMap:
			_imp = ','.join(_fieldValues)
			_product += _fieldName+": " + _imp
		
		_logs.append(_product)
	
	
	if _print:
		print "<br/>".join(_logs)
except Exception as e:
	
	#be careful not to print the error message on your publish web-site as sensitive information like credentials might be indicated for debug purposes
	if _print :
		print e