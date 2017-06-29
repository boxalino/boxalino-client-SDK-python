import BxClient
import BxAutocompleteRequest

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
	_queryText = "whit" # a search query to be completed
	_textualSuggestionsHitCount = 10 #a maximum number of search textual suggestions to return in one page

	#create search request
	bxRequest = BxAutocompleteRequest.BxAutocompleteRequest(_language, _queryText, _textualSuggestionsHitCount)
	
	#set the request
	bxClient.setAutocompleteRequest(bxRequest)
	
	#make the query to Boxalino server and get back the response for all requests
	bxAutocompleteResponse = bxClient.getAutocompleteResponse()
	
	#loop on the search response hit ids and print them
	_logs.append("textual suggestions for "+_queryText+":")
	for _suggestion in bxAutocompleteResponse.getTextualSuggestions():
		_logs.append(_suggestion)
	
	
	if len(bxAutocompleteResponse.getTextualSuggestions()) == 0:
		_logs.append("There are no autocomplete textual suggestions. This might be normal, but it also might mean that the first execution of the autocomplete index preparation was not done and published yet. Please refer to the example backend_data_init and make sure you have done the following steps at least once: 1) publish your data 2) run the prepareAutocomplete case 3) publish your data again")

	if _print:
		print "<br/>".join(_logs)
except Exception as e:
	
	#be careful not to print the error message on your publish web-site as sensitive information like credentials might be indicated for debug purposes
	if _print :
		print e