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
	_language = "en" # a valid language code (e.g.: "en", "fr", "de", "it", ...)
	_queryText = "watch" # a search query
	_hitCount = 5 #a maximum number of search result to return in one page
	_offset = 5 #the offset to start the page with (if = hitcount ==> page 2)
	
	#create search request
	bxRequest = BxSearchRequest.BxSearchRequest(_language, _queryText, _hitCount)
	
	#set an offset for the returned search results (start at position provided)
	bxRequest.setOffset(_offset)
	
	#add the request
	bxClient.addRequest(bxRequest)
	
	#make the query to Boxalino server and get back the response for all requests (make sure you have added all your requests before calling getResponse; i.e.: do not push the first request, then call getResponse, then add a new request, then call getResponse again it wil not work; N.B.: if you need to do to separate requests call, then you cannot reuse the same instance of BxClient, but need to create a new one)
	bxResponse = bxClient.getResponse()
	
	#loop on the recommended response hit ids and print them
	_logs.append("recommendations of similar items:")
	for _i , _iid in bxResponse.getHitIds(_choiceIdSimilar):
		_logs.append(_i+": returned id "+_iid)

	_logs.append("")

	#retrieve the recommended responses object of the complementary request
	_logs.append("recommendations of complementary items:")
	#loop on the recommended response hit ids and print them
	for _i , _iid in bxResponse.getHitIds(_choiceIdComplementary):
		_logs.append(_i+": returned id "+_iid)

	if _print:
		print "<br/>".join(_logs)
except Exception as e:
	
	#be careful not to print the error message on your publish web-site as sensitive information like credentials might be indicated for debug purposes
	if _print :
		print e