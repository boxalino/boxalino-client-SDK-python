import json
import BxFacets
from p13n import ttypes
class BxChooseResponse:
	response = None
	bxRequests = None
	
	def __init__(self,response, bxRequests=[]):
		self.response = response
		if isinstance(bxRequests, list):
			self.bxRequests =  bxRequests
		else :
			self.bxRequests = [bxRequests]

	
	def getResponse(self):
		return self.response
	
	def getChoiceResponseVariant(self, choice=None, count= None):
	
		for k , bxRequest in enumerate(self.bxRequests):
			k=k+1
			if choice == None or choice == bxRequest.getChoiceId():
				if count > 0:
					count-=1
					continue
				return self.getChoiceIdResponseVariant(k)
	
	def getChoiceIdResponseVariant(self, id=0):
		response = self.getResponse()
		try:
			if response.variants != None and response.variants[id]:
				return response.variants[id]
		except:
			pass
		if type(response).__name__ == 'SearchResult':
			variant = BxChooseResponse.ttype.Variant()
			variant.searchResult = response
			return variant
		raise Exception('no variant provided in choice response for variant id ' ,id)
		
	
	def getFirstPositiveSuggestionSearchResult(self, variant, maxDistance=10):

		if variant.searchRelaxation.suggestionsResults != None :
			return None

		for searchResult in variant.searchRelaxation.suggestionsResults():
			if searchResult.totalHitCount > 0:
				if searchResult.queryText == "" or variant.searchResult.queryText == "":
					continue
				distance = self.levenshtein(searchResult.queryText, variant.searchResult.queryText)
				if distance <= maxDistance and distance != -1:
					return searchResult
		return None
	
	def getVariantSearchResult(self, variant,considerRelaxation=True, maxDistance=10, discardIfSubPhrases = True):

		searchResult = variant.searchResult
		if considerRelaxation and variant.searchResult.totalHitCount == 0 and  discardIfSubPhrases !=None and self.areThereSubPhrases()!=None:
			return self.getFirstPositiveSuggestionSearchResult(variant, maxDistance)
		return searchResult
	
	def getSearchResultHitIds(self, searchResult, fieldId='id'):
		ids = [];
		if searchResult:
			if searchResult.hits:
				for item in searchResult.hits():
					ids.append( item.values[fieldId][0])
			elif searchResult.hitsGroups != None:
				for hitGroup  in searchResult.hitsGroups():
					ids.append( hitGroup.groupValue)
		return ids
	
	def getHitIds(self, choice=None, considerRelaxation=True, count=0, maxDistance=10, fieldId='id', discardIfSubPhrases = True):
		variant = self.getChoiceResponseVariant(choice, count)
		return self.getSearchResultHitIds(self.getVariantSearchResult(variant, considerRelaxation, maxDistance, discardIfSubPhrases), fieldId)

	def retrieveHitFieldValues(self, item, field, fields, hits):
		fieldValues = []
		for bxRequest in self.bxRequests():
			fieldValues = dict(fieldValues ,bxRequest.retrieveHitFieldValues(item, field, fields, hits))
		return fieldValues
	
	def getSearchHitFieldValues(self, searchResult, fields=None):
		fieldValues = []
		if searchResult != None:
			hits = searchResult.hits
			if searchResult.hits == None:
				hits = []
				for hitGroup in searchResult.hitsGroups :
					hits.append(hitGroup.hits[0])
				
			for item in hits:
				finalFields = fields
				if finalFields == None:
					finalFields = [k for k,v in item.items() if v == item.values]
				
				for field in finalFields:
					try:
						if item.values[field] != None:
							fieldValues[item.values['id'][0]][field] = item.values[field]
					except IndexError: 
						pass
					try:
						if fieldValues[item.values['id'][0]][field]:
							pass
					except	IndexError:
						fieldValues[item.values['id'][0]][field] = self.retrieveHitFieldValues(item, field, searchResult.hits, finalFields)
		return fieldValues
	
	def getRequestFacets(self,  choice=None):
		if choice == None:
			try:
				self.bxRequests[0]
				return self.bxRequests[0].getFacets()
			except IndexError:
				pass
			return None
		for bxRequest in self.bxRequests:
			if bxRequest.getChoiceId() == choice:
				return bxRequest.getFacets()
		return None
	

	def getFacets(self, choice=None, considerRelaxation=True, count=0, maxDistance=10, discardIfSubPhrases = True):
		
		variant = self.getChoiceResponseVariant(choice, count)
		searchResult = self.getVariantSearchResult(variant, considerRelaxation, maxDistance, discardIfSubPhrases)
		facets = self.getRequestFacets(choice)

		if facets==None or searchResult == None:
			return None
		
		facets.setFacetResponse(searchResult.facetResponses)
		return facets


	def getHitFieldValues(self, fields, choice=None, considerRelaxation=True, count=0, maxDistance=10, discardIfSubPhrases = True):
		variant = self.getChoiceResponseVariant(choice, count)
		return self.getSearchHitFieldValues(self.getVariantSearchResult(variant, considerRelaxation, maxDistance, discardIfSubPhrases), fields)
	
	def getFirstHitFieldValue(self, field=None, returnOneValue=True, hitIndex=0, choice=None, count=0, maxDistance=10):
		fieldNames = None
		if field != None:
			fieldNames = [field]
		count = 0
		for id , fieldValueMap in self.getHitFieldValues(fieldNames, choice, True, count, maxDistance):
			count += 1
			if count < hitIndex:
				continue
			
			for fieldName , fieldValues in fieldValueMap:
				if len(fieldValues)>0:
					if returnOneValue==True:
						return fieldValues[0]
					else:
						return fieldValues
		return None
	
	def  getTotalHitCount(self,choice=None, considerRelaxation=True, count=0, maxDistance=10, discardIfSubPhrases = True):
		variant = self.getChoiceResponseVariant(choice, count)
		searchResult = self.getVariantSearchResult(variant, considerRelaxation, maxDistance, discardIfSubPhrases)
		if searchResult == None:
			return 0
		return searchResult.totalHitCount


	def areResultsCorrected(self, choice=None, count=0, maxDistance=10):
		return self.getTotalHitCount(choice, False, count) == 0 and self.getTotalHitCount(choice, True, count, maxDistance) > 0 and self.areThereSubPhrases() == False
	
	
	def areResultsCorrectedAndAlsoProvideSubPhrases(self, choice=None, count=0, maxDistance=10):
		return self.getTotalHitCount(choice, False, count) == 0 and self.getTotalHitCount(choice, True, count, maxDistance, False) > 0 and self.areThereSubPhrases() == True
	
	
	def getCorrectedQuery(self, choice=None, count=0, maxDistance=10):
		variant = self.getChoiceResponseVariant(choice, count)
		searchResult = self.getVariantSearchResult(variant, True, maxDistance, False)
		if searchResult == True:
			return searchResult.queryText
		
		return None


	def areThereSubPhrases(self, choice=None, count=0, maxBaseResults=0):
		variant = self.getChoiceResponseVariant(choice, count)
		try:
			return variant.searchRelaxation.subphrasesResults and len(variant.searchRelaxation.subphrasesResults) > 0 and self.getTotalHitCount(choice, False, count) <= maxBaseResults
		except IndexError:
			pass
	
	def getSubPhrasesQueries(self, choice=None, count=0):
		if self.areThereSubPhrases(self, choice, count)== False:
			return []
		
		queries = []
		variant = self.getChoiceResponseVariant(choice, count)
		for searchResult in variant.searchRelaxation.subphrasesResults:
			queries.append(searchResult.queryText)
		
		return queries
	
	
	def getSubPhraseSearchResult(self , queryText, choice=None, count=0):
		if self.areThereSubPhrases(choice, count)== False:
			return None
		
		_variant = self.getChoiceResponseVariant(choice, count)
		for searchResult in _variant.searchRelaxation.subphrasesResults:
			if searchResult.queryText == queryText:
				return searchResult
			
		
		return None
	
	def getSubPhraseTotalHitCount(self , queryText, choice=None, count=0):
		searchResult = self.getSubPhraseSearchResult(queryText, choice, count)
		if searchResult!= None:
			return searchResult.totalHitCount
		return 0
	

	def getSubPhraseHitIds(self, queryText, choice=None, count=0, fieldId='id'):
		searchResult = self.getSubPhraseSearchResult(queryText, choice, count)
		if searchResult != None:
			return self.getSearchResultHitIds(searchResult, fieldId)
		return []


	def getSubPhraseHitFieldValues(self, queryText, fields, choice=None, considerRelaxation=True, count=0):
		searchResult = self.getSubPhraseSearchResult(queryText, choice, count)
		if  searchResult!= None:
			return self.getSearchHitFieldValues(searchResult, fields)
		return []

	
	def toJson(self, fields):
		object = []
		object['hits'] = []
		for id , fieldValueMap in self.getHitFieldValues(fields):
			hitFieldValues = {}
			for fieldName , fieldValues in fieldValueMap:
				hitFieldValues[fieldName] = {}
				hitFieldValues[fieldName]['values'] = fieldValues
			object['hits'].append({})
			object['hits']['id'] = id
			object['hits']['fieldValues'] = hitFieldValues
		return json.dumps(object)



	def levenshtein(a,b):

		n, m = len(a), len(b)
		if n > m:
			# Make sure n <= m, to use O(min(n,m)) space
			a,b = b,a
			n,m = m,n

		current = range(n+1)
		for i in range(1,m+1):
			previous, current = current, [i]+[0]*n
			for j in range(1,n+1):
				add, delete = previous[j]+1, current[j-1]+1
				change = previous[j-1]
				if a[j-1] != b[i-1]:
					change = change + 1
				current[j] = min(add, delete, change)

		return current[n]

