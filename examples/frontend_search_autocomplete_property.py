import BxClient
import BxAutocompleteRequest

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
	_queryText = "a" # // a search query to be completed
	_textualSuggestionsHitCount = 10 # //a maximum number of search textual suggestions to return in one page
	_property = 'categories' # //the properties to do a property autocomplete request on, be careful, except the standard "categories" which always work, but return values in an encoded way with the path ( "ID/root/level1/level2"), no other properties are available for autocomplete request on by default, to make a property "searcheable" as property, you must set the field parameter "propertyIndex" to "true"
	_propertyTotalHitCount = 5 # //the maximum number of property values to return
	_propertyEvaluateCounters = True # //should the count of results for each property value be calculated? if you do not need to retrieve the total count for each property value, please leave the 3rd parameter empty or set it to false, your query will go faster

	#//create search request
	bxRequest = BxAutocompleteRequest.BxAutocompleteRequest(_language, _queryText, _textualSuggestionsHitCount)
	
	#//indicate to the request a property index query is requested
	bxRequest.addPropertyQuery(_property, _propertyTotalHitCount, True)
	
	#//set the request
	bxClient.setAutocompleteRequest(bxRequest)
	#//make the query to Boxalino server and get back the response for all requests
    
	bxAutocompleteResponse = bxClient.getAutocompleteResponse()

	#//loop on the search response hit ids and print them
	_logs.append("property suggestions for "+_queryText+":<br>")
	for _hitValue in bxAutocompleteResponse.getPropertyHitValues(_property):
		_label = bxAutocompleteResponse.getPropertyHitValueLabel(_property,_hitValue)
		_totalHitCount = bxAutocompleteResponse.getPropertyHitValueTotalHitCount(_property, _hitValue)
		_result = "<b>"+_hitValue+":</b><ul><li>label="+_label+"</li> <li>totalHitCount="+_totalHitCount+"</li></ul>";
		_logs.append(_result)
	
	
	if _print:
		print "<br/>".join(_logs)
except Exception as e:
	
	#be careful not to print the error message on your publish web-site as sensitive information like credentials might be indicated for debug purposes
	if _print :
		print e