import BxClient
import BxSearchRequest
import BxFacets
import cgi

_account = "boxalino_automated_tests"
_password = "boxalino_automated_tests"
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
	form = cgi.FieldStorage() 
	if  form.getvalue('bx_price') != null :
		_selectedValue = form.getvalue('bx_price')
	else :
		_selectedValue = null

	#//create search request
	bxRequest = BxSearchRequest.BxSearchRequest(_language, _queryText, _hitCount)

	#//add a facert
	facets = BxFacets.BxFacets()
	facets.addPriceRangeFacet(_selectedValue)
	bxRequest.setFacets(facets)

	#//set the fields to be returned for each item in the response
	bxRequest.setReturnFields([facets.getPriceFieldName()])

	#//add the request
	bxClient.addRequest(bxRequest)

	#//make the query to Boxalino server and get back the response for all requests
	bxResponse = bxClient.getResponse()

	#//get the facet responses
	facets = bxResponse.getFacets()

	#//loop on the search response hit ids and print them
	for _fieldValue in facets.getPriceRanges():
		_range = "<a href='?bx_price="+facets.getPriceValueParameterValue(_fieldValue)+"'>"+facets.getPriceValueLabel(_fieldValue)+"</a> ("+facets.getPriceValueCount(_fieldValue)+")"
		if facets.isPriceValueSelected(_fieldValue):
			_range += "<a href='?'>[X]</a>"
		_logs.append(_range)
	

	#//loop on the search response hit ids and print them
	for _id , _fieldValueMap in bxResponse.getHitFieldValues([facets.getPriceFieldName()]):
		_logs.append("<h3>"+_id+"</h3>")
		for _fieldName , _fieldValues in _fieldValueMap:
			_imp = ','.join(_fieldValues)
			_logs.append("Price: " +_imp )
		
	
	
	if _print:
		print "<br/>".join(_logs)
except Exception as e:
	
	#be careful not to print the error message on your publish web-site as sensitive information like credentials might be indicated for debug purposes
	if _print :
		print e