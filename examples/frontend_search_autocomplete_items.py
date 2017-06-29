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
	_language = "en" # a valid language code (e.g.: "en", "fr", "de", "it", ...)
	_queryText = "whit" # a search query to be completed
	_textualSuggestionsHitCount = 10 #a maximum number of search textual suggestions to return in one page
	_fieldNames = ['title'] #return the title for each item returned (globally and per textual suggestion) - IMPORTANT: you need to put "products_" as a prefix to your field name except for standard fields: "title", "body", "discountedPrice", "standardPrice"

	#create search request
	bxRequest = BxAutocompleteRequest.BxAutocompleteRequest(_language, _queryText, _textualSuggestionsHitCount)
	
	#set the fields to be returned for each item in the response
	bxRequest.getBxSearchRequest().setReturnFields(_fieldNames)
	
	#set the request
	bxClient.setAutocompleteRequest(bxRequest)
	
	#make the query to Boxalino server and get back the response for all requests
	bxAutocompleteResponse = bxClient.getAutocompleteResponse()

	#loop on the search response hit ids and print them
	_logs.append("textual suggestions for "+_queryText+":<br>")
	
	for _suggestion in bxAutocompleteResponse.getTextualSuggestions():
		_logs.append("<div style='border:1px solid; padding:10px; margin:10px'>")
		_logs.append("<h3>"+_suggestion+"</b></h3>")

		_logs.append("item suggestions for suggestion "+_suggestion+":<br>")
		#//loop on the search response hit ids and print them
		for _iid , _fieldValueMap in bxAutocompleteResponse.getBxSearchResponse(_suggestion).getHitFieldValues(_fieldNames):
			_logs.append("<div>"+_iid)
			for _fieldName,  _fieldValues in _fieldValueMap  :
				_imp = ','.join(_fieldValues)
				_logs.append(" - "+_fieldName+": " +_imp)
			
			_logs.append("</div>")
		
		_logs.append("</div>")
	

	_logs.append("global item suggestions for "+_queryText+":<br>")
	#loop on the search response hit ids and print them
	for _iid ,_fieldValueMap in bxAutocompleteResponse.getBxSearchResponse().getHitFieldValues(_fieldNames) :
		_item = _iid
		for _fieldName , _fieldValues in _fieldValueMap :
			_imp =','.join(_fieldValues)
			_item += " - "+_fieldName+": " +_imp +"<br>"
		
		_logs.append(_item)
	
	if _print:
		print "<br/>".join(_logs)
except Exception as e:
	
	#be careful not to print the error message on your publish web-site as sensitive information like credentials might be indicated for debug purposes
	if _print :
		print e