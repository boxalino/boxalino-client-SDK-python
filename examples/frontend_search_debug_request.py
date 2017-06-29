import BxClient
import BxSearchRequest
import pprint

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
	_hitCount = 10 #; //a maximum number of search result to return in one page

	#//create search request
	bxRequest = BxSearchRequest.BxSearchRequest(_language, _queryText, _hitCount)
	
	#//add the request
	bxClient.addRequest(bxRequest)
	
	#//make the query to Boxalino server and get back the response for all requests
	bxResponse = bxClient.getResponse()
	
	
	if _print:
		print "<pre>"
		print pprint.pprint(bxClient.getThriftChoiceRequest())
		print "</pre>"
except Exception as e:
	
	#be careful not to print the error message on your publish web-site as sensitive information like credentials might be indicated for debug purposes
	if _print :
		print e