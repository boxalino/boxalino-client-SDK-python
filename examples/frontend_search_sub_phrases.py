import BxClient
import BxRequest
import BxSearchRequest

account = "csharp_unittest"
password = "csharp_unittest"
domain = ""
logs = []
_print = True

#Create the Boxalino Client SDK instance
#N.B.: you should not create several instances of BxClient on the same page, make sure to save it in a static variable and to re-use it.
bxClient = BxClient.BxClient(account, password, domain)

try :
	language = "en" # // a valid language code (e.g.: "en", "fr", "de", "it", ...)
	queryText = "women pack" # // a search query to be completed
	hitCount = 10 # //a maximum number of search result to return in one page
	#//create search request
	bxRequest = BxSearchRequest.BxSearchRequest(language, queryText, hitCount)
	#BxRequest.BxRequest.setQueryText( queryText)

	#//add the request
	bxClient.addRequest(bxRequest)
	#print bxClient.getThriftChoiceRequest()
	#//make the query to Boxalino server and get back the response for all requests
 	bxResponse = bxClient.getResponse()
	
	#//check if the system has generated sub phrases results
	if bxResponse.areThereSubPhrases():
		logs.append("No results found for all words in " +queryText + ", but following partial matches were found:<br\>")
		for _subPhrase in bxResponse.getSubPhrasesQueries():
			logs.append("Results for "+_subPhrase +" (" +bxResponse.getSubPhraseTotalHitCount(_subPhrase)+ " hits):")
			#//loop on the search response hit ids and print them
			for i , id in bxResponse.getSubPhraseHitIds(_subPhrase):
				logs.append(i+": returned id "+id)
			logs.append('')
	else :
		#//loop on the search response hit ids and print them
		for i , id in bxResponse.getHitIds():
			logs.append(i+": returned id "+id)
		
	
	if _print:
		print "<br/>".join(logs)
except Exception as e:
	
	#be careful not to print the error message on your publish web-site as sensitive information like credentials might be indicated for debug purposes
	if _print :
		print e