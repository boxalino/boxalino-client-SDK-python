import hashlib
import BxChooseResponse
class BxAutocompleteResponse:
	response = None
	bxAutocompleteRequest = None
	def __init__(self,response, bxAutocompleteRequest=None):
		self.response = response
		self.bxAutocompleteRequest = bxAutocompleteRequest

	def getResponse(self):
		return self.response

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
			return hit.highlighted != "" and self.bxAutocompleteRequest.getHighlightPre() in hit.highlighted is 0
		elif groupName=='highlighted-not-beginning':
			return hit.highlighted != "" and self.bxAutocompleteRequest.getHighlightPre() in hit.highlighted is not 0
		else :
			return hit.highlighted == ""
	
	def reOrderSuggestions(self,  suggestions):
		queryText = self.getSearchRequest().getQueryText();
		
		groupNames = ['highlighted-beginning', 'highlighted-not-beginning', 'others'];
		groupValues = []
		
		for k, groupName in groupNames:
			try:
				groupValues[k]
			except IndexError:
				groupValues[k] = []

			for suggestion in suggestions():
				if self.suggestionIsInGroup(self, groupName, suggestion):
					groupValues[k].append( suggestion)
		
		final = []
		for values in groupValues():
			for value in values():
				final.append( value)
			
		return final
	

	def getTextualSuggestionHit(self,  suggestion):
		for hit in self.getResponse().hits():
			if hit.suggestion == suggestion:
				return hit;
		raise Exception('unexisting textual suggestion provided'+ suggestion)
	
	
	def getTextualSuggestionTotalHitCount(self,  suggestion):
		hit = self.getTextualSuggestionHit(suggestion)
		return hit.searchResult.totalHitCount
	
	def getSearchRequest(self):
		return self.bxAutocompleteRequest.getBxSearchRequest()
	
	
	def getTextualSuggestionFacets(self, suggestion):
		hit = self.getTextualSuggestionHit(suggestion)
	
		facets = self.getSearchRequest().getFacets()

		if facets is None:
			return None
		
		facets._setSearchResults(hit.searchResult)
		return facets
	
	def getTextualSuggestionHighlighted(self, suggestion):
		hit = self.getTextualSuggestionHit(suggestion)
		if hit.highlighted == "":
			return suggestion
		return hit.highlighted
	
	def getBxSearchResponse(self, textualSuggestion= None):

		if textualSuggestion == None :
			searchResult =  self.getResponse().prefixSearchResult
		else :
			searchResult = self.getTextualSuggestionHit(textualSuggestion).searchResult
		return BxChooseResponse.BxChooseResponse(searchResult, self.bxAutocompleteRequest.getBxSearchRequest())
	
	def getPropertyHits(self, field):
		for propertyResult in self.getResponse().propertyResults():
			if propertyResult.name == field:
				return propertyResult.hits
		return [];
	
	def getPropertyHit(self, field, hitValue):
		for hit in self.getPropertyHits(field):
			if self.value == hitValue:
				return hit
		return None;


	
	def getPropertyHitValues(self, field):
		hitValues =[]
		for hit in self.getPropertyHits(field):
			hitValues.append(hit.value)
		return hitValues
	
	
	def getPropertyHitValueLabel(self, field, hitValue):
		hit = self.getPropertyHit(field, hitValue)
		if hit != None:
			return hit.label
		return None
	
	def getPropertyHitValueTotalHitCount(self, field, hitValue):
		hit = self.getPropertyHit(field, hitValue);
		if hit != None:
			return hit.totalHitCount
		return None
