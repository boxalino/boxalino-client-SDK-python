
import BxClient
import BxRequest

#required parameters you should set for this example to work
_account = "csharp_unittest" # your account name
_password = "csharp_unittest" # your account password
_domain = "" # your web-site domain (e.g.: www.abc.com)
_logs = [] #optional, just used here in example to collect logs
_print = True

#Create the Boxalino Client SDK instance
#N.B.: you should not create several instances of BxClient on the same page, make sure to save it in a static variable and to re-use it.
bxClient = BxClient.BxClient(_account, _password, _domain)

try :
	_language = "en" # a valid language code (e.g.: "en", "fr", "de", "it", ...)
	_choiceId = "similar" #the recommendation choice id (standard choice ids are: "similar" => similar products on product detail page, "complementary" => complementary products on product detail page, "basket" => cross-selling recommendations on basket page, "search"=>search results, "home" => home page personalized suggestions, "category" => category page suggestions, "navigation" => navigation product listing pages suggestions)
	_itemFieldId = "id" # the field you want to use to define the id of the product (normally id, but could also be a group id if you have a difference between group id and sku)
	_itemFieldIdValue = "1940" #the product id the user is currently looking at
	_hitCount = 10 #a maximum number of recommended result to return in one page

	#create similar recommendations request
	bxRequest = BxRequest.BxRequest(_language, _choiceId, _hitCount)
	
	#indicate the product the user is looking at now (reference of what the recommendations need to be similar to)
	bxRequest.setProductContext(_itemFieldId, _itemFieldIdValue)
	
	#add the request
	bxClient.addRequest(bxRequest)
	
	#make the query to Boxalino server and get back the response for all requests
	bxResponse = bxClient.getResponse();
	
	#loop on the recommended response hit ids and print them
	for _i , _iid in bxResponse.getHitIds():
		_logs.append(_i+": returned id "+_iid)

	if _print:
		print "<br/>".join(_logs)

except Exception as e:
	
	#be careful not to print the error message on your publish web-site as sensitive information like credentials might be indicated for debug purposes
	if _print :
		print e

