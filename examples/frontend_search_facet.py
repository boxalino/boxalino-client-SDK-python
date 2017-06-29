import BxClient
import BxSearchRequest
import BxFacets
import cgi

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
	_facetField = "products_color" # //the field to consider in the filter - IMPORTANT: you need to put "products_" as a prefix to your field name except for standard fields: "title", "body", "discountedPrice", "standardPrice"
	form = cgi.FieldStorage() 
	if  form.getvalue('bx_' + _facetField) != null :
		_selectedValue = form.getvalue('bx_' + _facetField)
	else :
		_selectedValue = null

	#//create search request
	bxRequest = BxSearchRequest.BxSearchRequest(_language, _queryText, _hitCount)

	#//set the fields to be returned for each item in the response
	bxRequest.setReturnFields([_facetField])

	#//add a facert
	facets = BxFacets.BxFacets()
	facets.addFacet(_facetField, _selectedValue);
	bxRequest.setFacets(facets)

	#//add the request
	bxClient.addRequest(bxRequest)

	#//make the query to Boxalino server and get back the response for all requests
	bxResponse = bxClient.getResponse()

	#//get the facet responses
	facets = bxResponse.getFacets()

	#//loop on the search response hit ids and print them
	for _fieldValue in facets.getFacetValues(_facetField):
		_logs.append("<a href='?bx_" + _facetField + "=" + facets.getFacetValueParameterValue(_facetField, _fieldValue) + "'>" + facets.getFacetValueLabel(_facetField, _fieldValue) + "</a> (" +_facets.getFacetValueCount(_facetField, _fieldValue) + ")")
		if facets.isFacetValueSelected(_facetField, _fieldValue):
			_logs.append("<a href='?''>[X]</a>")
		
	

	#//loop on the search response hit ids and print them
	for _id , _fieldValueMap in bxResponse.getHitFieldValues([_facetField]) :
		_logs.append("<h3>"+_id+"</h3>")
		for _fieldName , _fieldValues in _fieldValueMap:
			_imp = ','.join(_fieldValues)
			_logs.append(_fieldName+": " +_imp)
		
	

	if _print:
		print "<br/>".join(_logs)
except Exception as e:
	
	#be careful not to print the error message on your publish web-site as sensitive information like credentials might be indicated for debug purposes
	if _print :
		print e