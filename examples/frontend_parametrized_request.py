import BxClient , BxParametrizedRequest ,cgi

_account = "csharp_unittest"
_password = "csharp_unittest"
_domain = ""
_isDev = False
_logs = []
_print = True

bxClient = BxClient.BxClient(_account, _password, _domain, _isDev)
bxClient.setRequestMap(cgi.FieldStorage())

def getItemFieldsCB(ids, fieldNames) :
	#todo your code here to retrieve the fields values
	_values = {}
	for iid in ids:
		_values[iid] = {}
		for fieldName in fieldNames:
			_values[iid][fieldName] = [fieldName + "-value"]
	return _values

try:
	
	_language = "en" # a valid language code (e.g.: "en", "fr", "de", "it", ...)
	_choiceId = "productfinder" #the recommendation choice id (standard choice ids are: "similar" => similar products on product detail page, "complementary" => complementary products on product detail page, "basket" => cross-selling recommendations on basket page, "search"=>search results, "home" => home page personalized suggestions, "category" => category page suggestions, "navigation" => navigation product listing pages suggestions)
	_hitCount = 10 #a maximum number of recommended result to return in one page
	_requestWeightedParametersPrefix = "bxrpw_"
	_requestFiltersPrefix = "bxfi_"
	_requestFacetsPrefix = "bxfa_"
	_requestSortFieldPrefix = "bxsf_"
	_requestReturnFieldsName= "bxrf"
	
	_bxReturnFields = ['id'] #the list of fields which should be returned directly by Boxalino, the others will be retrieved through a call-back function
	_getItemFieldsCB = "getItemFieldsCB"
	
	#create the request and set the parameter prefix values
	bxRequest = BxParametrizedRequest.BxParametrizedRequest(_language, _choiceId, _hitCount, 0, _bxReturnFields, _getItemFieldsCB)
	bxRequest.setRequestWeightedParametersPrefix(_requestWeightedParametersPrefix)
	bxRequest.setRequestFiltersPrefix(_requestFiltersPrefix)
	bxRequest.setRequestFacetsPrefix(_requestFacetsPrefix)
	bxRequest.setRequestSortFieldPrefix(_requestSortFieldPrefix)
	
	bxRequest.setRequestReturnFieldsName(_requestReturnFieldsName)
	
	#add the request
	bxClient.addRequest(bxRequest)
	
	#make the query to Boxalino server and get back the response for all requests
	bxResponse = bxClient.getResponse()
	_logs.append("<h3>weighted parameters</h3>")
	for _fieldName , _fieldValues in bxRequest.getWeightedParameters():
		for _fieldValue , _weight in _fieldValues:
			_logs.append(_fieldName+': '+_fieldValue+': '+_weight)
	
	_logs.append("..")
	
	_logs.append("<h3>filters</h3>")
	_tempFilter = bxRequest.getFilters()
	if _tempFilter:
		for bxFilter in _tempFilter:
			_implode = ','.join(bxFilter.getValues())
			_logs.append(bxFilter.getFieldName()+": "+_implode+ " :" + bxFilter.isNegative())
	
	_logs.append("..")
	
	_logs.append("<h3>facets</h3>")
	bxFacets = bxRequest.getFacets()
	for _fieldName in bxFacets.getFieldNames():
		_implode = ','.join(bxFacets.getSelectedValues(_fieldName))
		_logs.append(_fieldName+": " + _implode)
	
	_logs.append("..")
	
	_logs.append("<h3>sort fields</h3>")
	bxSortFields = bxRequest.getSortFields()
	for _fieldName in bxSortFields.getSortFields():
		_logs.append(_fieldName+": " + bxSortFields.isFieldReverse(_fieldName))
	
	_logs.append("..")
	
	#loop on the recommended response hit ids and print them
	_logs.append("<h3>results</h3>")
	_logs.append(bxResponse.toJson(bxRequest.getAllReturnFields()))

	if _print:
		print "<br/>".join(_logs)
except Exception as e:
	#raise e
	if _print :
		print e
	