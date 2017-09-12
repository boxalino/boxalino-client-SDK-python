import BxSearchRequest
from p13n import ttypes
class BxAutocompleteRequest:
	language =None
	queryText =None
	choiceId =None
	textualSuggestionsHitCount  =None
	bxSearchRequest =None
	highlight =True
	highlightPre ='<em>'
	highlightPost ='</em>'
	indexId = None

	def __init__(self,language, queryText, textualSuggestionsHitCount, productSuggestionHitCount = 5, autocompleteChoiceId = 'autocomplete', searchChoiceId = 'search'):
		self.language = language
		self.queryText = queryText
		self.textualSuggestionsHitCount = textualSuggestionsHitCount
		if autocompleteChoiceId == None:
			autocompleteChoiceId = 'autocomplete'
		self.choiceId = autocompleteChoiceId
		self.bxSearchRequest =  BxSearchRequest.BxSearchRequest(language, queryText, productSuggestionHitCount, searchChoiceId)

	def getBxSearchRequest(self):
		return self.bxSearchRequest

	def setBxSearchRequest(self,bxSearchRequest):
		self.bxSearchRequest =bxSearchRequest

	def getLanguage(self):
		return self._language

	def setLanguage(self, language):
		self.language = language

	def getQuerytext(self):
		return self.queryText
	
	def setQuerytext(self, queryText):
		self.queryText = queryText
	
	def getChoiceId(self):
		return self.choiceId
	
	def setChoiceId(self,choiceId):
		self.choiceId=choiceId
	
	def getTextualSuggestionHitCount(self):
		return self.textualSuggestionsHitCount

	def setTextualSuggestionHitCount(self, textualSuggestionsHitCount):
		self.textualSuggestionsHitCount = textualSuggestionsHitCount

	def getIndexId(self):
		return self.indexId

	def setIndexId(self, indexId):
		self.indexId = indexId
	
	def setDefaultIndexId(self, indexId):
		if self.indexId == None :
			self.setIndexId( indexId)
		self.bxSearchRequest.setDefaultIndexId( indexId)
	
	def getHighlight(self):
		return self.highlight
	

	def getHighlightPre(self):
		return self.highlightPre

	def getHighlightPost(self):
		return self.highlightPost

	def getAutocompleteQuery(self): 
		autocompleteQuery = ttypes.AutocompleteQuery()
		autocompleteQuery._indexId = self.getIndexId()
		autocompleteQuery._language = self.language
		autocompleteQuery._queryText = self.queryText
		autocompleteQuery._suggestionsHitCount = self.textualSuggestionsHitCount
		autocompleteQuery._highlight = self.highlight
		autocompleteQuery._highlightPre = self.highlightPre
		autocompleteQuery._highlightPost = self.highlightPost
		return autocompleteQuery

	propertyQueries = []
	def addPropertyQuery(self, field, hitCount, evaluateTotal=False):
		propertyQuery = ttypes.PropertyQuery(self)
		propertyQuery.name = field
		propertyQuery.hitCount = hitCount
		propertyQuery.evaluateTotal = evaluateTotal
		self.propertyQueries = propertyQuery
	
	def resetPropertyQueries(self):
		self.propertyQueries = []
	
	
	def getAutocompleteThriftRequest(self,profileid, thriftUserRecord):
		autocompleteRequest = ttypes.AutocompleteRequest()
		autocompleteRequest.userRecord = thriftUserRecord
		autocompleteRequest.profileId = profileid
		autocompleteRequest.choiceId = self.choiceId
		autocompleteRequest.searchQuery = self.bxSearchRequest.getSimpleSearchQuery(self)
		autocompleteRequest.searchChoiceId = self.bxSearchRequest.getChoiceId(self)
		autocompleteRequest.autocompleteQuery = self.getAutocompleteQuery(self)
		if len(self.propertyQueries)>0:
			autocompleteRequest.propertyQueries = self.propertyQueries
		return autocompleteRequest
