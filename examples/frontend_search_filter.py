import BxClient
import BxSearchRequest
import BxFilter

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
	_filterField = "id" # //the field to consider in the filter
	_filterValues = ["41", "1940"] # //the field to consider any of the values should match (or not match)
	_filterNegative = True # //false by default, should the filter match the values or not?
	
	#//create search request
	bxRequest = BxSearchRequest.BxSearchRequest(_language, _queryText, _hitCount)
	
	#//add a filter
	bxRequest.addFilter(BxFilter.BxFilter(_filterField, _filterValues, _filterNegative))
	
	#//add the request
	bxClient.addRequest(bxRequest)
	
	#//make the query to Boxalino server and get back the response for all requests
	bxResponse = bxClient.getResponse()
	
	#//loop on the search response hit ids and print them
	for _i , _id in bxResponse.getHitIds():
		_logs.append(_i+": returned id "+_id)
		
	
	
	if _print:
		print "<br/>".join(_logs)
except Exception as e:
	
	#be careful not to print the error message on your publish web-site as sensitive information like credentials might be indicated for debug purposes
	if _print :
		print e