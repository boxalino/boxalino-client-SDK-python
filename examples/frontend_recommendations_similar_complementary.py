import BxClient
import BxRecommendationRequest

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
	_choiceIdSimilar = "similar" #the recommendation choice id (standard choice ids are: "similar" => similar products on product detail page, "complementary" => complementary products on product detail page, "basket" => cross-selling recommendations on basket page, "search"=>search results, "home" => home page personalized suggestions, "category" => category page suggestions, "navigation" => navigation product listing pages suggestions)
	_choiceIdComplementary = "complementary"
	_itemFieldId = "id" # the field you want to use to define the id of the product (normally id, but could also be a group id if you have a difference between group id and sku)
	_itemFieldIdValue = "1940" #the product id the user is currently looking at
	_hitCount = 10 #a maximum number of recommended result to return in one page

	
	#create similar recommendations request
	bxRequestSimilar = BxRecommendationRequest.BxRecommendationRequest(_language, _choiceIdSimilar, _hitCount)
	#indicate the product the user is looking at now (reference of what the recommendations need to be similar to)
	bxRequestSimilar.setProductContext(_itemFieldId, _itemFieldIdValue)
	#add the request
	bxClient.addRequest(bxRequestSimilar)
	
	
	#create complementary recommendations request
	bxRequestComplementary = BxRecommendationRequest.BxRecommendationRequest(_language, _choiceIdComplementary, _hitCount)
	#indicate the product the user is looking at now (reference of what the recommendations need to be similar to)
	bxRequestComplementary.setProductContext(_itemFieldId, _itemFieldIdValue)
	#add the request
	bxClient.addRequest(bxRequestComplementary)
	
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