import BxClient
import BxRecommendationRequest

_account = "csharp_unittest"
_password = "csharp_unittest"
_domain = ""
_logs = []
_print = True

bxClient = BxClient.BxClient(_account, _password, _domain)

try:
	
	_language = "en" # a valid language code (e.g.: "en", "fr", "de", "it", ...)
	_choiceId = "basket" #the recommendation choice id (standard choice ids are: "similar" => similar products on product detail page, "complementary" => complementary products on product detail page, "basket" => cross-selling recommendations on basket page, "search"=>search results, "home" => home page personalized suggestions, "category" => category page suggestions, "navigation" => navigation product listing pages suggestions)
	_itemFieldId = "id"# the field you want to use to define the id of the product (normally id, but could also be a group id if you have a difference between group id and sku)
	_itemFieldIdValuesPrices = []
	_itemFieldIdValuesPrices.append({"id":"1940", "price":10.80})
	_itemFieldIdValuesPrices.append({"id":"1234", "price":130.5}) #the product ids and their prices that the user currently has in his basket
	_hitCount = 10 #a maximum number of recommended result to return in one page

	#//create similar recommendations request
	bxRequest = BxRecommendationRequest.BxRecommendationRequest(_language, _choiceId, _hitCount)
	
	#//indicate the products the user currently has in his basket (reference of products for the recommendations)
	bxRequest.setBasketProductWithPrices(_itemFieldId, _itemFieldIdValuesPrices)
	
	#//add the request
	bxClient.addRequest(bxRequest)
	
	#//make the query to Boxalino server and get back the response for all requests
	bxResponse = bxClient.getResponse()
	for _i , _iid in bxResponse.getHitIds():
		_logs.append(_i+": returned id "+_iid)
	
	if _print:
		print "<br/>".join(_logs)
except Exception as e:
	#raise e
	if _print :
		print e
	