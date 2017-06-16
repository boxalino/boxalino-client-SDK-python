#import "com\boxalino\bxclient\v1";

class BxAutocompleteRequest:
	_language =None
	_queryText =None
	_choiceId =None
	_textualSuggestionsHitCount  =None
	_bxSearchRequest =None
	_highlight =None
	_highlightPre =None
	_highlightPost =None
	_indexId = None

	def __init__(self,language, queryText, textualSuggestionsHitCount, productSuggestionHitCount = 5, autocompleteChoiceId = 'autocomplete', searchChoiceId = 'search', highlight = True, highlightPre = '<em>', highlightPost = '</em>'):
		self._language = language
		self._queryText = queryText;
		self._textualSuggestionsHitCount = textualSuggestionsHitCount;
		self._highlight = highlight;
		self._highlightPre = highlightPre;
		self._highlightPost = highlightPost;
		if autocompleteChoiceId == None:
			autocompleteChoiceId = 'autocomplete';
		self._choiceId = autocompleteChoiceId;
		self._bxSearchRequest =  BxSearchRequest(language, queryText, productSuggestionHitCount, searchChoiceId);

	def getBxSearchRequest(self):
		return self._bxSearchRequest

	def setBxSearchRequest(self,bxSearchRequest):
		self._bxSearchRequest =bxSearchRequest

	def getLanguage(self):
		return self._language

	def setLanguage(self, language):
		self._language =language
	

	def getQuerytext(self):
		return self._queryText
	
	def setQuerytext(self, queryText):
		self._queryText = queryText;
	
	def getChoiceId(self):
		return self._choiceId;
	
	def setChoiceId(self,choiceId):
		self._choiceId=choiceId;
	
	def getTextualSuggestionHitCount(self):
		return self._textualSuggestionsHitCount

	def setTextualSuggestionHitCount(self, textualSuggestionsHitCount):
		self._textualSuggestionsHitCount = textualSuggestionsHitCount

	def getIndexId(self):
		return self._indexId 

	def setIndexId(self, indexId):
		self._indexId = indexId
	
	def setDefaultIndexId(self, indexId):
		if self._indexId == None :
			self._setIndexId(self, indexId)
		self._bxSearchRequest.setDefaultIndexId(self, indexId);	
	
	def getHighlight(self):
		return self._highlight
	

	def getHighlightPre(self):
		return self._highlightPre

	def getHighlightPost(self):
		return self._highlightPost

	def getAutocompleteQuery(self): 
		self = AutocompleteQuery()
		self.__indexId = self.getIndexId();
		self.__language = self._language;
		self.__queryText = self._queryText;
		self.__suggestionsHitCount = self._textualSuggestionsHitCount;
		self.__highlight = self._highlight;
		self.__highlightPre = self._highlightPre;
		self.__highlightPost = self._highlightPost;
		return self;

	__propertyQueries = [];
	def addPropertyQuery(self, field, hitCount, evaluateTotal=False):
		_propertyQuery = PropertyQuery(self) 
		_propertyQuery._name = field 
		_propertyQuery._hitCount = hitCount 
		_propertyQuery._evaluateTotal = evaluateTotal
		self._propertyQueries = _propertyQuery
	
	def resetPropertyQueries(self):
		self._propertyQueries = [];
	
	
	def getAutocompleteThriftRequest(self,profileid, thriftUserRecord):
		_autocompleteRequest = AutocompleteRequest()
		_autocompleteRequest._userRecord = thriftUserRecord
		_autocompleteRequest._profileId = profileid
		_autocompleteRequest._choiceId = self._choiceId
		_autocompleteRequest._searchQuery = self._bxSearchRequest.getSimpleSearchQuery(self)
        _autocompleteRequest._searchChoiceId = self._bxSearchRequest.getChoiceId(self)
		_autocompleteRequest._autocompleteQuery = self.getAutocompleteQuery(self)
		
		if len(self._propertyQueries)>0:
			_autocompleteRequest._propertyQueries = self._propertyQueries;
		return _autocompleteRequest;
	