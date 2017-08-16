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
	_facetField = "products_color" # //the field to consider in the filter - IMPORTANT: you need to put "products_" as a prefix to your field name except for standard fields: "title", "body", "discountedPrice", "standardPrice"
	form = cgi.FieldStorage() 
	if  form.getvalue('bx_category_id') != None :
		_selectedValue = form.getvalue('bx_category_id')
	else :
		_selectedValue = None

	#//create search request
	bxRequest = BxSearchRequest.BxSearchRequest(_language, _queryText, _hitCount)

	#//add a facert
	facets =  BxFacets.BxFacets()
	facets.addCategoryFacet(_selectedValue)
	bxRequest.setFacets(facets)
	
	#add the request
	bxClient.addRequest(bxRequest)
	
	#//make the query to Boxalino server and get back the response for all requests
	bxResponse = bxClient.getResponse()
	
	#//get the facet responses
	facets = bxResponse.getFacets()
	
	#//show the category breadcrumbs
	_level = 0;
	_logs.append("<a href='?'>home</a>")
	for _categoryId , _categoryLabel in facets.getParentCategories():
		_logs.append(">> <a href='?bx_category_id="+_categoryId+"'>"+_categoryLabel+"</a>")
		_level +=1
	
	_logs.append(" ")
	
	#//show the category facet values
	for _value in facets.getCategories():
		_logs.append("<a href='?bx_category_id="+facets.getCategoryValueId(_value)+"'>"+facets.getCategoryValueLabel(_value)+"</a> ("+facets.getCategoryValueCount(_value)+")")
	
	_logs.append(" ")
	
	#//loop on the search response hit ids and print them
	for _i , _id in bxResponse.getHitIds():
		_logs.append(_i+": returned id "+_id)
	
	if _print:
		print "<br/>".join(_logs)
except Exception as e:
	
	#be careful not to print the error message on your publish web-site as sensitive information like credentials might be indicated for debug purposes
	if _print :
		print e