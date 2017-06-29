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
	
	_requestParameters = {"geoIP-latitude" : ["47.36"], "geoIP-longitude" : ["6.1517993"]}
	
	#//create search request
	bxRequest = BxSearchRequest.BxSearchRequest(_language, _queryText, _hitCount)
	
	#//set the fields to be returned for each item in the response
	for _k , _v in _requestParameters:
		bxClient.addRequestContextParameter(_k, _v)
	
	
	#//add the request
	bxClient.addRequest(bxRequest)
	
	#//make the query to Boxalino server and get back the response for all requests
	bxResponse = bxClient.getResponse()
	
	#//indicate the search made with the number of results found
	_logs.append("Results for query "+_queryText+" ("+bxResponse.getTotalHitCount()+"):<br>")

	#//loop on the search response hit ids and print them
	for _i , _id in bxResponse.getHitIds():
		_logs.append(_i+": returned id "+_id)
	
	
	if _print:
		print "<br/>".join(_logs)
except Exception as e:
	
	#be careful not to print the error message on your publish web-site as sensitive information like credentials might be indicated for debug purposes
	if _print :
		print e