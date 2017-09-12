import BxData ,BxClient

_account = "boxalino_automated_tests"
_password = "boxalino_automated_tests"
_domain = ""
_languages = []
_languages.append('en')
_isDev = False
_isDelta = False
_logs = []
_print = True
BxClient.BxClient.LOAD_CLASSES
bxData = BxData.BxData(BxClient.BxClient(_account, _password, _domain), _languages, _isDev,_isDelta)
try:
	#/**
	#* Publish choices
	#*/
	#//your choie configuration can be generated in 3 possible ways: dev (using dev data), prod (using prod data as on your live web-site), prod-test (using prod data but not affecting your live web-site)
	_isTest = False
	_logs.append("force the publish of your choices configuration: it does it either for dev or prod (above  parameter) and, if isDev is false, you can do it in prod or prod-test<br>")
	bxData.publishChoices(_isTest)
	
	#/**
	#* Prepare corpus index
	#*/
	_logs.append("force the preparation of a corpus index based on all the terms of the last data you sent ==> you need to have published your data before and you will need to publish them again that the corpus is sent to the index<br>")
	bxData.prepareCorpusIndex()
	
	#/**
	#* Prepare autocomplete index
	#*/
	#//NOT YET READY NOTICE: prepareAutocompleteIndex doesn't add the fields yet even if you pass them to the function like in this example here (TODO), for now, you need to go in the data intelligence admin and set the fields manually. You can contact support@boxalino.com to do that.
	#//the autocomplete index is automatically filled with common searches done over time, but of course, before going live, you will not have any. While it is possible to load pre-existing search logs (contact support@boxalino.com to learn how, you can also define some fields which will be considered for the autocompletion anyway (e.g.: brand, product line, etc.).
	_fields = ["products_color"]
	_logs.append("force the preparation of an autocompletion index based on all the terms of the last data you sent ==> you need to have published your data before and you will need to publish them again that the corpus is sent to the index<br>")
	bxData.prepareAutocompleteIndex(_fields)
	if _print:
		print "<br/>".join(_logs)
except Exception as e:
	#raise e
	if _print :
		print e
	