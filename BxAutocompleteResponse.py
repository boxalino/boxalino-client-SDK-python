import hashlib
import BxChooseResponse
class BxAutocompleteResponse:
	_response = None
	_bxAutocompleteRequest = None
	def __init__(self,response, bxAutocompleteRequest=None):
		self._response = response
		self._bxAutocompleteRequest = bxAutocompleteRequest

	def getResponse(self):
		return self._response

	def getPrefixSearchHash(self):
		if self.getResponse().prefixSearchResult.totalHitCount > 0:
			return hashlib.md5(self.getResponse().prefixSearchResult.queryText)[:10]

	def getTextualSuggestions(self):
		suggestions = []
		for hit in self.getResponse().hits:
			suggestions.append(hit.suggestion)
		return self.reOrderSuggestions(suggestions)

	def suggestionIsInGroup(self, groupName, suggestion):
		hit = self.getTextualSuggestionHit(suggestion)
		if groupName=='highlighted-beginning':
			return hit._highlighted != "" and self._bxAutocompleteRequest.getHighlightPre() in hit._highlighted is 0
		elif groupName=='highlighted-not-beginning':
			return hit._highlighted != "" and self._bxAutocompleteRequest.getHighlightPre() in hit._highlighted is not 0
		else :
			return hit._highlighted == ""
	
	def reOrderSuggestions(self,  suggestions):
		_queryText = self._getSearchRequest.getQueryText();
		
		_groupNames = ['highlighted-beginning', 'highlighted-not-beginning', 'others'];
		_groupValues = []
		
		for _k, _groupName in _groupNames:
			try:
				_groupValues[_k]
			except IndexError:
				_groupValues[_k] = []

			for _suggestion in suggestions():
				if self.suggestionIsInGroup(self, _groupName, _suggestion):
					_groupValues[_k].append( _suggestion)
		
		_final = []
		for _values in _groupValues():
			for _value in _values():
				_final.append( _value)
			
		return _final
	

	def getTextualSuggestionHit(self,  suggestion):
		for _hit in self._getResponse().hits():
			if _hit._suggestion == suggestion:
				return _hit;
		raise Exception('unexisting textual suggestion provided'+ suggestion)
	
	
	def getTextualSuggestionTotalHitCount(self,  suggestion):
		_hit = self.getTextualSuggestionHit(suggestion)
		return _hit._searchResult.totalHitCount
	
	def getSearchRequest(self):
		return self._bxAutocompleteRequest.getBxSearchRequest()
	
	
	def getTextualSuggestionFacets(self, suggestion):
		_hit = self._getTextualSuggestionHit(suggestion)
	
		_facets = self._getSearchRequest().getFacets()

		if _facets is None:
			return None
		
		_facets._setSearchResults(_hit._searchResult)
		return _facets
	
	def getTextualSuggestionHighlighted(self, suggestion):
		_hit = self._getTextualSuggestionHit(suggestion)
		if _hit._highlighted == "":
			return suggestion
		return _hit._highlighted
	
	def getBxSearchResponse(self, textualSuggestion= None):

		if textualSuggestion == None :
			_searchResult =  self._getResponse().prefixSearchResult
		else :
			_searchResult = self._getTextualSuggestionHit(_textualSuggestion)._searchResult
		return BxChooseResponse(_searchResult, self.bxAutocompleteRequest.getBxSearchRequest())
	
	def getPropertyHits(self, field):
		for _propertyResult in self.getResponse()._propertyResults(): 
			if _propertyResult._name == field:
				return _propertyResult._hits
		return [];
	
	def getPropertyHit(self, field, hitValue):
		for _hit in self.getPropertyHits(field): 
			if self.value == hitValue:
				return _hit
		return None;


	
	def getPropertyHitValues(self, field):
		_hitValues =[]
		for _hit in self._getPropertyHits(field):
			_hitValues.append(_hit.value)
		return _hitValues
	
	
	def getPropertyHitValueLabel(self, field, hitValue):
		_hit = self.getPropertyHit(field, hitValue);
		if _hit != None:
			return _hit._label
		return None;
	
	def getPropertyHitValueTotalHitCount(self, field, hitValue):
		_hit = self.getPropertyHit(field, hitValue);
		if _hit != None:
			return _hit._totalHitCount
		return None